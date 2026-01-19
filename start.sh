#!/bin/bash

# AI Chatbot Startup Script

echo "🚀 Starting AI Chatbot..."
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Warning: Ollama doesn't appear to be running."
    echo "Please start Ollama in a separate terminal with: ollama serve"
    echo ""
fi

# Start backend
echo "Starting backend server..."
cd backend
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -q -r requirements.txt

echo "Backend starting on http://localhost:5000"
python app.py &
BACKEND_PID=$!

cd ..

# Wait a bit for backend to start
sleep 3

# Start frontend
echo ""
echo "Starting frontend server..."
cd frontend

if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    npm install
fi

echo "Frontend starting on http://localhost:3000"
npm start &
FRONTEND_PID=$!

echo ""
echo "✅ AI Chatbot is starting up!"
echo ""
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "To stop the servers, press Ctrl+C or run:"
echo "kill $BACKEND_PID $FRONTEND_PID"
echo ""

# Wait for both processes
wait
