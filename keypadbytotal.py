import logging
import sys
import os
import random
from enum import Enum, auto

import pyttsx3

from PySide6.QtCore import Qt, QSize, Signal, QUrl
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtMultimedia import QSoundEffect
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QSizePolicy
)

log = logging.getLogger(__name__)

class KeypadCommand(Enum):
    DIGIT = auto()
    BACKSPACE = auto()
    ENTER = auto()

class KeypadByTotal(QWidget):
    total_entered = Signal(int)

    def __init__(self):
        super().__init__()

        HPAD = 10
        VPAD = 10
        W = 100
        H = 100
        DISPH = 60

        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setFixedWidth(HPAD * 2 + W * 4)
        self.setFixedHeight(VPAD * 3 + DISPH + H * 4)

        # Initialize multiple sound effects for button clicks (for variety)
        self.click_sounds = []
        sounds_dir = os.path.join(os.path.dirname(__file__), "sounds")
        
        # Load all 10 key samples
        for i in range(1, 11):
            sound_effect = QSoundEffect()
            sound_path = os.path.join(sounds_dir, f"key_sample_{i}.wav")
            if os.path.exists(sound_path):
                sound_effect.setSource(QUrl.fromLocalFile(sound_path))
                sound_effect.setVolume(0.6)
                self.click_sounds.append(sound_effect)
        
        log.debug(f"Loaded {len(self.click_sounds)} key sound samples")
        
        # Initialize text-to-speech engine (cross-platform)
        try:
            self.tts_engine = pyttsx3.init()
            # Set properties for British-sounding voice
            voices = self.tts_engine.getProperty('voices')
            # Try to find a British English voice
            for voice in voices:
                if 'en_GB' in voice.id or 'english-uk' in voice.id.lower() or 'daniel' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    log.debug(f"Using voice: {voice.name}")
                    break
            # Set speech rate (slightly slower for clarity)
            self.tts_engine.setProperty('rate', 150)
        except Exception as e:
            log.warning(f"Failed to initialize TTS engine: {e}")
            self.tts_engine = None

        # Paint background blue - handy when experimenting with layouts
        # self.setAutoFillBackground(True)
        # palette = self.palette()
        # palette.setColor(QPalette.ColorRole.Window, QColor("lightblue"))
        # self.setPalette(palette)

        # Display (result/output)
        self.display = QLineEdit("0", self)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(DISPH)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
            }
        """)

        self.display.setGeometry(HPAD, VPAD, self.width() - 2 * HPAD, 20)

        btn_stylesheet = (
            "QPushButton { border-image: url(images/btn.png); font-size: 36px; padding-bottom: 10px; } "
            "QPushButton:pressed { border-image: url(images/btn-pressed.png); padding-bottom: 2px; padding-left: 2px; }"
        )
        btn_stylesheet_3x1 = (
            "QPushButton { border-image: url(images/btn3x1.png); font-size: 36px; padding-bottom: 10px; } "
            "QPushButton:pressed { border-image: url(images/btn3x1-pressed.png); padding-bottom: 2px; padding-left: 2px; }"
        )
        btn_stylesheet_1x2_red = (
            "QPushButton { border-image: url(images/btn1x2-red.png); font-size: 36px; padding-bottom: 10px; } "
            "QPushButton:pressed { border-image: url(images/btn1x2-red-pressed.png); padding-bottom: 2px; padding-left: 2px; }"
        )
        btn_stylesheet_1x2_green = (
            "QPushButton { border-image: url(images/btn1x2-green.png); font-size: 36px; padding-bottom: 10px; } "
            "QPushButton:pressed { border-image: url(images/btn1x2-green-pressed.png); padding-bottom: 2px; padding-left: 2px; }"
        )
        self.create_button("7", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 0, VPAD * 2 + DISPH + H * 0, W, H)
        self.create_button("8", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 1, VPAD * 2 + DISPH + H * 0, W, H)
        self.create_button("9", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 2, VPAD * 2 + DISPH + H * 0, W, H)

        self.create_button("4", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 0, VPAD * 2 + DISPH + H * 1, W, H)
        self.create_button("5", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 1, VPAD * 2 + DISPH + H * 1, W, H)
        self.create_button("6", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 2, VPAD * 2 + DISPH + H * 1, W, H)

        self.create_button("1", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 0, VPAD * 2 + DISPH + H * 2, W, H)
        self.create_button("2", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 1, VPAD * 2 + DISPH + H * 2, W, H)
        self.create_button("3", KeypadCommand.DIGIT, btn_stylesheet, HPAD + W * 2, VPAD * 2 + DISPH + H * 2, W, H)

        self.create_button("0", KeypadCommand.DIGIT, btn_stylesheet_3x1, HPAD + W * 0, VPAD * 2 + DISPH + H * 3, W * 3, H)
        self.create_button("", KeypadCommand.BACKSPACE, btn_stylesheet_1x2_red, HPAD + W * 3, VPAD * 2 + DISPH + H * 0, W, H * 2, "icons/backspace.png")
        self.create_button("", KeypadCommand.ENTER, btn_stylesheet_1x2_green, HPAD + W * 3, VPAD * 2 + DISPH + H * 2, W, H * 2, "icons/enter.png")

    def create_button(self, text, command, styleSheet, x, y, w, h, icon = None):
        button = QPushButton(text, self)
        button.setStyleSheet(styleSheet)
        button.setGeometry(x, y, w, h)
        command_payload = text if text.isdigit() else None
        button.clicked.connect(lambda: self.on_button_click(command, command_payload))
        if icon is not None:
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(40, 40))
        return button

    def on_button_click(self, command, payload = None):
        log.debug("Command={} payload={}".format(command, payload))
        
        # Play random click sound for all button presses (adds variety)
        if self.click_sounds:
            random.choice(self.click_sounds).play()
        
        input = self.display.text()
        if command == KeypadCommand.DIGIT:
            input += payload
        elif command == KeypadCommand.BACKSPACE:
            input = input[:-1]
            if input == "" or int(input) == 0:
                input = "0"
        if command == KeypadCommand.ENTER:
            log.debug("Entered {}".format(input))
            score_value = int(input)
            self.total_entered.emit(score_value)
            # Speak the score out loud using macOS text-to-speech
            self.speak_score(score_value)
            input = "0"
        self.display.setText(str(int(input)))
    
    def speak_score(self, score):
        """Use cross-platform text-to-speech to announce the score"""
        if self.tts_engine:
            try:
                # Speak the score in a separate thread to avoid blocking
                self.tts_engine.say(str(score))
                self.tts_engine.runAndWait()
            except Exception as e:
                log.warning("Failed to speak score: {}".format(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    keypad = KeypadByTotal()
    keypad.show()
    sys.exit(app.exec())
