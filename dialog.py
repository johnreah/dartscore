import logging
from enum import Enum, auto

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton, QHBoxLayout, QLabel, QGroupBox, \
    QCheckBox

log = logging.getLogger(__name__)

class DialogResult(Enum):
    OK = auto()
    CANCEL = auto()
    EXIT = auto()
    NEW_GAME_P1 = auto()
    NEW_GAME_P2 = auto()

class Dialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent = parent)
        self.result = None

        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)

        vLayout = QVBoxLayout(self)

        groupBox = QGroupBox()
        groupBox.setTitle("Sound Effects")
        vLayout.addWidget(groupBox)

        groupBoxLayout = QVBoxLayout()
        groupBox.setLayout(groupBoxLayout)
        checkbox1 = QCheckBox("Enable button clicks")
        groupBoxLayout.addWidget(checkbox1)
        checkbox2 = QCheckBox("Enable text-to-speech")
        groupBoxLayout.addWidget(checkbox2)
        checkbox3 = QCheckBox("Announce scores when entered")
        groupBoxLayout.addWidget(checkbox3)
        checkbox4 = QCheckBox('Announce "You require..." when a checkout is available')
        groupBoxLayout.addWidget(checkbox4)

        btnNewGameP1 = QPushButton("New Game Player 1")
        btnNewGameP1.clicked.connect(lambda: self.accept_with_result(DialogResult.NEW_GAME_P1))
        vLayout.addWidget(btnNewGameP1)

        btnNewGameP2 = QPushButton("New Game Player 2")
        btnNewGameP2.clicked.connect(lambda: self.accept_with_result(DialogResult.NEW_GAME_P2))
        vLayout.addWidget(btnNewGameP2)

        btnExit = QPushButton("Exit")
        btnExit.clicked.connect(lambda: self.accept_with_result(DialogResult.EXIT))
        vLayout.addWidget(btnExit)

        dbb = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(dbb)
        self.buttonBox.accepted.connect(lambda: self.accept_with_result(DialogResult.OK))
        self.buttonBox.rejected.connect(self.reject)
        vLayout.addWidget(self.buttonBox)

        groupBox.setStyleSheet("QGroupBox { font-family: Verdana; font-size: 36px; }")
        checkbox1.setStyleSheet("QCheckBox { font-family: Verdana; font-size: 36px; } QCheckBox::indicator {width: 36px; height: 36px; } QCheckBox::indicator:checked {image: url(icons/settings.png); } QCheckBox::indicator:unchecked {image: url(icons/backspace.png); }")
        checkbox2.setStyleSheet("QCheckBox { font-family: Verdana; font-size: 36px; }")
        checkbox3.setStyleSheet("QCheckBox { font-family: Verdana; font-size: 36px; }")
        checkbox4.setStyleSheet("QCheckBox { font-family: Verdana; font-size: 36px; }")
        btnNewGameP1.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        btnNewGameP2.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        btnExit.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        self.buttonBox.setStyleSheet("QWidget { font-family: Verdana; font-size: 48px; }")

        # self.show()
        # self.hide()

    def accept_with_result(self, result):
        self.result = result
        self.accept()
