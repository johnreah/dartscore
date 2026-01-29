import os
import wave
from threading import Thread

import numpy as np
import sounddevice as sd

def playsound(filename: str):
    Thread(target=_playsound, args=(filename,)).start()

def _playsound(filename: str):
    path = os.path.join(os.path.dirname(__file__), "sounds")
    path = os.path.join(path, filename)

    with wave.open(path, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        frames = wav_file.readframes(wav_file.getnframes())
        audio_array = np.frombuffer(frames, dtype=np.int16)

    audio_frames = audio_array.reshape(-1, 1)  # (frames, channels) for mono
    with sd.OutputStream(samplerate=sample_rate, channels=1, dtype="int16") as stream:
        stream.write(audio_frames)
