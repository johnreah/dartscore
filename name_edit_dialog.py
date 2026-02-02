from enum import Enum, auto

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton, QHBoxLayout, QLabel, QGroupBox, \
    QCheckBox, QLineEdit, QSizePolicy

from preferences import Preferences
from virtual_keyboard import VirtualKeyboard


class DialogResult(Enum):
    OK = auto()
    CANCEL = auto()

class NameEditDialog(QDialog):

    name_edit_dialog_ok = Signal(str)

    def __init__(self, parent, name: str):
        super().__init__(parent = parent)

        self.name = name
        self.result = None
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)
        # self.setStyleSheet(dialogStyle)

        vLayout = QVBoxLayout(self)

        self.edName = QLineEdit(self.name, self)
        self.edName.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.edName.setReadOnly(False)
        self.edName.setFixedHeight(60)
        self.edName.setStyleSheet("""
            QLineEdit {
                font-size: 24px;
                padding: 10px;
                background-color: #f0f0f0;
                border: 2px solid #ccc;
        """)
        vLayout.addWidget(self.edName)

        dbb = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(dbb)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.accepted.connect(lambda: self.name_edit_dialog_ok.emit(self.edName.text()))

        vLayout.addWidget(self.buttonBox)

        self.edName.selectAll()

    # def accept_with_result(self, result):
    #     self.result = result
    #     self.accept()
