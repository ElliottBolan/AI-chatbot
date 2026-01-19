import React, { useState, useRef, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);
  
  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (e) => {
    e.preventDefault();
    
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await fetch(`${API_URL}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response from server');
      }

      const data = await response.json();
      
      const assistantMessage = {
        role: 'assistant',
        content: data.response,
        hasWebContent: data.has_web_content,
        urlsProcessed: data.urls_processed || []
      };
      
      setMessages(prev => [...prev, assistantMessage]);
    } catch (err) {
      const errorMessage = {
        role: 'assistant',
        content: `Error: ${err.message}. Please make sure the backend server is running.`,
        isError: true
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const resetConversation = async () => {
    try {
      await fetch(`${API_URL}/api/reset`, {
        method: 'POST',
      });
      setMessages([]);
    } catch (err) {
      console.error('Failed to reset conversation:', err);
    }
  };

  return (
    <div className="App">
      <div className="chat-container">
        <div className="chat-header">
          <h1>🤖 AI Chatbot</h1>
          <p className="subtitle">Powered by Llama with Web Scraping & Reasoning</p>
          <button onClick={resetConversation} className="reset-btn">
            Reset Conversation
          </button>
        </div>

        <div className="messages-container">
          {messages.length === 0 && (
            <div className="welcome-message">
              <h2>Welcome! 👋</h2>
              <p>I'm an AI chatbot powered by Llama.</p>
              <p>I can help you with:</p>
              <ul>
                <li>Answering questions and providing information</li>
                <li>Web scraping - just include a URL in your message</li>
                <li>Reasoning and analysis</li>
              </ul>
              <p>Try asking me something or share a URL!</p>
            </div>
          )}
          
          {messages.map((msg, index) => (
            <div key={index} className={`message ${msg.role}`}>
              <div className="message-header">
                <span className="message-role">
                  {msg.role === 'user' ? '👤 You' : '🤖 Assistant'}
                </span>
                {msg.hasWebContent && (
                  <span className="web-badge">🌐 Web Content Analyzed</span>
                )}
              </div>
              <div className={`message-content ${msg.isError ? 'error' : ''}`}>
                {msg.content}
              </div>
              {msg.urlsProcessed && msg.urlsProcessed.length > 0 && (
                <div className="urls-processed">
                  <small>URLs processed: {msg.urlsProcessed.join(', ')}</small>
                </div>
              )}
            </div>
          ))}
          
          {isLoading && (
            <div className="message assistant loading">
              <div className="message-header">
                <span className="message-role">🤖 Assistant</span>
              </div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            </div>
          )}
          
          <div ref={messagesEndRef} />
        </div>

        <form onSubmit={sendMessage} className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message or paste a URL..."
            disabled={isLoading}
            className="message-input"
          />
          <button type="submit" disabled={isLoading || !input.trim()} className="send-btn">
            {isLoading ? '⏳' : '📤'} Send
          </button>
        </form>
      </div>
    </div>
  );
}

export default App;
