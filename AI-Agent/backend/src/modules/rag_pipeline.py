"""
RAG (Retrieval-Augmented Generation) pipeline.
Combines Pinecone retrieval with Gemini LLM for question answering.
"""

from google import genai
from typing import List, Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


class ChatbotRAG:
    """RAG pipeline for context-aware chatbot responses."""
    
    def __init__(
        self,
        google_api_key: str,
        vector_store,
        embedder,
        model: str = "gemini-2.5-flash",
        top_k: int = 5,
        max_context_length: int = 2000,
        temperature: float = 0.3
    ):
        """
        Initialize RAG chatbot.
        
        Args:
            google_api_key (str): Google API key
            vector_store: Pinecone vector store instance
            embedder: Gemini embedder instance
            model (str): Gemini model name
            top_k (int): Number of documents to retrieve
            max_context_length (int): Max context chars for LLM
            temperature (float): Generation temperature
        """
        self.client = genai.Client(api_key=google_api_key)
        self.model = model
        self.vector_store = vector_store
        self.embedder = embedder
        self.top_k = top_k
        self.max_context_length = max_context_length
        self.temperature = temperature
        
        self.conversation_history = []
    
    def retrieve_context(self, query: str) -> Tuple[List[Dict[str, Any]], str]:
        """
        Retrieve relevant documents from vector store.
        
        Args:
            query (str): User query
            
        Returns:
            Tuple[List, str]: (retrieved documents, combined context)
        """
        try:
            # Embed the query
            query_embedding = self.embedder.embed_text(query)
            
            if not query_embedding:
                logger.error("Failed to embed query")
                return [], ""
            
            # Retrieve similar documents
            documents = self.vector_store.query_similar(
                embedding=query_embedding,
                top_k=self.top_k,
                include_metadata=True
            )
            
            # Combine context with length limit and include real content
            context_parts = []
            total_length = 0

            for doc in documents:
                meta = doc.get("metadata", {}) or {}
                source = meta.get("url", "unknown")
                title = meta.get("title", "")
                score = doc.get("score", 0)

                # Prefer content from metadata (content preview), with fallbacks
                content = meta.get("content") or doc.get("content", "")
                # Truncate per-document content to keep the overall prompt bounded
                # Slightly larger snippet for better answers, but still conservative
                max_content_len = 800
                if isinstance(content, str) and len(content) > max_content_len:
                    content = content[:max_content_len] + "..."

                entry = f"\n[Score: {score:.2f} | Source: {title or source}]\n"
                entry += f"URL: {source}\n"
                entry += f"Content: {content}\n"

                if total_length + len(entry) <= self.max_context_length:
                    context_parts.append(entry)
                    total_length += len(entry)
                else:
                    # If near the limit, add a truncated tail and stop
                    remaining = max(0, self.max_context_length - total_length)
                    if remaining > 100:
                        context_parts.append(entry[:remaining] + "...\n")
                    break

            combined_context = "".join(context_parts)
            
            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents, combined_context
            
        except Exception as e:
            logger.error(f"Error retrieving context: {e}")
            return [], ""
    
    def generate_response(self, query: str, context: str) -> str:
        """
        Generate LLM response based on query and context.
        
        Args:
            query (str): User query
            context (str): Retrieved context
            
        Returns:
            str: Generated response
        """
        try:
            # Import system prompt
            from src.config.system_prompt import SYSTEM_PROMPT
            
            # Build user message with context
            user_message = f"""Context from Nintendo website:
{context}

User question: {query}

Please answer the question based on the context provided above. Be friendly, helpful, and casual!"""
            
            # Generate response using Gemini with enhanced system instruction, with robust fallbacks
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=[{"role": "user", "parts": [{"text": user_message}]}],
                    system_instruction=SYSTEM_PROMPT,
                    generation_config={"temperature": self.temperature}
                )
            except Exception:
                try:
                    # Fallback: Try with system instruction as part of message
                    full_message = f"{SYSTEM_PROMPT}\n\n{user_message}"
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=full_message
                    )
                except Exception:
                    # Last resort: simple message without system instruction
                    response = self.client.models.generate_content(
                        model=self.model,
                        contents=[{"role": "user", "parts": [{"text": user_message}]}]
                    )

            # Extract text robustly across SDK shapes
            text = None
            if hasattr(response, "text") and response.text:
                text = response.text
            elif isinstance(response, dict):
                # Try common dict shapes
                text = response.get("text")
                if not text:
                    # candidates[0].content.parts[0].text
                    candidates = response.get("candidates") or []
                    if candidates:
                        cand0 = candidates[0] or {}
                        content = cand0.get("content") or {}
                        parts = content.get("parts") or []
                        if parts and isinstance(parts[0], dict):
                            text = parts[0].get("text")

            if text:
                logger.info(f"Generated response for query: {query[:50]}...")
                return text
            else:
                logger.error("No response generated from Gemini")
                return "Sorry, I couldn't generate a response. Please try again. 🎮"
                
        except Exception as e:
            logger.error(f"Error generating response with Gemini: {e}. Using fallback answer.")
            # Fallback: return a concise extractive-style answer
            if not context:
                return (
                    "I'm currently unable to contact the support system. "
                    "But I'm here to help with Nintendo questions! Try again in a moment. 🎮"
                )
            # Provide top context snippets as a helpful response
            snippet = context[:600]
            return (
                "I'm having trouble generating a response right now, but here's what I found that might help:\n\n"
                f"{snippet}\n\n"
                "Try asking again in a moment, or feel free to ask a different question!"
            )
    
    def answer_query(self, query: str) -> Dict[str, Any]:
        """
        Full RAG pipeline: retrieve context and generate response.
        
        Args:
            query (str): User query
            
        Returns:
            Dict: Response with context and answer
        """
        # Add to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": query
        })
        
        # Retrieve context
        documents, context = self.retrieve_context(query)
        
        # Generate response
        response = self.generate_response(query, context)
        
        # Add response to history
        self.conversation_history.append({
            "role": "assistant",
            "content": response
        })
        
        result = {
            "query": query,
            "response": response,
            "context_documents": documents,
            "context_length": len(context),
            "conversation_turn": len(self.conversation_history) // 2
        }
        
        return result
    
    def reset_conversation(self):
        """Clear conversation history."""
        self.conversation_history = []
        logger.info("Conversation history cleared")
    
    def get_conversation_history(self) -> List[Dict[str, str]]:
        """Get full conversation history."""
        return self.conversation_history


def create_rag_chatbot(
    google_api_key: str,
    pinecone_api_key: str,
    pinecone_index_name: str,
    embedder_instance,
    top_k: int = 5,
    temperature: float = 0.3
):
    """
    Convenience function to create a RAG chatbot instance.
    
    Args:
        google_api_key (str): Google API key
        pinecone_api_key (str): Pinecone API key
        pinecone_index_name (str): Pinecone index name
        embedder_instance: Gemini embedder instance
        top_k (int): Number of documents to retrieve
        temperature (float): Generation temperature
        
    Returns:
        ChatbotRAG: Initialized RAG chatbot
    """
    from .pinecone_store import PineconeVectorStore
    
    vector_store = PineconeVectorStore(
        api_key=pinecone_api_key,
        index_name=pinecone_index_name
    )
    
    chatbot = ChatbotRAG(
        google_api_key=google_api_key,
        vector_store=vector_store,
        embedder=embedder_instance,
        top_k=top_k,
        temperature=temperature
    )
    
    return chatbot
