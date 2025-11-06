# Backend - Nintendo RAG Chatbot

This backend is a Flask API that powers a Retrieval-Augmented Generation (RAG) chatbot using:
- Firecrawl (website scraping, with HTTP fallback)
- Google Gemini (LLM + embeddings, with deterministic fallback when quotas are exhausted)
- Pinecone (vector DB)

## Quick start

1) Create and activate the project virtualenv (already configured for this workspace).
2) Ensure `backend/.env` has your keys: `GOOGLE_API_KEY`, `PINECONE_API_KEY`, optionally `FIRECRAWL_API_KEY`.
3) Start the server (port 5002 is recommended on macOS due to conflicts):

```bash
cd backend
PORT=5002 ../../.venv/bin/python app.py
```

In another terminal, initialize the RAG index (scrapes → embeds → upserts):

```bash
curl -sS -X POST http://127.0.0.1:5002/api/initialize -H 'Content-Type: application/json' -d '{"rebuild": true}'
```

Check stats:

```bash
curl -sS http://127.0.0.1:5002/api/stats | jq .
```

## How to send a prompt (3 options)

Option A — cURL:

```bash
curl -sS -X POST http://127.0.0.1:5002/api/query \
  -H 'Content-Type: application/json' \
  -d '{"query": "What are the key tech specs of the Nintendo Switch 2?"}' | jq .
```

Option B — Python snippet:

```python
import requests

BASE_URL = "http://127.0.0.1:5002"

# Initialize once (optional after first start)
requests.post(f"{BASE_URL}/api/initialize", json={"rebuild": False}, timeout=300)

resp = requests.post(
    f"{BASE_URL}/api/query",
    json={"query": "List any tech specs mentioned for Nintendo Switch 2."},
    timeout=60,
)
print(resp.json())
```

Option C — CLI helper (interactive):

```bash
cd backend
../../.venv/bin/python cli_chat.py             # interactive mode
CHATBOT_BASE_URL=http://127.0.0.1:5002 \
  ../../.venv/bin/python cli_chat.py --once "Your question here"
```

Notes:
- If the model quota is exhausted, embeddings/generation fall back gracefully; answers remain grounded to retrieved context but may be less fluent.
- Initialize with `{"rebuild": true}` to clear and re-ingest.
- To reset the conversation state: `POST /api/reset`.

## API endpoints

- POST `/api/initialize` — Initialize backend components and ingest content. Body: `{"rebuild": true|false}`
- POST `/api/query` — Ask a question. Body: `{"query": "..."}`
- GET `/api/history` — Get conversation history
- POST `/api/reset` — Reset conversation history
- GET `/api/health` — Health status
- GET `/api/stats` — Vector DB stats

## Troubleshooting

- Port in use on macOS (e.g., 5000/5001): use another port, e.g., `PORT=5002`.
- 400 INVALID_ARGUMENT on embeddings: now auto-batched (<=100 per request).
- 429 RESOURCE_EXHAUSTED: Gemini quota exceeded. The backend uses a deterministic fallback so the RAG still works; upgrade quota for better quality.
- Firecrawl returns 0 pages: the backend adds specific URLs and has an HTTP fallback to ingest at least a single page.

# Nintendo Chatbot Backend

A Retrieval-Augmented Generation (RAG) chatbot backend that scrapes Nintendo's website, embedds the content, stores it in a vector database, and answers user queries using LLM intelligence.

## Architecture Overview

```
┌─────────────────┐
│  Firecrawl API  │  (Scrape Nintendo website)
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│ Website Documents       │  (Markdown/HTML content)
└────────┬────────────────┘
         │
         ▼
┌──────────────────────┐
│ Gemini Embeddings    │  (Convert text → vectors)
└────────┬─────────────┘
         │
         ▼
┌──────────────────────┐
│ Pinecone Vector DB   │  (Store & retrieve vectors)
└────────┬─────────────┘
         │
         ▼
┌──────────────────────────────┐
│ RAG Pipeline                 │
│ (Retrieve context + LLM)     │
└────────┬─────────────────────┘
         │
         ▼
┌──────────────────────────────┐
│ Flask REST API               │
│ (HTTP endpoints)             │
└──────────────────────────────┘
```

## Components

### 1. **Firecrawl Scraper** (`src/modules/firecrawl_scraper.py`)
- Scrapes Nintendo.com using Firecrawl API
- Extracts markdown and HTML content
- Handles pagination and sitemap
- Returns structured document data

### 2. **Gemini Embedder** (`src/modules/gemini_embedder.py`)
- Converts text to embeddings using Google Gemini API
- Uses `gemini-embedding-001` model
- Handles text chunking for large documents
- Returns 768-dimensional vectors

### 3. **Pinecone Vector Store** (`src/modules/pinecone_store.py`)
- Stores embeddings in Pinecone vector database
- Supports similarity search and retrieval
- Manages metadata (URLs, titles, sources)
- Batch operations for efficiency

### 4. **RAG Pipeline** (`src/modules/rag_pipeline.py`)
- Retrieves relevant documents via semantic search
- Builds context from similar documents
- Generates responses using Gemini LLM
- Maintains conversation history

### 5. **Flask API Server** (`app.py`)
- REST API endpoints for chatbot interaction
- Health checks and initialization
- Query processing and response generation
- Conversation management

## Installation

### Prerequisites
- Python 3.9+
- API keys for: Firecrawl, Google (Gemini), Pinecone

### Setup Steps

