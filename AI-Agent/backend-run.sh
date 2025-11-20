#!/bin/zsh
# backend-run.sh
# Quick start script for Nintendo RAG Chatbot Backend
# Usage: ./backend-run.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
VENV_PATH="$SCRIPT_DIR/.venv"

echo "🚀 Starting Nintendo Chatbot Backend..."
echo ""

# Check if venv exists
if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Virtual environment not found at $VENV_PATH"
    echo "Please set up the venv first with: python3 -m venv .venv"
    exit 1
fi

# Check if backend directory exists
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Backend directory not found at $BACKEND_DIR"
    exit 1
fi

# Check if .env exists
if [ ! -f "$BACKEND_DIR/.env" ]; then
    echo "❌ .env file not found at $BACKEND_DIR/.env"
    echo "Please create it with your API keys"
    exit 1
fi

# Start the backend in background
cd "$BACKEND_DIR"
echo "Starting Flask server on port 5002..."

# Try Windows path first, then Unix path
if [ -f "$VENV_PATH/Scripts/python.exe" ]; then
    PORT=5002 "$VENV_PATH/Scripts/python.exe" app.py > /tmp/backend.log 2>&1 &
else
    PORT=5002 "$VENV_PATH/bin/python" app.py > /tmp/backend.log 2>&1 &
fi

BACKEND_PID=$!
echo "✅ Backend started (PID: $BACKEND_PID)"
echo ""

# Wait for server to be ready
echo "⏳ Waiting for server to start..."
sleep 5

echo "✅ Server started successfully"
echo ""

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
echo "💬 Query endpoint: http://127.0.0.1:5002/api/query"
echo "📊 Stats endpoint: http://127.0.0.1:5002/api/stats"
echo "🏥 Health endpoint: http://127.0.0.1:5002/api/health"
echo ""
echo "Example query:"
echo '  curl -X POST http://127.0.0.1:5002/api/query \'
echo '    -H "Content-Type: application/json" \'
echo '    -d '"'"'{"query":"Tell me about Nintendo","top_k":5}'"'"
echo ""
echo "Press CTRL+C to stop the server"
echo ""

# Keep script running until interrupted
trap "kill $BACKEND_PID 2>/dev/null || true; echo 'Backend stopped'; exit 0" SIGINT
wait $BACKEND_PID
