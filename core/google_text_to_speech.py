from gtts import gTTS
import pygame
import os

def google_text_to_speech(text, lang="hi"):
    tts = gTTS(text=text, lang=lang, slow=False)
    filename = "temp_voice.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    # Wait until audio finishes
    while pygame.mixer.music.get_busy():
        continue

    pygame.mixer.quit()
    os.remove(filename)

if __name__ == "__main__":
    google_text_to_speech("Mai nitish kumar bol raha hoon, aap kaise hain?", lang="hi")
