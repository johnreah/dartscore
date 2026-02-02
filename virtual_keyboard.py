from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Signal, Qt


class VirtualKeyboard(QWidget):
    """A virtual QWERTY keyboard widget"""

    key_pressed = Signal(str)  # Emits the character/key pressed

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shift_active = False
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)

        # Define keyboard rows
        self.keys = [
            ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'],
            ['Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'],
            ['Space']
        ]

        self.key_buttons = {}

        # Row 1
        row1_layout = QHBoxLayout()
        row1_layout.setSpacing(5)
        for key in self.keys[0]:
            btn = self.create_key_button(key)
            if key == 'Backspace':
                btn.setMinimumWidth(100)
            row1_layout.addWidget(btn)
            self.key_buttons[key] = btn
        main_layout.addLayout(row1_layout)

        # Row 2
        row2_layout = QHBoxLayout()
        row2_layout.setSpacing(5)
        row2_layout.addSpacing(20)  # Slight indent
        for key in self.keys[1]:
            btn = self.create_key_button(key)
            row2_layout.addWidget(btn)
            self.key_buttons[key] = btn
        main_layout.addLayout(row2_layout)

        # Row 3
        row3_layout = QHBoxLayout()
        row3_layout.setSpacing(5)
        row3_layout.addSpacing(40)  # More indent
        for key in self.keys[2]:
            btn = self.create_key_button(key)
            if key == 'Enter':
                btn.setMinimumWidth(80)
            row3_layout.addWidget(btn)
            self.key_buttons[key] = btn
        main_layout.addLayout(row3_layout)

        # Row 4
        row4_layout = QHBoxLayout()
        row4_layout.setSpacing(5)
        for key in self.keys[3]:
            btn = self.create_key_button(key)
            if key == 'Shift':
                btn.setMinimumWidth(80)
            row4_layout.addWidget(btn)
            self.key_buttons[key] = btn
        main_layout.addLayout(row4_layout)

        # Row 5 (Space bar)
        row5_layout = QHBoxLayout()
        row5_layout.setSpacing(5)
        row5_layout.addSpacing(100)
        for key in self.keys[4]:
            btn = self.create_key_button(key)
            btn.setMinimumWidth(400)
            row5_layout.addWidget(btn)
            self.key_buttons[key] = btn
        row5_layout.addSpacing(100)
        main_layout.addLayout(row5_layout)

    def create_key_button(self, key_text):
        """Create a button for a keyboard key"""
        btn = QPushButton(key_text)
        btn.setMinimumSize(50, 50)
        btn.setStyleSheet("""
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border: 2px solid #999;
            }
        """)
        btn.clicked.connect(lambda: self.handle_key_press(key_text))
        return btn

    def handle_key_press(self, key):
        """Handle a key press"""
        if key == 'Shift':
            self.shift_active = not self.shift_active
            self.update_shift_state()
        elif key == 'Backspace':
            self.key_pressed.emit('\b')  # Backspace character
        elif key == 'Enter':
            self.key_pressed.emit('\n')  # Newline character
        elif key == 'Space':
            self.key_pressed.emit(' ')
        else:
            # Handle regular characters
            char = key if self.shift_active else key.lower()
            self.key_pressed.emit(char)
            # Auto-reset shift after character
            if self.shift_active:
                self.shift_active = False
                self.update_shift_state()

    def update_shift_state(self):
        """Update the visual state of shift keys"""
        shift_style_active = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #4CAF50;
                color: white;
                border: 2px solid #45a049;
                border-radius: 5px;
            }
        """
        shift_style_normal = """
            QPushButton {
                font-size: 16px;
                font-weight: bold;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
                border-radius: 5px;
            }
            QPushButton:pressed {
                background-color: #d0d0d0;
                border: 2px solid #999;
            }
        """

        # Update all letter keys
        for row in self.keys[1:4]:  # Letter rows
            for key in row:
                if key not in ['Shift', 'Enter', 'Backspace'] and key.isalpha():
                    self.key_buttons[key].setText(key if self.shift_active else key.lower())

        # Update shift key appearance
        style = shift_style_active if self.shift_active else shift_style_normal
        self.key_buttons['Shift'].setStyleSheet(style)

