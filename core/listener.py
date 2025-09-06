# listener.py
import speech_recognition as sr
import socket
import time

def check_internet_connection():
    """Check if the device is connected to the internet."""
    try:
        # Try to connect to Google's DNS server
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def listen_voice(retry_attempts=2, retry_delay=2):
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    recognizer.pause_threshold = 2  # seconds of silence before stopping

    # First check internet connection
    if not check_internet_connection():
        print("❌ No internet connection detected. Speech recognition requires internet.")
        return "NETWORK_ERROR"

    for attempt in range(retry_attempts + 1):
        with mic as source:
            print("🎤 Adjusting for ambient noise, please wait...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("👂 Jarvis listening...")

            try:
                audio = recognizer.listen(source)  # stops after 2 sec silence
                text = recognizer.recognize_google(audio)  # type: ignore
                print(f"🗣️ You said: {text}")
                return text
            except sr.UnknownValueError:
                print("❓ Sorry, I did not understand that.")
                return ""
            except sr.RequestError:
                if attempt < retry_attempts:
                    print(f"❗ Network error. Retrying in {retry_delay} seconds... (Attempt {attempt+1}/{retry_attempts})")
                    time.sleep(retry_delay)
                    continue
                else:
                    print("❗ Could not connect to Google Speech Recognition service. Check your internet connection.")
                    return "NETWORK_ERROR"
