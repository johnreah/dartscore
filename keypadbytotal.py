import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton
)


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

        btn7 = QPushButton("7", self)
        btn7.setGeometry(hpad * 1 + w * 0, disph + 2 * vpad, w, h)
        btna = QPushButton("a", self)
        btna.setGeometry(hpad * 2 + w * 1, disph + 2 * vpad, w, h)
        btnb = QPushButton("b", self)
        btnb.setGeometry(hpad * 3 + w * 2, disph + 2 * vpad, w, h)
        btnc = QPushButton("c", self)
        btnc.setGeometry(hpad * 4 + w * 3, disph + 2 * vpad, w, h)

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

    # def create_button(self, text, styleSheet, row, col, rowspan = 1, colspan = 1, fixedWidth = 100, fixedHeight = 100, icon = ''):
    #     button = QPushButton(text)
    #     button.setStyleSheet(styleSheet)
    #     self.gridLayout.addWidget(button, row, col, rowspan, colspan)
    #     button.clicked.connect(self.on_button_click)
    #     if colspan == 1:
    #         button.setFixedWidth(fixedWidth)
    #     button.setFixedHeight(fixedHeight)
    #     if icon != '':
    #         button.setIcon(QIcon(icon))
    #         button.setIconSize(QSize(40, 40))
    #     return button

    def on_button_click(self):
        btn = self.sender()
        text = btn.text()

        if text == 'C':
            self.current_input = ""
            self.display.setText("0")
            self.reset_display = True

        elif text == '±':
            if self.current_input:
                if self.current_input[0] == '-':
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.display.setText(self.current_input)

        elif text == '%':
            try:
                value = float(self.current_input) / 100
                self.current_input = str(value)
                self.display.setText(self.current_input)
            except:
                self.display.setText("Error")

        elif text in '÷×−+':
            if self.current_input:
                self.current_input += {'÷': '/', '×': '*', '−': '-', '+': '+'}.get(text, text)
                self.reset_display = True

        elif text == '=':
            try:
                result = eval(self.current_input)  # Note: eval is simple here; for production use safer parsing
                self.current_input = str(result)
                self.display.setText(self.current_input)
                self.reset_display = True
            except:
                self.display.setText("Error")
                self.current_input = ""

        else:  # Numbers and decimal point
            if self.reset_display:
                self.current_input = text
                self.reset_display = False
            else:
                self.current_input += text
            self.display.setText(self.current_input if self.current_input else "0")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calc = KeypadByTotal()
    calc.show()
    sys.exit(app.exec())
