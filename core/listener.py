import speech_recognition as sr 

def listen_voice():
    recoginizer = sr.Recognizer()
    mic = sr.Microphone()
    recoginizer.pause_threshold = 2
    with mic as source:
        print("Adjusting for ambient noise, please wait...")
        recoginizer.adjust_for_ambient_noise(source,duration=2)
        audio = recoginizer.listen(source)

        while True:
            try:
                print("👂 Jarvis listening...")
                audio = recoginizer.listen(source)  # will stop after 3 sec silence

                # Process speech
                text = recoginizer.recognize_google(audio)  # type: ignore
                print(f"🗣️ You said: {text}")

            except sr.UnknownValueError:
                print("❓ Sorry, I did not understand that.")
            except sr.RequestError:
                print("❗ Could not request results; check your network connection.")
            except KeyboardInterrupt:
                print("\n👋 Stopping Jarvis...")
                break

if __name__ == "__main__":
    listen_voice()
