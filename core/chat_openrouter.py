import os
import logging
from typing import List, Dict, Optional, Any
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")
DEFAULT_MODEL = "deepseek/deepseek-chat-v3.1:free"
DEFAULT_SYSTEM_PROMPT = """
You are Eva, a friendly Indian AI voice assistant.
- Speak in a natural, conversational desi style — polite, warm, and approachable.
- Keep answers short and clear (1–3 sentences), like you’re talking to a friend.
- Use simple words and avoid over-technical explanations unless the user asks.
- Add a touch of Indian flavor where it feels natural (e.g., “Arre”, “Boss”, “Yaar”, “Namaste”) but don’t overdo it.
- When sharing facts, explain them simply, as if you’re helping someone over chai.
- If you don’t know something, admit it honestly, and suggest a next step (“Maybe check once online?”).
- Always sound supportive, practical, and down-to-earth.
"""


class OpenRouterChat:
    def __init__(self, model: str = DEFAULT_MODEL, system_prompt: str = DEFAULT_SYSTEM_PROMPT):
        """Initialize the OpenRouter chat client.
        
        Args:
            model: The model to use for chat
            system_prompt: The system prompt to use
        """
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables.")
        
        self.model = model
        self.system_prompt = system_prompt
        self.conversation_history: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt}
        ]
        
        try:
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=api_key
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
                return "Oh no!, I can’t access my secret powers. Maybe my magic key went missing?"
            elif "403" in str(e):
                logger.error("Forbidden access - insufficient permissions.")    
                return "Looks like I’m not allowed in this VIP section of the AI club. Mind checking my access pass (API key)?"
            elif "429" in str(e):
                logger.error("Rate limit exceeded.")
                return "Phew! I’ve been talking too much and hit my daily chat limit. Let’s chill for a bit and try again later."
            elif "500" in str(e) or "502" in str(e) or "503" in str(e):
                logger.error("Server error.")
                return "The AI servers are having a coffee break ☕. Let’s give them a minute to wake up."
            elif "timeout" in str(e).lower():
                logger.error("Connection timeout.")
                return "Hello? Hello?? 📞 …ugh, connection dropped. Can you check the internet and try me again?"
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