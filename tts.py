import logging
import os
import queue
import io
import sys
import threading
import wave
import numpy as np
import sounddevice as sd
import pyttsx3
from PySide6.QtCore import QObject, QTimer, QThread, Signal
from piper import PiperVoice

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

#----------------------------------------------------------------------------
# pyttsx3 co-operative multi-tasking

class TTS(QObject):
    def __init__(self):
        super().__init__()

        self.engine = pyttsx3.init()
        self.engine.connect('started-utterance', self.on_start)
        self.engine.connect('started-word', self.on_word)
        self.engine.connect('finished-utterance', self.on_end)
        self.engine.startLoop(False)

        voices = self.engine.getProperty('voices')
        for v in (voices):
            if v.name == 'Daniel':
                self.engine.setProperty('voice', v.id)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.on_timer)
        self.timer.start(50)

    def on_timer(self):
        self.engine.iterate()

    def on_start(self, name):
        log.debug(f"Starting {name}")

    def on_word(self, name, location, length):
        log.debug(f"Starting {name}, {location}, {length}")

    def on_end(self, name, completed):
        log.debug(f"Ending {name}, {completed}")

    def say(self, text):
        self.engine.say(text)
        log.debug("Ending say()")

    # def closeEvent(self, event): # only for qwindows
    #     self.timer.stop()
    #     self.engine.stop()
    #     self.engine.endLoop()
    #     self.engine = None
    #     super().closeEvent

#----------------------------------------------------------------------------
# pyttsx3 multi-threaded

class TTSThreaded():
    def __init__(self):
        super().__init__()

        self.queue = queue.Queue()
        self.mutex = threading.Lock()

        self.engine = pyttsx3.init()
        self.engine.connect('started-utterance', self.on_start)
        self.engine.connect('started-word', self.on_word)
        self.engine.connect('finished-utterance', self.on_end)

    def say(self, text: str):
        print(f"Putting {text!r} in queue")
        self.queue.put(text)
        print(f"Queue has {self.queue.qsize()} items")

        def _speak_in_thread():
            # while self.queue.qsize() > 0:
            t = self.queue.get()
            log.info(f"Got text from queue: {t!r}")
            self.engine.say(t)
            self.engine.runAndWait()
            self.mutex.release()

        if self.mutex.locked() == False:
            self.mutex.acquire()
            threading.Thread(target=_speak_in_thread, daemon=True).start()

    def stop(self):
        self.engine.stop()

    def on_start(self, name):
        log.info(f"Starting {name}")

    def on_word(self, name, location, length):
        log.info(f"Starting {name}, {location}, {length}")

    def on_end(self, name, completed):
        log.info(f"Ending {name}, {completed}")


class TTSWorker(threading.Thread):
    def __init__(self):
        super().__init__(daemon=True)
        self.q = queue.Queue()
        self._stop_event = threading.Event()
        self.engine = pyttsx3.init()
        # self.engine.setProperty('rate', 145)
        # self.engine.setProperty('voice', ...) # optional

    def say(self, text: str):
        """Non-blocking: just queue the text"""
        log.debug(f"say({text!r})")
        if text:
            self.q.put(text)
        log.debug("queue has {} items".format(self.q.qsize()))

    def stop_current_and_clear(self):
        """Interrupt current speech + discard queue"""
        self.engine.stop()                      # interrupts current utterance
        with self.q.mutex:
            self.q.queue.clear()

    def shutdown(self):
        self._stop_event.set()
        self.q.put(None)                        # sentinel to wake thread

    def run(self):
        while not self._stop_event.is_set():
            try:
                text = self.q.get(timeout=0.3)      # wake periodically to check stop
                log.debug(f"Got text from queue: {text!r}")
                if text is None:
                    break
            except queue.Empty:
                continue

            try:
                self.engine.say(text)
                self.engine.runAndWait()            # blocks THIS thread only → safe
            except RuntimeError as e:
                if "run loop already started" in str(e):
                    print("Caught run loop error → recovering with stop()")
                    self.engine.stop()
                    # Optional: small delay or retry once
                else:
                    raise
            finally:
                self.q.task_done()

        print("TTS worker shutting down")

#----------------------------------------------------------------------------
# piper-tts

class TTSPiper():

    def __init__(self):
        self.thread = QThread()
        self.worker = TTSPiperWorker()
        self.worker.moveToThread(self.thread)
        self.worker.terminated.connect(self.thread.quit)
        self.worker.terminated.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.terminated.connect(lambda: print("TTS worker terminated"))
        self.thread.started.connect(self.worker.run)
        self.thread.start()

    def say(self, text):
        self.worker.queue.put(text)

    def stop(self):
        pass

    def shutdown(self):
        log.debug("requesting interruption")
        self.thread.requestInterruption()
        self.thread.quit()
        self.thread.wait()

class TTSPiperWorker(QObject):
    terminated = Signal()
    error = Signal(str)

    def __init__(self):
        super().__init__()
        self.queue = queue.Queue()

    def run(self):
        try:
            self.voice = PiperVoice.load(os.path.join(os.path.dirname(__file__), "voices/en_GB-alba-medium.onnx"))
            while True:
                text = None
                try:
                    text = self.queue.get(block=True, timeout=0.2)
                except queue.Empty as e:
                    pass

                if QThread.currentThread().isInterruptionRequested():
                    log.debug("Queue get interrupted")
                    self.terminated.emit()
                    return
                elif text is None:
                    continue

                wav_buffer = io.BytesIO()
                with wave.open(wav_buffer, 'wb') as wav_file:
                    wav_file.setnchannels(1)  # Piper outputs mono audio
                    wav_file.setsampwidth(2)  # 16-bit audio
                    wav_file.setframerate(self.voice.config.sample_rate)
                    self.voice.synthesize_wav(text, wav_file)

                wav_buffer.seek(0)

                with wave.open(wav_buffer, 'rb') as wav_file:
                    sample_rate = wav_file.getframerate()
                    frames = wav_file.readframes(wav_file.getnframes())
                    audio_array = np.frombuffer(frames, dtype=np.int16)

                log.debug(f"Playing {len(audio_array)} samples at {sample_rate} Hz...")
                audio_frames = audio_array.reshape(-1, 1)  # (frames, channels) for mono
                with sd.OutputStream(samplerate=sample_rate, channels=1, dtype="int16") as stream:
                    stream.write(audio_frames)
                log.debug("Playback complete!")

        except Exception as e:
            log.error(f"Error in TTS thread: {e}")
            self.error.emit(str(e))
