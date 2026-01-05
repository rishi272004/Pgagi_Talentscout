"""
LLM Client Module
Handles interactions with various LLM providers (OpenAI, Ollama, etc.)
"""

import os
import json
from typing import Optional, List, Dict
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """Base class for LLM interactions"""

    def __init__(self, provider: Optional[str] = None):
        """
        Initialize LLM Client
        
        Args:
            provider: LLM provider type ('openai', 'ollama', or None for default)
        """
        self.provider = provider or os.getenv('LLM_PROVIDER', 'ollama')
        self.model = self._get_model()
        self.client = self._initialize_client()

    def _get_model(self) -> str:
        """Get the model name based on provider"""
        if self.provider == 'openai':
            return 'gpt-3.5-turbo'
        elif self.provider == 'ollama':
            return os.getenv('OLLAMA_MODEL', 'mistral')
        return 'gpt-3.5-turbo'

    def _initialize_client(self):
        """Initialize the appropriate LLM client"""
        if self.provider == 'openai':
            try:
                from openai import OpenAI
                api_key = os.getenv('OPENAI_API_KEY')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY not set in environment")
                return OpenAI(api_key=api_key)
            except ImportError:
                raise ImportError("OpenAI package not installed. Install with: pip install openai")
        elif self.provider == 'ollama':
            return None  # Ollama uses HTTP API
        return None

    def generate_response(self, prompt: str, system_message: Optional[str] = None, 
                         temperature: float = 0.7, max_tokens: int = 500) -> str:
        """
        Generate response from LLM
        
        Args:
            prompt: User prompt
            system_message: System context message
            temperature: Response creativity (0.0-1.0)
            max_tokens: Maximum response length
            
        Returns:
            Generated response text
        """
        if self.provider == 'openai':
            return self._openai_response(prompt, system_message, temperature, max_tokens)
        elif self.provider == 'ollama':
            return self._ollama_response(prompt, system_message, temperature, max_tokens)
        else:
            return self._fallback_response(prompt)

    def _openai_response(self, prompt: str, system_message: Optional[str] = None,
                        temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate response using OpenAI API"""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _ollama_response(self, prompt: str, system_message: Optional[str] = None,
                        temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Generate response using Ollama API"""
        import requests
        
        try:
            full_prompt = prompt
            if system_message:
                full_prompt = f"{system_message}\n\n{prompt}"

            response = requests.post(
                'http://localhost:11434/api/generate',
                json={
                    'model': self.model,
                    'prompt': full_prompt,
                    'temperature': temperature,
                    'num_predict': max_tokens,
                    'stream': False
                },
                timeout=60
            )
            
            if response.status_code == 200:
                return response.json().get('response', '').strip()
            else:
                return "Error: Unable to connect to Ollama. Make sure Ollama is running on localhost:11434"
        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Please ensure Ollama is installed and running."
        except Exception as e:
            return f"Error generating response: {str(e)}"

    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when LLM provider is unavailable"""
        return f"I'm currently unable to process your request. Please ensure the LLM provider is configured correctly."


class ConversationManager:
    """Manages multi-turn conversations with context"""

    def __init__(self, llm_client: LLMClient, system_prompt: str):
        """
        Initialize Conversation Manager
        
        Args:
            llm_client: Initialized LLM client
            system_prompt: System-level instructions for the conversation
        """
        self.llm_client = llm_client
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str):
        """Add message to conversation history"""
        self.conversation_history.append({"role": role, "content": content})

    def get_response(self, user_input: str, temperature: float = 0.7) -> str:
        """
        Get LLM response based on conversation history
        
        Args:
            user_input: Current user input
            temperature: Response creativity
            
        Returns:
            LLM generated response
        """
        self.add_message("user", user_input)
        
        # Format conversation history as context
        context = self._format_context()
        response = self.llm_client.generate_response(
            prompt=context + user_input,
            system_message=self.system_prompt,
            temperature=temperature
        )
        
        self.add_message("assistant", response)
        return response

    def _format_context(self) -> str:
        """Format conversation history for context"""
        if not self.conversation_history:
            return ""
        
        context = "Previous conversation:\n"
        for msg in self.conversation_history[:-1]:  # Exclude the last message (current user input)
            role = "You" if msg['role'] == "user" else "Assistant"
            context += f"{role}: {msg['content']}\n"
        
        return context

    def clear_history(self):
        """Clear conversation history"""
        self.conversation_history = []

    def get_history(self) -> List[Dict[str, str]]:
        """Get conversation history"""
        return self.conversation_history
