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

        # self.setFixedWidth(800)
        # self.setFixedHeight(300)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor("lightblue"))
        self.setPalette(palette)

        # vBoxLayout = QVBoxLayout(self)

        # Display (result/output)
        self.display = QLineEdit("0", self)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(60)
        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
            }
        """)

        hpad = 10
        vpad = 10
        w = 100
        h = 100
        dispw = 400
        disph = 60

        # vBoxLayout.addWidget(self.display)
        self.display.setGeometry(hpad, vpad, dispw, disph)

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
        self.create_button("7", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 0, disph + h * 0, w, h)
        self.create_button("8", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 1, disph + h * 0, w, h)
        self.create_button("9", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 2, disph + h * 0, w, h)

        self.create_button("4", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 0, disph + h * 1, w, h)
        self.create_button("5", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 1, disph + h * 1, w, h)
        self.create_button("6", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 2, disph + h * 1, w, h)

        self.create_button("1", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 0, disph + h * 2, w, h)
        self.create_button("2", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 1, disph + h * 2, w, h)
        self.create_button("3", KeypadCommand.DIGIT, btn_stylesheet, hpad + w * 2, disph + h * 2, w, h)

        self.create_button("0", KeypadCommand.DIGIT, btn_stylesheet_3x1, hpad + w * 0, disph + h * 3, w * 3, h)
        self.create_button("", KeypadCommand.BACKSPACE, btn_stylesheet_1x2_red, hpad + w * 3, disph + h * 0, w, h * 2, "icons/backspace.png")
        self.create_button("", KeypadCommand.ENTER, btn_stylesheet_1x2_green, hpad + w * 3, disph + h * 2, w, h * 2, "icons/enter.png")

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

        # if text == 'C':
        #     self.current_input = ""
        #     self.display.setText("0")
        #     self.reset_display = True
        #
        # elif text == '±':
        #     if self.current_input:
        #         if self.current_input[0] == '-':
        #             self.current_input = self.current_input[1:]
        #         else:
        #             self.current_input = '-' + self.current_input
        #         self.display.setText(self.current_input)
        #
        # elif text == '%':
        #     try:
        #         value = float(self.current_input) / 100
        #         self.current_input = str(value)
        #         self.display.setText(self.current_input)
        #     except:
        #         self.display.setText("Error")
        #
        # elif text in '÷×−+':
        #     if self.current_input:
        #         self.current_input += {'÷': '/', '×': '*', '−': '-', '+': '+'}.get(text, text)
        #         self.reset_display = True
        #
        # elif text == '=':
        #     try:
        #         result = eval(self.current_input)  # Note: eval is simple here; for production use safer parsing
        #         self.current_input = str(result)
        #         self.display.setText(self.current_input)
        #         self.reset_display = True
        #     except:
        #         self.display.setText("Error")
        #         self.current_input = ""
        #
        # else:  # Numbers and decimal point
        #     if self.reset_display:
        #         self.current_input = text
        #         self.reset_display = False
        #     else:
        #         self.current_input += text
        #     self.display.setText(self.current_input if self.current_input else "0")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = KeypadByTotal()
    calc.show()
    sys.exit(app.exec())
