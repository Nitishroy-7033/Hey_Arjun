import os
import torch
import sounddevice as sd
import numpy as np
import tempfile
from scipy.io.wavfile import write
from faster_whisper import WhisperModel
from gtts import gTTS
import pygame


# --- 1. Auto-detect best device (GPU or CPU) ---
def get_device():
    if torch.cuda.is_available():
        print("⚡ CUDA GPU detected! Using GPU")
        return "cuda", "float16"
    else:
        print("🐢 No GPU found, using CPU")
        return "cpu", "int8"


# --- 2. Record from microphone ---
def record_audio(seconds=5, samplerate=16000):
    print("🎤 Recording...")
    recording = sd.rec(int(seconds * samplerate),
                       samplerate=samplerate,
                       channels=1,
                       dtype=np.int16)
    sd.wait()
    print("✅ Recording complete")

    # Save temporary file
    tmp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    write(tmp_wav.name, samplerate, recording)
    return tmp_wav.name


# --- 3. Transcribe with faster-whisper ---
def transcribe_audio(file_path, model, beam_size=5):
    print("🔎 Transcribing...")
    segments, info = model.transcribe(file_path,
                                      beam_size=beam_size,
                                      vad_filter=True)

    text = " ".join([segment.text for segment in segments])
    if text.strip():
        print(f"🗣️ You said ({info.language}): {text}")
    else:
        print("❓ No speech detected")

    return text.strip()


# --- 4. Speak back with gTTS ---
def speak_text(text, lang="hi"):
    if not text:
        return
    print(f"🔊 Speaking: {text}")
    tts = gTTS(text=text, lang=lang)
    filename = "temp_response.mp3"
    tts.save(filename)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(filename)


# --- 5. Jarvis main loop ---
def jarvis_loop():
    print("🤖 Jarvis started (Ctrl+C to stop)")

    device, compute_type = get_device()
    model = WhisperModel("small", device=device,
                         compute_type=compute_type,
                         download_root="./models")

    try:
        while True:
            # Step 1: Record (5 sec clip)
            audio_file = record_audio(seconds=5)

            # Step 2: Transcribe
            text = transcribe_audio(audio_file, model)

            # Step 3: Respond
            if text:
                speak_text(f"आपने कहा: {text}", lang="hi")

            os.remove(audio_file)

    except KeyboardInterrupt:
        print("\n👋 Jarvis stopped")


if __name__ == "__main__":
    jarvis_loop()
