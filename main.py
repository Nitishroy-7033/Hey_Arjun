from core.listener import listen_voice, check_internet_connection, listen_for_wake_word
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
        print("🤖 Eva started! Say 'Eva' to activate... (Ctrl+C to stop)")
        text_to_speech("Eva is now online and ready to assist you. Just say Eva to activate me.")
    except ValueError as e:
        print(f"❌ Error initializing Eva: {str(e)}")
        text_to_speech("I couldn't start properly. There might be an issue with my API key.")
        return
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        text_to_speech("Something went wrong during startup. Please check the logs.")
        return
    
    try:
        while True:
            # Listen for wake word
            if listen_for_wake_word(wake_word="eva"):
                text_to_speech("Yes, I'm listening")
                
                # Check internet connection
                if not check_internet_connection():
                    print("❌ Internet connection lost. Waiting to reconnect...")
                    text_to_speech("Oh no! The Wi-Fi ghost stole our internet. Let's wait a bit...")
                    time.sleep(5)
                    continue
                        
                # Get voice input
                text = listen_voice()
                
                # Handle network errors from voice recognition
                if text == "NETWORK_ERROR":
                    text_to_speech("I'm having trouble connecting to the internet. Please check your connection.")
                    time.sleep(5)
                    continue
                    
                if not text:
                    text_to_speech("I didn't catch that. Please try again.")
                    continue
                
                print(f"🗣️ You said: {text}")
                
                # Handle Route based on intent
                decision = decide_action(chat, text)
                
                if decision["action"] == "tool":
                    tool_name = decision.get("tool")
                    arguments = decision.get("arguments", {})
                    
                    print(f"🔧 Using tool: {tool_name} with args: {arguments}")
                    
                    try:
                        if tool_name == "open_app":
                            open_app(arguments.get("app_name"))
                        elif tool_name == "set_volume":
                            set_volume(arguments.get("level"))
                        elif tool_name == "shutdown_computer":
                            shutdown_computer(arguments.get("delay_seconds", 60))
                        elif tool_name == "cancel_shutdown":
                            cancel_shutdown()
                        elif tool_name == "sleep_computer":
                            sleep_computer()
                        elif tool_name == "create_folder":
                            create_folder(arguments.get("folder_name"), arguments.get("path"))
                        elif tool_name == "lock_computer":
                            lock_computer()
                        elif tool_name == "unlock_computer":
                            unlock_computer(arguments.get("password"))
                        elif tool_name == "restart_computer":
                            restart_computer(arguments.get("delay_seconds", 60))
                        else:
                            text_to_speech(f"I don't know how to use the tool {tool_name}.")
                            
                    except Exception as e:
                        print(f"❌ Tool execution error: {str(e)}")
                        text_to_speech(f"I encountered an error while using {tool_name}. {str(e)}")
                
                elif decision["action"] == "chat":
                    response = decision.get("response", "I'm not sure how to respond to that.")
                    print(f"🤖 Eva: {response}")
                    text_to_speech(response)

                time.sleep(0.5)
                
            time.sleep(0.1)  # Small delay to prevent high CPU usage
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Eva...")
        text_to_speech("Goodbye! See you later.")

if __name__ == "__main__":
    main()
