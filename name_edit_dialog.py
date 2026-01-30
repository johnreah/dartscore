from enum import Enum, auto

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton, QHBoxLayout, QLabel, QGroupBox, \
    QCheckBox

from preferences import Preferences

class DialogResult(Enum):
    OK = auto()
    CANCEL = auto()

class NameEditDialog(QDialog):

    def __init__(self, parent, prefs: Preferences):
        super().__init__(parent = parent)

        self.prefs = prefs
        self.result = None
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)
        # self.setStyleSheet(dialogStyle)

        vLayout = QVBoxLayout(self)

        dbb = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(dbb)
        self.buttonBox.accepted.connect(lambda: self.accept_with_result(DialogResult.OK))
        self.buttonBox.rejected.connect(self.reject)

        vLayout.addWidget(self.buttonBox)

    def accept_with_result(self, result):
        self.result = result
        self.accept()
