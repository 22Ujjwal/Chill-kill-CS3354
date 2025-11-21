#!/bin/zsh
# backend-run.sh
# Quick start script for Nintendo RAG Chatbot Backend
# Usage: ./backend-run.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_PATH="$SCRIPT_DIR/.venv"

echo ""
echo "🎮 ═══════════════════════════════════════════════════════"
echo "   Nintendo RAG Chatbot Backend - Quick Start"
echo "═══════════════════════════════════════════════════════"
echo ""

# ✅ PRE-FLIGHT CHECKS
echo "📋 Running pre-flight checks..."
echo ""

# Check 1: Python installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found!"
    echo "   Please install Python 3: https://www.python.org/downloads/"
    exit 1
fi
echo "✅ Python 3 found"

# Check 2: venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo ""
    echo "📦 Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
    echo "✅ Virtual environment created"
    echo ""
    echo "📦 Installing dependencies..."
    "$VENV_PATH/bin/pip" install -q -r "$BACKEND_DIR/requirements.txt"
    echo "✅ Dependencies installed"
fi
echo "✅ Virtual environment ready"

# Check 3: Backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found at $BACKEND_DIR"
    exit 1
fi
echo "✅ Backend directory found"

# Check 4: .env file exists
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "❌ .env file not found!"
    echo ""
    echo "📝 Creating .env from template..."
    if [ -f "$BACKEND_DIR/.env.example" ]; then
        cp "$BACKEND_DIR/.env.example" "$BACKEND_DIR/.env"
        echo "✅ .env created from .env.example"
        echo ""
        echo "⚠️  IMPORTANT: Edit $BACKEND_DIR/.env and add your API keys:"
        echo "   - GOOGLE_API_KEY (from Google AI Studio)"
        echo "   - PINECONE_API_KEY (from Pinecone Dashboard)"
        echo "   - FIRECRAWL_API_KEY (from Firecrawl)"
        echo ""
        read -p "Press Enter once you've added your API keys, or Ctrl+C to cancel..."
    else
        echo "❌ .env.example not found. Please create .env manually."
        exit 1
    fi
fi
echo "✅ .env file configured"

# Check 5: API keys present
if grep -q "your_.*_key_here\|^GOOGLE_API_KEY=$\|^PINECONE_API_KEY=$\|^FIRECRAWL_API_KEY=$" "$BACKEND_DIR/.env"; then
    echo "⚠️  WARNING: Placeholder API keys detected in .env"
    echo "   Please update them with real values before continuing."
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi
echo "✅ API keys configured"

echo ""
echo "🚀 All checks passed! Starting backend..."
echo ""

# Start the backend in background
cd "$BACKEND_DIR"
echo "Starting Flask server on port 5002..."
PORT=5002 "$VENV_PATH/bin/python" app.py > /tmp/backend.log 2>&1 &
BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for server to be ready
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is responding
MAX_RETRIES=10
RETRY_COUNT=0
while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://127.0.0.1:5002/api/health > /dev/null 2>&1; then
        echo "✅ Server is responding"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ $RETRY_COUNT -lt $MAX_RETRIES ]; then
        echo "⏳ Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
        sleep 1
    fi
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "❌ Server failed to start"
    echo "📋 Check logs: tail -f /tmp/backend.log"
    kill $BACKEND_PID 2>/dev/null || true
    exit 1
fi

# Initialize the chatbot
echo ""
echo "🤖 Initializing chatbot..."
INIT_RESPONSE=$(curl -s -X POST http://127.0.0.1:5002/api/initialize \
    -H "Content-Type: application/json" \
    -d '{"rebuild":true}')

INIT_STATUS=$(echo "$INIT_RESPONSE" | grep -o '"status":"[^"]*"' | cut -d'"' -f4)
if [ "$INIT_STATUS" = "initialized" ] || [ "$INIT_STATUS" = "already_initialized" ]; then
    echo "✅ Chatbot is ready"
else
    echo "⚠️  Initialization response: $INIT_RESPONSE"
fi

echo ""
echo "🎉 Nintendo Chatbot is now running!"
echo ""
echo "📍 Server: http://127.0.0.1:5002"
echo "💬 Query: http://127.0.0.1:5002/api/query"
echo "🏥 Health: http://127.0.0.1:5002/api/health"
echo "📊 Stats: http://127.0.0.1:5002/api/stats"
echo ""
echo "🧪 Example query:"
echo '  curl -s -X POST http://127.0.0.1:5002/api/query \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"query":"Tell me about Nintendo"}'"'"' | jq '\''.response'\'''
echo ""
echo ""
echo "💬 Or use interactive CLI:"
echo "  cd backend"
echo "  source ../.venv/bin/activate"
echo "  python cli_chat.py"
echo ""
echo "📝 View logs:"
echo "  tail -f /tmp/backend.log"
echo ""
echo "🛑 Stop server: Press CTRL+C"
echo ""

# Keep script running until interrupted
trap "kill $BACKEND_PID 2>/dev/null || true; echo ''; echo '🛑 Backend stopped'; exit 0" SIGINT
wait $BACKEND_PID