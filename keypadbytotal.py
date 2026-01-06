import logging
import sys
from enum import Enum, auto

from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QPalette, QColor, QIcon
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
        input = self.display.text()

        if command == KeypadCommand.DIGIT:
            input += payload
        elif command == KeypadCommand.BACKSPACE:
            input = input[:-1]
            if input == "" or int(input) == 0:
                input = "0"
        if command == KeypadCommand.ENTER:
            log.debug("Entered {}".format(input))
            self.total_entered.emit(int(input))
            input = "0"
        self.display.setText(str(int(input)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    keypad = KeypadByTotal()
    keypad.show()
    sys.exit(app.exec())
