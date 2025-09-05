import pyttsx3

def text_to_speech(text, rate=150, volume=2.0):
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)  # Speed of speech
    engine.setProperty('volume', volume)  # Volume (0.0 to 1.0)
    
    voices = engine.getProperty('voices')
    if voices:
        engine.setProperty('voice', voices[0].id)  # type: ignore

    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    text_to_speech("Hello, this is a text to speech test.")
    