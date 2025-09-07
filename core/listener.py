# listener.py
import speech_recognition as sr
import socket
import time


recognizer = sr.Recognizer()
mic = sr.Microphone()

def initialize_microphone():
    """Initialize the microphone and adjust for ambient noise."""
    with mic as source:
        print("🎤 Adjusting for ambient noise, please wait...")
        recognizer.adjust_for_ambient_noise(source, duration=2)
    print("✅ Microphone initialized and ready.")



def check_internet_connection():
    """Check if the device is connected to the internet."""
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def listen_voice(retry_attempts=2, retry_delay=2):
    if not check_internet_connection():
        print("❌ No internet connection detected.")
        return "NETWORK_ERROR"

    for attempt in range(retry_attempts + 1):
        with mic as source:
            print("👂 Eva listening...")
            try:
                audio = recognizer.listen(source)  # stops after silence
                text = recognizer.recognize_google(audio) # type: ignore
                print(f"🗣️ You said: {text}")
                return text
            except sr.UnknownValueError:
                print("❓ Sorry, I did not understand that.")
                return ""
            except sr.RequestError:
                if attempt < retry_attempts:
                    print(f"❗ Network error. Retrying in {retry_delay} sec...")
                    time.sleep(retry_delay)
                    continue
                else:
                    return "NETWORK_ERROR"

def listen_for_wake_word(wake_word="eva"):
    with mic as source:
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio).lower()
            print(f"🗣️ Heard: {text}")
            return wake_word in text
        except Exception:
            return False