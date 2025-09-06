from core.listener import listen_voice, check_internet_connection
from core.text_to_speech import text_to_speech
from core.chat_openrouter import OpenRouterChat
import time

def main():
    chat = OpenRouterChat()
    print("🤖 Jarvis started! Speak something... (Ctrl+C to stop)")
    
    try:
        while True:
            # Check internet connection first
            if not check_internet_connection():
                print("❌ Internet connection lost. Waiting to reconnect...")
                text_to_speech("Oh nooo! The Wi-Fi ghost stole our internet. Let’s wait a bit...")
                
                # Wait for internet to come back
                reconnect_attempts = 0
                while not check_internet_connection() and reconnect_attempts < 2:
                    time.sleep(5)
                    reconnect_attempts += 1
                    print(f"Reconnection attempt {reconnect_attempts}...")
                    text_to_speech("Still no luck... trying again, attempt {reconnect_attempts}")
                
                if check_internet_connection():
                    print("✅ Internet connection restored!")
                    text_to_speech("Yesss! The internet genie is back. I’m online again!")
                else:
                    print("❌ Could not reconnect to the internet. Please check your connection and restart Jarvis.")
                    text_to_speech("Hmm… still no internet. Maybe the Wi-Fi went on vacation. Please check it and restart me.")
                    break
                    
            # Get voice input
            text = listen_voice()
            
            # Handle network errors from voice recognition
            if text == "NETWORK_ERROR":
                text_to_speech("Uh oh, I can’t hear you properly. Maybe the internet is messing with my ears.")
                continue
                
            # Process regular input
            if text:
                try:
                    response = chat.chat(text, True)
                    print(f"\n🤖 Jarvis: {response}\n")
                    text_to_speech(response)
                except Exception as e:
                    print(f"Error communicating with AI service: {str(e)}")
                    text_to_speech("My brain froze… maybe the internet tripped over a cable. Let’s try again in a bit.")
            
            time.sleep(0.5)  # Short pause between cycles
            
    except KeyboardInterrupt:
        print("\n👋 Exiting Jarvis...")
        text_to_speech("Goodbye! See you later.")

if __name__ == "__main__":
    main()
