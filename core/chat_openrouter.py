import logging
import os
import sys
from typing import List, Dict, Optional, Any

# Add project root to sys.path to allow for package-level imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from openai import OpenAI
from configs.config import Configs
from configs.messages import ErrorMessages

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OpenRouterChat:
    def __init__(self, model: str = Configs.ASSISTANT_MODEL, system_prompt: str = Configs.SYSTEM_PROMPT):
        if not Configs.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")
        
        self.model = model
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]
        
        try:
            self.client = OpenAI(
                base_url=Configs.OPENROUTER_API_URL,
                api_key=Configs.OPENROUTER_API_KEY
            )
            logger.info(f"Initialized OpenRouter client with model: {model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenRouter client: {str(e)}")
            raise

    def chat(self, message: str, stream: bool = False, 
             temperature: float = 0.7, max_tokens: int = 1000) -> str:
        # Add user message to history
        self.conversation_history.append({"role": "user", "content": message})
        
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history, # type: ignore
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream
            ) # type: ignore
            
            if stream:
                # Handle streaming response
                full_response = ""
                for chunk in completion:
                    if chunk.choices and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        full_response += content
                        print(content, end="", flush=True)
                response_text = full_response
            else:
                # Handle regular response
                response_text = completion.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({"role": "assistant", "content": response_text})
            return response_text
            
        except Exception as e:
            error_msg = f"Error during API call: {str(e)}"
            logger.error(error_msg)
            if "401" in str(e):
                logger.error("Unauthorized access - invalid API key.")
                return ErrorMessages.UNAUTHORIZED
            elif "403" in str(e):
                logger.error("Forbidden access - insufficient permissions.")    
                return "Looks like I’m not allowed in this VIP section of the AI club. Mind checking my access pass (API key)?"
            elif "429" in str(e):
                logger.error("Rate limit exceeded.")
                return "Phew! I’ve been talking too much and hit my daily chat limit. Let’s chill for a bit and try again later."
            elif "500" in str(e) or "502" in str(e) or "503" in str(e):
                logger.error("Server error.")
                return ErrorMessages.SERVER_ERROR
            elif "timeout" in str(e).lower():
                logger.error("Connection timeout.")
                return ErrorMessages.TIMEOUT
            else:
                logger.error("An unexpected error occurred.")
                return "Well, that didn’t go as planned 🤦. Let’s pretend this never happened and try again in a moment."



if __name__ == "__main__":
    # Example usage
    chat = OpenRouterChat()
    
    # Single message example
    response = chat.chat("Hello, how are you?")
    print(f"\nAI: {response}")
    
    # Continue conversation with history
    response = chat.chat("Tell me about artificial intelligence.")
    print(f"\nAI: {response}")
    
    # Example with streaming
    print("\nStreaming response:")
    chat.chat("Summarize what we've discussed so far.", stream=True)