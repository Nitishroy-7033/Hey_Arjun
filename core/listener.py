# listener.py
import speech_recognition as sr 

def listen_voice():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    recognizer.pause_threshold = 2  # seconds of silence before stopping

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
            print("❗ Could not request results; check your network connection.")
            return ""
