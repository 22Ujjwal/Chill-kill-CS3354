"""
Main API server for the chatbot backend.
Flask-based REST API for interacting with the RAG chatbot.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
import os
from datetime import datetime

# Setup logging FIRST
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app early
app = Flask(__name__)
CORS(app)

# Import settings (lightweight, just loads env vars)
from src.config.settings import (
    FIRECRAWL_API_KEY,
    GOOGLE_API_KEY,
    PINECONE_API_KEY,
    PINECONE_INDEX_NAME,
    TARGET_WEBSITE_URL,
    CRAWL_LIMIT,
    TOP_K_RESULTS,
    TEMPERATURE
)

# Global state
chatbot = None
embedder = None
vector_store = None
initialization_complete = False


def initialize_backend():
    """Initialize all backend components: scraper, embedder, vector store."""
    global chatbot, embedder, vector_store, initialization_complete
    
    try:
        logger.info("Initializing backend components...")
        
        # Import heavy modules only when needed
        from src.modules.gemini_embedder import GeminiEmbedder
        from src.modules.pinecone_store import PineconeVectorStore
        from src.modules.rag_pipeline import create_rag_chatbot
        
        # Step 1: Initialize embedder
        embedder = GeminiEmbedder(GOOGLE_API_KEY)
        logger.info("✓ Gemini embedder initialized")
        
        # Step 2: Initialize Pinecone vector store
        vector_store = PineconeVectorStore(
            api_key=PINECONE_API_KEY,
            index_name=PINECONE_INDEX_NAME
        )
        logger.info("✓ Pinecone vector store initialized")
        
        # Step 3: Create RAG chatbot
        chatbot = create_rag_chatbot(
            google_api_key=GOOGLE_API_KEY,
            pinecone_api_key=PINECONE_API_KEY,
            pinecone_index_name=PINECONE_INDEX_NAME,
            embedder_instance=embedder,
            top_k=TOP_K_RESULTS,
            temperature=TEMPERATURE
        )
        logger.info("✓ RAG chatbot initialized")
        
        initialization_complete = True
        logger.info("✓ Backend initialization complete!")
        
        return True
        
    except Exception as e:
        logger.error(f"Error during backend initialization: {e}")
        return False


@app.before_request
def log_request():
    """Log incoming requests for debugging."""
    logger.info(f"Incoming request: {request.method} {request.path}")


@app.route("/api/health", methods=["GET"])
def health_check():
    """Health check endpoint."""
    logger.info("Health check requested")
    return jsonify({
        "status": "healthy",
        "chatbot_ready": initialization_complete,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route("/api/initialize", methods=["POST"])
def initialize_endpoint():
    """Initialize backend components and scrape website."""
    try:
        global chatbot, embedder, vector_store, initialization_complete
        
        if initialization_complete:
            return jsonify({
                "status": "already_initialized",
                "message": "Backend is already initialized"
            }), 200
        
        # Initialize components
        if not initialize_backend():
            return jsonify({
                "status": "error",
                "message": "Failed to initialize backend components"
            }), 500
        
        # Import locally to defer heavy imports
        from src.modules.firecrawl_scraper import scrape_nintendo_website
        from src.modules.gemini_embedder import embed_content_for_storage
        from src.modules.pinecone_store import store_documents_in_pinecone
        
        # Optional: clear existing vectors if requested (rebuild)
        try:
            payload = request.get_json(silent=True) or {}
            if payload.get("rebuild") and vector_store:
                logger.info("Rebuild requested: clearing Pinecone namespace before upsert...")
                vector_store.clear_namespace()
        except Exception as e:
            logger.warning(f"Unable to process rebuild flag: {e}")

        # Step 4: Scrape website (+ explicit tech-specs page)
        logger.info(f"Scraping website: {TARGET_WEBSITE_URL}")
        tech_specs_url = "https://www.nintendo.com/us/gaming-systems/switch-2/tech-specs/"
        documents = scrape_nintendo_website(
            api_key=FIRECRAWL_API_KEY,
            target_url=TARGET_WEBSITE_URL,
            limit=CRAWL_LIMIT,
            additional_urls=[tech_specs_url]
        )
        
        if not documents:
            return jsonify({
                "status": "error",
                "message": "Failed to scrape website"
            }), 500
        
        logger.info(f"✓ Scraped {len(documents)} documents")
        
        # Step 5: Embed documents
        logger.info("Embedding documents...")
        embedded_docs = embed_content_for_storage(GOOGLE_API_KEY, documents)
        
        if not embedded_docs:
            return jsonify({
                "status": "error",
                "message": "Failed to embed documents"
            }), 500
        
        logger.info(f"✓ Embedded {len(embedded_docs)} documents")
        
        # Step 6: Store in Pinecone
        logger.info("Storing embeddings in Pinecone...")
        success = store_documents_in_pinecone(
            api_key=PINECONE_API_KEY,
            index_name=PINECONE_INDEX_NAME,
            documents=embedded_docs
        )
        
        if not success:
            return jsonify({
                "status": "error",
                "message": "Failed to store embeddings in Pinecone"
            }), 500
        
        logger.info("✓ Embeddings stored in Pinecone")
        
        return jsonify({
            "status": "initialized",
            "message": "Backend fully initialized and ready",
            "documents_processed": len(embedded_docs),
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error during initialization: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/query", methods=["POST"])
def query_endpoint():
    """Query the chatbot."""
    if not initialization_complete or not chatbot:
        return jsonify({
            "status": "error",
            "message": "Chatbot not initialized. Please call /api/initialize first."
        }), 400
    
    try:
        data = request.get_json()
        query = data.get("query", "").strip()
        
        if not query:
            return jsonify({
                "status": "error",
                "message": "Query cannot be empty"
            }), 400
        
        # Get RAG response
        result = chatbot.answer_query(query)
        
        return jsonify({
            "status": "success",
            "query": result["query"],
            "response": result["response"],
            "context_documents_count": len(result["context_documents"]),
            "context_length": result["context_length"],
            "turn": result["conversation_turn"],
            "timestamp": datetime.now().isoformat()
        }), 200
        
    except Exception as e:
        logger.error(f"Error processing query: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/history", methods=["GET"])
def history_endpoint():
    """Get conversation history."""
    if not chatbot:
        return jsonify({
            "status": "error",
            "message": "Chatbot not initialized"
        }), 400
    
    try:
        history = chatbot.get_conversation_history()
        return jsonify({
            "status": "success",
            "history": history,
            "turns": len(history) // 2
        }), 200
        
    except Exception as e:
        logger.error(f"Error retrieving history: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/reset", methods=["POST"])
def reset_endpoint():
    """Reset conversation."""
    if not chatbot:
        return jsonify({
            "status": "error",
            "message": "Chatbot not initialized"
        }), 400
    
    try:
        chatbot.reset_conversation()
        return jsonify({
            "status": "success",
            "message": "Conversation reset"
        }), 200
        
    except Exception as e:
        logger.error(f"Error resetting conversation: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/stats", methods=["GET"])
def stats_endpoint():
    """Get vector store statistics."""
    if not vector_store:
        return jsonify({
            "status": "error",
            "message": "Vector store not initialized"
        }), 400
    
    try:
        stats = vector_store.get_index_stats()
        return jsonify({
            "status": "success",
            "stats": stats
        }), 200
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}")
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        "status": "error",
        "message": "Endpoint not found"
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    logger.error(f"Internal server error: {error}")
    return jsonify({
        "status": "error",
        "message": "Internal server error"
    }), 500


if __name__ == "__main__":
    logger.info("Starting Nintendo Chatbot Backend API...")
    
    # Check for required environment variables
    if not GOOGLE_API_KEY or not PINECONE_API_KEY:
        logger.error("Missing required environment variables. Please set GOOGLE_API_KEY and PINECONE_API_KEY.")
        exit(1)
    
    # Run Flask app
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=False,
        use_reloader=False
    )
