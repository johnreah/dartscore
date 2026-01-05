import logging
import sys

from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QPalette, QColor, QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton, QSizePolicy
)

log = logging.getLogger(__name__)

class KeypadByTotal(QWidget):
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
        self.display = QLineEdit(self, "0")
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
        btn_stylesheet_1x2 = (
            "QPushButton { border-image: url(images/btn1x2.png); font-size: 36px; padding-bottom: 10px; } "
            "QPushButton:pressed { border-image: url(images/btn1x2-pressed.png); padding-bottom: 2px; padding-left: 2px; }"
        )
        btn7 = self.create_button("7", btn_stylesheet, hpad + w * 0, disph + h * 0, w, h)
        btn8 = self.create_button("8", btn_stylesheet, hpad + w * 1, disph + h * 0, w, h)
        btn9 = self.create_button("9", btn_stylesheet, hpad + w * 2, disph + h * 0, w, h)

        btn4 = self.create_button("4", btn_stylesheet, hpad + w * 0, disph + h * 1, w, h)
        btn5 = self.create_button("5", btn_stylesheet, hpad + w * 1, disph + h * 1, w, h)
        btn6 = self.create_button("6", btn_stylesheet, hpad + w * 2, disph + h * 1, w, h)

        btn1 = self.create_button("1", btn_stylesheet, hpad + w * 0, disph + h * 2, w, h)
        btn2 = self.create_button("2", btn_stylesheet, hpad + w * 1, disph + h * 2, w, h)
        btn3 = self.create_button("3", btn_stylesheet, hpad + w * 2, disph + h * 2, w, h)

        btn0 = self.create_button("0", btn_stylesheet_3x1, hpad + w * 0, disph + h * 3, w * 3, h)
        btn_backspace = self.create_button("", btn_stylesheet_1x2, hpad + w * 3, disph + h * 0, w, h * 2, "icons/backspace.png")
        btn_enter = self.create_button("", btn_stylesheet_1x2, hpad + w * 3, disph + h * 2, w, h * 2, "icons/enter.png")
        # btna = QPushButton("a", self)
        # btna.setGeometry(hpad + w * 1, disph, w, h)
        # btna.setStyleSheet(btn_stylesheet)
        #
        # btnb = QPushButton("b", self)
        # btnb.setGeometry(hpad + w * 2, disph, w, h)
        # btnb.setStyleSheet(btn_stylesheet)
        #
        # btn4 = self.create_button("4", btn_stylesheet, hpad + w * 0, disph + h, w, h)

        # btnc = QPushButton("", self)
        # btnc.setGeometry(hpad + w * 3, disph, w, h)
        # btnc.setStyleSheet(btn_stylesheet)
        # btnc.setIcon(QIcon("icons/backspace.png"))
        # btnc.setIconSize(QSize(40, 40))

        # btn7.setStyleSheet("QPushButton:pressed { border-image: url(images/btn7.png); font-size: 36px; }")
            # "QPushButton:hover { border-image: url(images/btn7.png); }"
            # "QPushButton:pressed { border-image: url(images/btn7.png); }"
            # "QPushButton:disabled { border-image: url(images/btn7.png); }"

        # Grid for buttons
        # self.gridLayout = QGridLayout()
        # vBoxLayout.addLayout(self.gridLayout)
        #
        # styleDigit = "font-family: Verdana; font-size: 36px; background-color: #ffffff;"
        # styleBackspace = "background-color: #ee4444;"
        # styleEnter = "background-color: #44cc44;"
        #
        # btn7 = self.create_button('7', styleDigit, 0, 0)
        # btn8 = self.create_button('8', styleDigit, 0, 1)
        # btn9 = self.create_button('9', styleDigit, 0, 2)
        # btn4 = self.create_button('4', styleDigit, 1, 0)
        # btn5 = self.create_button('5', styleDigit, 1, 1)
        # btn6 = self.create_button('6', styleDigit, 1, 2)
        # btn1 = self.create_button('1', styleDigit, 2, 0)
        # btn2 = self.create_button('2', styleDigit, 2, 1)
        # btn3 = self.create_button('3', styleDigit, 2, 2)
        # btn0 = self.create_button('0', styleDigit, 3, 0, colspan=3)
        # self.btnBackspace = self.create_button('', styleBackspace, 0, 3, rowspan = 2, fixedHeight = 200, icon = "icons/backspace.png")
        # self.btnEnter = self.create_button('', styleEnter, 2, 3, rowspan = 2, fixedHeight = 200, icon = "icons/enter.png")
        #
        # self.current_input = ""
        # self.reset_display = True

    def create_button(self, text, styleSheet, x, y, w, h, icon = ""):
        button = QPushButton(text, self)
        button.setStyleSheet(styleSheet)
        button.setGeometry(x, y, w, h)
        button.clicked.connect(self.on_button_click)
        if icon != "":
            button.setIcon(QIcon(icon))
            button.setIconSize(QSize(40, 40))
        return button

    def on_button_click(self):
        btn = self.sender()
        text = btn.text()
        log.debug(text)

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
