# AI Chatbot

An intelligent chatbot application powered by Llama AI with web scraping and reasoning capabilities, featuring a modern React frontend.

## Features

- 🤖 **AI-Powered Conversations**: Uses Llama language model for intelligent responses
- 🌐 **Web Scraping**: Automatically extracts and analyzes content from URLs shared in conversations
- 🧠 **Reasoning**: Advanced reasoning capabilities for complex queries
- 💬 **Modern Chat Interface**: Clean and responsive React-based UI
- 🔄 **Conversation History**: Maintains context across messages
- ⚡ **Real-time Responses**: Fast and efficient message processing

## Architecture

The project consists of two main components:

### Backend (Python/Flask)
- Flask REST API server
- Llama integration via Ollama
- Web scraping with BeautifulSoup
- CORS enabled for frontend communication

### Frontend (React)
- Modern React application
- Real-time chat interface
- Responsive design
- Loading states and error handling

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8+** (for backend)
- **Node.js 14+** and npm (for frontend)
- **Ollama** (for Llama model)

### Installing Ollama

1. Install Ollama from [https://ollama.ai](https://ollama.ai)
2. Pull the Llama2 model:
   ```bash
   ollama pull llama2
   ```
3. Start Ollama service:
   ```bash
   ollama serve
   ```

## Installation

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Start the backend server:
   ```bash
   python app.py
   ```

The backend server will run on `http://localhost:5000`

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

The frontend will run on `http://localhost:3000`

## Usage

1. Make sure Ollama is running (`ollama serve`)
2. Start the backend server (port 5000)
3. Start the frontend development server (port 3000)
4. Open your browser to `http://localhost:3000`
5. Start chatting! You can:
   - Ask questions
   - Share URLs for the bot to analyze
   - Have contextual conversations

### Example Prompts

- "What is machine learning?"
- "Analyze this article: https://example.com/article"
- "Explain quantum computing in simple terms"
- "Compare these two pages: https://site1.com and https://site2.com"

## Configuration

### Backend Environment Variables

You can customize the backend by setting these environment variables:

- `OLLAMA_API_URL`: Ollama API endpoint (default: `http://localhost:11434/api/generate`)
- `MODEL_NAME`: Llama model to use (default: `llama2`)

Example:
```bash
export MODEL_NAME=llama2:13b
export OLLAMA_API_URL=http://localhost:11434/api/generate
```

### Frontend Environment Variables

Create a `.env` file in the frontend directory:

```
REACT_APP_API_URL=http://localhost:5000
```

## API Endpoints

### Health Check
```
GET /api/health
```
Returns the health status and model name.

### Chat
```
POST /api/chat
Content-Type: application/json

{
  "message": "Your message here"
}
```

Returns:
```json
{
  "response": "AI response",
  "urls_processed": ["url1", "url2"],
  "has_web_content": true
}
```

### Reset Conversation
```
POST /api/reset
```
Clears the conversation history.

## Project Structure

```
AI-chatbot/
├── backend/
│   ├── app.py              # Flask application
│   ├── requirements.txt    # Python dependencies
│   └── .gitignore
├── frontend/
│   ├── public/            # Static files
│   ├── src/
│   │   ├── App.js         # Main React component
│   │   ├── App.css        # Styles
│   │   └── index.js       # Entry point
│   ├── package.json       # Node dependencies
│   └── .gitignore
└── README.md
```

## Technologies Used

### Backend
- **Flask**: Web framework
- **Ollama**: Llama model integration
- **BeautifulSoup4**: Web scraping
- **Requests**: HTTP library
- **Flask-CORS**: Cross-origin resource sharing

### Frontend
- **React**: UI library
- **Modern CSS**: Gradient designs and animations
- **Fetch API**: Backend communication

## Troubleshooting

### Backend Issues

**Error: Cannot connect to Ollama**
- Make sure Ollama is running: `ollama serve`
- Check if the model is installed: `ollama list`
- Pull the model if needed: `ollama pull llama2`

**Port 5000 already in use**
- Change the port in `app.py`: `app.run(port=5001)`
- Update frontend API URL accordingly

### Frontend Issues

**Cannot connect to backend**
- Verify backend is running on port 5000
- Check CORS settings
- Ensure `REACT_APP_API_URL` is set correctly

**Blank page after npm start**
- Check browser console for errors
- Clear browser cache
- Delete `node_modules` and run `npm install` again

## Development

### Running Tests
```bash
# Backend tests (if available)
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

Frontend:
```bash
cd frontend
npm run build
```

The build folder will contain optimized production files.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Future Enhancements

- [ ] User authentication
- [ ] Conversation persistence (database)
- [ ] Multiple conversation threads
- [ ] File upload support
- [ ] Voice input/output
- [ ] Markdown rendering in messages
- [ ] Export conversation history
- [ ] Custom model selection in UI
- [ ] Rate limiting and caching
- [ ] Docker containerization

## Support

For issues and questions, please open an issue on the GitHub repository.
