import logging
import sys

import pyttsx3
from PySide6.QtCore import QObject, QTimer

log = logging.getLogger(__name__)

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

