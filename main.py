from core.listener import listen_voice, check_internet_connection
from core.text_to_speech import text_to_speech
from core.chat_openrouter import OpenRouterChat
from router import decide_action
from tools.system_tools import (
    open_app, set_volume, shutdown_computer, cancel_shutdown,
    sleep_computer, create_folder, lock_computer, unlock_computer,
    restart_computer
)
import time
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_api_key():
    """Check if the API key exists and looks valid"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        return False
    
    # Basic format check (OpenRouter keys typically start with sk-or)
    if not api_key.startswith("sk-or"):
        return False
        
    return True

def main():
    # First check if API key seems valid
    if not check_api_key():
        print("❌ API key missing or invalid! Please check your .env file.")
        text_to_speech("I can't start because my API key is missing or invalid. Please check the dot env file.")
        return
        
    try:
        chat = OpenRouterChat()
        print("🤖 Jarvis started! Speak something... (Ctrl+C to stop)")
        text_to_speech("Jarvis is now online and ready to assist you.")
    except ValueError as e:
        print(f"❌ Error initializing Jarvis: {str(e)}")
        text_to_speech("I couldn't start properly. There might be an issue with my API key.")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        text_to_speech("Something went wrong during startup. Please check the logs.")
        return
    
    try:
        while True:
            # Check internet connection first
            if not check_internet_connection():
                print("❌ Internet connection lost. Waiting to reconnect...")
                text_to_speech("Oh nooo! The Wi-Fi ghost stole our internet. Let's wait a bit...")
                
                # Wait for internet to come back
                reconnect_attempts = 0
                while not check_internet_connection() and reconnect_attempts < 2:
                    time.sleep(5)
                    reconnect_attempts += 1
                    print(f"Reconnection attempt {reconnect_attempts}...")
                    text_to_speech(f"Still no luck... trying again, attempt {reconnect_attempts}")
                
                if check_internet_connection():
                    print("✅ Internet connection restored!")
                    text_to_speech("Yesss! The internet genie is back. I'm online again!")
                else:
                    print("❌ Could not reconnect to the internet. Please check your connection and restart Jarvis.")
                    text_to_speech("Hmm… still no internet. Maybe the Wi-Fi went on vacation. Please check it and restart me.")
                    break
                    
            # Get voice input
            text = listen_voice()
            
            # Handle network errors from voice recognition
            if text == "NETWORK_ERROR":
                text_to_speech("Uh oh, I can't hear you properly. Maybe the internet is messing with my ears.")
                continue
                
            if not text:  # Handle empty input
                continue
                
            print(f"🗣️ You said: {text}")
            
            # Handle Route based on intent
            decision = decide_action(chat, text)
            
            if decision["action"] == "tool":
                tool = decision["tool"]
                args = decision.get("arguments", {})
                
                result = "I don't know how to do that yet."
                
                # Route to the appropriate tool
                if tool == "open_app":
                    result = open_app(**args)
                elif tool == "set_volume":
                    result = set_volume(**args)
                elif tool == "shutdown_computer":
                    result = shutdown_computer(**args)
                elif tool == "cancel_shutdown":
                    result = cancel_shutdown()
                elif tool == "sleep_computer":
                    result = sleep_computer()
                elif tool == "create_folder":
                    result = create_folder(**args)
                elif tool == "lock_computer":
                    result = lock_computer()
                elif tool == "unlock_computer":
                    result = unlock_computer(**args)
                elif tool == "restart_computer":
                    result = restart_computer(**args)
                
                print(f"⚡ Tool result: {result}")
                text_to_speech(result)
            
            elif decision["action"] == "chat":
                response = decision["response"]
                print(f"\n🤖 Jarvis: {response}\n")
                text_to_speech(response)

            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Jarvis...")
        text_to_speech("Goodbye! See you later.")

if __name__ == "__main__":
    main()
