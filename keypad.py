import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QGridLayout,
    QPushButton, QLineEdit, QVBoxLayout
)
from PySide6.QtCore import Qt

class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 400)

        # Main widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Display (result/output)
        self.display = QLineEdit("0")
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
        layout.addWidget(self.display)

        # Grid for buttons
        grid = QGridLayout()
        layout.addLayout(grid)

        # Button layout (like a real calculator)
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '−'],
            ['1', '2', '3', '+'],
            ['0', '.', '=', '']
        ]

        # Create buttons and add to grid
        self.button_objects = {}
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                if not text:  # Skip empty cell
                    continue

                btn = QPushButton(text)
                btn.setFixedHeight(60)

                # Style different types of buttons
                if text in '0123456789.':
                    btn.setStyleSheet("QPushButton { font-size: 18px; background-color: #ffffff; }")
                elif text in 'C±%':
                    btn.setStyleSheet("QPushButton { font-size: 18px; color: white; background-color: #ff9500; }")
                elif text in '÷×−+=':
                    btn.setStyleSheet("QPushButton { font-size: 22px; color: white; background-color: #ff5e00; }")
                else:
                    btn.setStyleSheet("QPushButton { font-size: 18px; }")

                # Special case: 0 button spans two columns
                if text == '0':
                    grid.addWidget(btn, row_idx, col_idx, 1, 2)
                else:
                    grid.addWidget(btn, row_idx, col_idx)

                # Connect button click
                btn.clicked.connect(self.on_button_click)
                self.button_objects[text] = btn

        # Make = button span two rows if desired (optional)
        # For now, we keep layout simple

        self.current_input = ""
        self.reset_display = True

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
    calc = Calculator()
    calc.show()
    sys.exit(app.exec())
