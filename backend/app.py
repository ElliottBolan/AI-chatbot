from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import json
import os
from typing import List, Dict
import re

app = Flask(__name__)
CORS(app)

# Configuration
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434/api/generate')
MODEL_NAME = os.getenv('MODEL_NAME', 'llama2')

class ChatBot:
    def __init__(self):
        self.conversation_history = []
    
    def scrape_web(self, url: str) -> str:
        """Scrape content from a web URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style", "nav", "footer", "header"]):
                script.decompose()
            
            # Get text
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return text[:5000]  # Limit to first 5000 characters
        except Exception as e:
            return f"Error scraping URL: {str(e)}"
    
    def detect_urls(self, message: str) -> List[str]:
        """Detect URLs in the message"""
        url_pattern = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
        return re.findall(url_pattern, message)
    
    def reason_with_llama(self, prompt: str, context: str = "") -> str:
        """Use Llama model for reasoning"""
        try:
            full_prompt = f"{context}\n\n{prompt}" if context else prompt
            
            payload = {
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            }
            
            response = requests.post(OLLAMA_API_URL, json=payload, timeout=60)
            response.raise_for_status()
            
            result = response.json()
            return result.get('response', 'No response from model')
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Please ensure Ollama is running (run 'ollama serve' in terminal)."
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def process_message(self, message: str) -> Dict:
        """Process incoming message with reasoning and web scraping"""
        # Detect URLs in the message
        urls = self.detect_urls(message)
        
        scraped_content = ""
        if urls:
            scraped_content = "\n\n".join([
                f"Content from {url}:\n{self.scrape_web(url)}" 
                for url in urls
            ])
        
        # Add to conversation history
        self.conversation_history.append({"role": "user", "content": message})
        
        # Build context from conversation history
        context = "\n".join([
            f"{msg['role']}: {msg['content']}" 
            for msg in self.conversation_history[-5:]  # Last 5 messages
        ])
        
        # Create enhanced prompt with scraped content
        if scraped_content:
            enhanced_prompt = f"""Based on the following web content and the user's question, provide a helpful and accurate response.

Web Content:
{scraped_content}

User Question: {message}

Please analyze the information and provide a comprehensive answer."""
        else:
            enhanced_prompt = message
        
        # Get response from Llama
        response = self.reason_with_llama(enhanced_prompt, context if not scraped_content else "")
        
        # Add to conversation history
        self.conversation_history.append({"role": "assistant", "content": response})
        
        return {
            "response": response,
            "urls_processed": urls,
            "has_web_content": bool(scraped_content)
        }

# Global chatbot instance
chatbot = ChatBot()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "model": MODEL_NAME})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "No message provided"}), 400
    
    message = data['message']
    result = chatbot.process_message(message)
    
    return jsonify(result)

@app.route('/api/reset', methods=['POST'])
def reset_conversation():
    """Reset conversation history"""
    global chatbot
    chatbot = ChatBot()
    return jsonify({"status": "conversation reset"})

if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() in ('true', '1', 'yes')
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