1. **Clone the repository:**
```bash
cd backend
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

Required environment variables:
- `FIRECRAWL_API_KEY` - Firecrawl API key
- `GOOGLE_API_KEY` - Google API key for Gemini
- `PINECONE_API_KEY` - Pinecone API key

4. **Verify configuration:**
```bash
python -c "from src.config.settings import *; print('Configuration loaded successfully')"
```

## Usage

### Start the Backend Server

```bash
python app.py
```

The API will start on `http://localhost:5000`

### API Endpoints

#### 1. Health Check
```bash
curl http://localhost:5000/api/health
```

Response:
```json
{
  "status": "healthy",
  "chatbot_ready": false,
  "timestamp": "2025-10-24T12:00:00"
}
```

#### 2. Initialize Backend (Scrape & Index)
```bash
curl -X POST http://localhost:5000/api/initialize
```

This endpoint:
1. Scrapes Nintendo.com (10 pages)
2. Generates embeddings for all documents
3. Stores embeddings in Pinecone
4. Initializes the RAG chatbot

**Warning:** This may take 2-5 minutes depending on document count.

Response:
```json
{
  "status": "initialized",
  "message": "Backend fully initialized and ready",
  "documents_processed": 47,
  "timestamp": "2025-10-24T12:05:00"
}
```

#### 3. Query the Chatbot
```bash
curl -X POST http://localhost:5000/api/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the Nintendo Switch 2?"}'
```

Response:
```json
{
  "status": "success",
  "query": "What is the Nintendo Switch 2?",
  "response": "Based on Nintendo's website, the Switch 2 is...",
  "context_documents_count": 5,
  "context_length": 1847,
  "turn": 1,
  "timestamp": "2025-10-24T12:06:00"
}
```

#### 4. Get Conversation History
```bash
curl http://localhost:5000/api/history
```

Response:
```json
{
  "status": "success",
  "history": [
    {"role": "user", "content": "What is the Nintendo Switch 2?"},
    {"role": "assistant", "content": "Based on Nintendo's website..."},
    ...
  ],
  "turns": 5
}
```

#### 5. Reset Conversation
```bash
curl -X POST http://localhost:5000/api/reset
```

#### 6. Get Vector Store Statistics
```bash
curl http://localhost:5000/api/stats
```

## Configuration

Edit `src/config/settings.py` to customize:

```python
# Website crawling
TARGET_WEBSITE_URL = "https://www.nintendo.com/us/"
CRAWL_LIMIT = 10

# RAG behavior
TOP_K_RESULTS = 5  # Number of documents to retrieve
MAX_CONTEXT_LENGTH = 2000  # Max context chars
TEMPERATURE = 0.3  # LLM generation temperature

# Models
GEMINI_MODEL_NAME = "gemini-2.5-flash"
GEMINI_EMBEDDING_MODEL = "gemini-embedding-001"
```

## Workflow

### Data Ingestion Pipeline

1. **Scrape**: Firecrawl extracts content from Nintendo.com
2. **Embed**: Gemini converts documents to vector embeddings
3. **Store**: Pinecone indexes the vectors with metadata

### Query Processing Pipeline

1. **Embed**: Convert user query to embedding
2. **Retrieve**: Find similar documents in Pinecone
3. **Augment**: Build context from retrieved documents
4. **Generate**: Gemini LLM generates response with context

## Project Structure

```
backend/
├── app.py                          # Main Flask API server
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment variables template
├── README.md                       # This file
├── src/
│   ├── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py             # Configuration & environment
│   └── modules/
│       ├── __init__.py
│       ├── firecrawl_scraper.py    # Website scraping
│       ├── gemini_embedder.py      # Text embeddings
│       ├── pinecone_store.py       # Vector database
│       └── rag_pipeline.py         # RAG & LLM integration
└── tests/
    └── (test files)
```

## Troubleshooting

### Issue: "Failed to scrape website"
- Verify Firecrawl API key is correct
- Check internet connectivity
- Ensure target URL is accessible

### Issue: "Failed to embed documents"
- Verify Google API key is valid
- Check Gemini API limits
- Ensure documents have content

### Issue: "Pinecone connection error"
- Verify Pinecone API key and environment
- Check index name matches configuration
- Ensure index exists in Pinecone console

### Issue: "Chatbot not initialized"
- Call `/api/initialize` endpoint first
- Wait for initialization to complete
- Check server logs for errors

## Performance Optimization

- **Batch embeddings**: Pinecone upserts vectors in batches of 100
- **Chunked documents**: Large documents split into chunks
- **Cached results**: Firecrawl caches content for 48 hours
- **Top-K retrieval**: Only retrieve most relevant documents

## Security

- ✅ API keys stored in `.env` (not committed)
- ✅ CORS enabled for frontend communication
- ✅ Input validation on all endpoints
- ✅ Error handling without exposing internals

## Future Enhancements

- [ ] User authentication
- [ ] Rate limiting
- [ ] Caching layer (Redis)
- [ ] Async processing (Celery)
- [ ] Webhook support
- [ ] Custom document upload
- [ ] Multi-language support
- [ ] Analytics dashboard

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.0 | Web framework |
| requests | 2.31.0 | HTTP client |
| google-genai | 0.3.0 | Gemini API |
| pinecone-client | 3.0.0 | Vector database |
| python-dotenv | 1.0.0 | Environment config |
| Flask-CORS | 4.0.0 | Cross-origin support |

## Support & Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check logs:
```bash
# View live logs
tail -f backend.log

# Search for errors
grep "ERROR" backend.log
```

## License

This project is part of the Nintendo Chatbot Assistant for CS3354.
