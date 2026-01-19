# AI Chatbot - Quick Start Guide

## Prerequisites
- **Ollama** installed and running (`ollama serve`)
- **Llama2 model** downloaded (`ollama pull llama2`)

## Fastest Way to Run

### Using Docker (Recommended)
```bash
docker-compose up -d
```
Access at: http://localhost:3000

### Using Development Mode
```bash
# Terminal 1: Start Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

# Terminal 2: Start Frontend
cd frontend
npm install
npm start
```
Access at: http://localhost:3000

### Using Helper Script
```bash
./start.sh
```

## Key Features

1. **Chat with Llama AI**: Ask any question
2. **Web Scraping**: Include URLs in your messages for analysis
3. **Context Awareness**: Maintains conversation history
4. **Modern UI**: Beautiful gradient design with animations

## Example Usage

### Ask a Question
```
You: What is machine learning?
```

### Analyze a Webpage
```
You: What is on this page? https://example.com
```

### Multi-turn Conversation
```
You: Explain quantum computing
Assistant: [Response]
You: Can you give me an example?
```

## Troubleshooting

### "Cannot connect to Ollama"
```bash
# Start Ollama
ollama serve

# In another terminal, verify it's running
curl http://localhost:11434/api/tags
```

### Port Already in Use
```bash
# Find what's using the port
lsof -i :5000  # or :3000

# Kill the process or change the port
```

### Fresh Start
```bash
# Docker
docker-compose down
docker-compose up --build -d

# Manual
# Delete venv and node_modules, then reinstall
```

## API Endpoints

- `GET /api/health` - Check server status
- `POST /api/chat` - Send a message
- `POST /api/reset` - Clear conversation history

## Environment Variables

### Backend (.env)
```
OLLAMA_API_URL=http://localhost:11434/api/generate
MODEL_NAME=llama2
FLASK_DEBUG=True  # Development only
```

### Frontend (.env)
```
REACT_APP_API_URL=http://localhost:5000
```

## Common Commands

```bash
# Check Ollama models
ollama list

# Pull a different model
ollama pull llama2:13b

# View logs (Docker)
docker-compose logs -f

# Stop everything (Docker)
docker-compose down

# Rebuild (Docker)
docker-compose up --build
```
