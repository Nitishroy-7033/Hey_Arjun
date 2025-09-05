from core.listener import listen_voice
from core.text_to_speech import text_to_speech

def main():
    print("🤖 Jarvis started! Speak something... (Ctrl+C to stop)")
    try:
        while True:
            text = listen_voice()   # Get voice as text
            if text:
                text_to_speech(f"You said: {text}")  # Speak back what you said
    except KeyboardInterrupt:
        print("\n👋 Exiting Jarvis...")
        text_to_speech("Goodbye! See you later.")

if __name__ == "__main__":
    main()
