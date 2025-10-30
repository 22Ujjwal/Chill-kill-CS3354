"""
Configuration and settings for the chatbot backend.
Load API keys and environment variables here.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===== API Keys & Credentials =====
# Do NOT provide defaults for secret keys. They must come from environment/.env
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")  # Set this in .env
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")  # Set this in .env
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1")  # Adjust if needed

# ===== Models & Services =====
FIRECRAWL_BASE_URL = "https://api.firecrawl.dev/v2"
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "nintendo-chatbot")
PINECONE_NAMESPACE = os.getenv("PINECONE_NAMESPACE", "default")

# ===== Website Configuration =====
TARGET_WEBSITE_URL = "https://www.nintendo.com/us/"
CRAWL_LIMIT = 10
INCLUDE_SITEMAP = True
CRAWL_ENTIRE_DOMAIN = False

# ===== Embedding Configuration =====
EMBEDDING_DIMENSION = 1024  # Pinecone index configured for 1024-dim vectors

# ===== RAG Configuration =====
TOP_K_RESULTS = 5  # Number of documents to retrieve for context
MAX_CONTEXT_LENGTH = 2000  # Max chars of context to send to LLM
TEMPERATURE = 0.3  # Gemini generation temperature
