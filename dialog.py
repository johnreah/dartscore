import logging
from enum import Enum, auto

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton, QHBoxLayout, QLabel, QGroupBox, \
    QCheckBox

log = logging.getLogger(__name__)

class DialogResult(Enum):
    OK = auto()
    CANCEL = auto()
    NEW_GAME_P1 = auto()
    NEW_GAME_P2 = auto()
    RESET = auto()
    EXIT = auto()

class Dialog(QDialog):

    def __init__(self, parent):
        super().__init__(parent = parent)

        dialogStyle = """
            QWidget {
                font-family: Verdana;
                font-size: 36px;
            }
            QPushButton {
                background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 lightblue);
                border-style: solid;
                border-color: #444;
                border-width: 1px; border-radius: 5px; width: 180px;
            }
            """

        groupBoxStyle = """
            QCheckBox::indicator {
                width: 40px;
                height: 40px;
            }
            QCheckBox::indicator:checked {
                image: url(icons/checkbox-checked.png);
            }
            QCheckBox::indicator:unchecked {
                image: url(icons/checkbox-unchecked.png);
            }
            """

        self.result = None
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet(dialogStyle)

        vLayout = QVBoxLayout(self)

        groupBox = QGroupBox()
        groupBox.setStyleSheet(groupBoxStyle)
        groupBox.style().polish(groupBox) # hack
        groupBox.setTitle("Sound Effects")
        vLayout.addWidget(groupBox)

        groupBoxLayout = QVBoxLayout()
        checkbox1 = QCheckBox("Enable button clicks")
        groupBoxLayout.addWidget(checkbox1)
        checkbox2 = QCheckBox("Enable text-to-speech")
        groupBoxLayout.addWidget(checkbox2)
        checkbox3 = QCheckBox("Announce scores when entered")
        groupBoxLayout.addWidget(checkbox3)
        checkbox4 = QCheckBox('Announce "You require..." when a checkout is available')
        groupBoxLayout.addWidget(checkbox4)
        groupBox.setLayout(groupBoxLayout)

        btnNewGameP1 = QPushButton("New Game Player 1")
        btnNewGameP1.clicked.connect(lambda: self.accept_with_result(DialogResult.NEW_GAME_P1))
        vLayout.addWidget(btnNewGameP1)

        btnNewGameP2 = QPushButton("New Game Player 2")
        btnNewGameP2.clicked.connect(lambda: self.accept_with_result(DialogResult.NEW_GAME_P2))
        vLayout.addWidget(btnNewGameP2)

        btnReset = QPushButton("Reset everything")
        btnReset.clicked.connect(lambda: self.accept_with_result(DialogResult.RESET))
        vLayout.addWidget(btnReset)

        btnExit = QPushButton("Exit")
        btnExit.clicked.connect(lambda: self.accept_with_result(DialogResult.EXIT))
        vLayout.addWidget(btnExit)

        dbb = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self.buttonBox = QDialogButtonBox(dbb)
        self.buttonBox.accepted.connect(lambda: self.accept_with_result(DialogResult.OK))
        self.buttonBox.rejected.connect(self.reject)
        vLayout.addWidget(self.buttonBox)

        # groupBox.setStyleSheet("QGroupBox { font-family: Verdana; font-size: 36px; } QCheckBox { font-family: Verdana; font-size: 36px; } QCheckBox::indicator {width: 40px; height: 40px; } QCheckBox::indicator:checked {image: url(icons/checkbox-checked.png); } QCheckBox::indicator:unchecked {image: url(icons/checkbox-unchecked.png); }")
        # groupBox.style().polish(groupBox) # hack
        # btnNewGameP1.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        # btnNewGameP2.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        # btnExit.setStyleSheet("QPushButton { font-family: Verdana; font-size: 48px; }")
        # self.buttonBox.setStyleSheet("QWidget { font-family: Verdana; font-size: 18px; }")

    def accept_with_result(self, result):
        self.result = result
        self.accept()
