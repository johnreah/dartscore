from enum import Enum, auto

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QDialogButtonBox, QPushButton, QHBoxLayout, QLabel, QGroupBox, \
    QCheckBox

from preferences import Preferences

class DialogResult(Enum):
    OK = auto()
    CANCEL = auto()
    NEW_GAME_P1 = auto()
    NEW_GAME_P2 = auto()
    RESET = auto()
    EXIT = auto()

class PrefsDialog(QDialog):

    def __init__(self, parent, prefs: Preferences):
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
                margin: 10px;
                padding: 10px;
            }
            """

        groupBoxStyle = """
            QGroupBox {
                border: 3px solid lightgrey;
                padding-top: 40px;
            }
            QCheckBox::indicator {
                padding: 10px;
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

        self.prefs = prefs
        self.result = None
        self.setModal(True)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.Dialog)
        self.setStyleSheet(dialogStyle)

        vLayout = QVBoxLayout(self)

        groupBox = QGroupBox()
        groupBox.setStyleSheet(groupBoxStyle)
        groupBox.style().polish(groupBox) # hack for raspberry pi
        groupBox.setTitle("Sound Effects")
        vLayout.addWidget(groupBox)

        groupBoxLayout = QVBoxLayout()

        self.cbSoundButtonClicks = QCheckBox("Enable button clicks")
        self.cbSoundButtonClicks.setChecked(self.prefs.sound_button_clicks)
        groupBoxLayout.addWidget(self.cbSoundButtonClicks)

        # cbTTS = QCheckBox("Enable text-to-speech")
        # cbTTS.setEnabled(False)
        # groupBoxLayout.addWidget(cbTTS)

        self.cbTTSSayTotals = QCheckBox("Announce scores when entered")
        self.cbTTSSayTotals.setChecked(self.prefs.tts_say_totals)
        groupBoxLayout.addWidget(self.cbTTSSayTotals)

        self.cbTTSSayScoreRequired = QCheckBox('Announce "You require..." when a checkout is available')
        self.cbTTSSayScoreRequired.setChecked(self.prefs.tts_say_score_required)
        groupBoxLayout.addWidget(self.cbTTSSayScoreRequired)

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

    def accept_with_result(self, result):
        self.prefs.sound_button_clicks = self.cbSoundButtonClicks.isChecked()
        self.prefs.tts_say_totals = self.cbTTSSayTotals.isChecked()
        self.prefs.tts_say_score_required = self.cbTTSSayScoreRequired.isChecked()
        self.result = result
        self.accept()
