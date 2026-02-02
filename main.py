import logging
import os
import sys
from collections import namedtuple

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, \
    QGridLayout, QLabel, QListWidgetItem

import score_utils
from keypadbytotal import KeypadByTotal
from name_edit_dialog import NameEditDialog
from preferences import Preferences
from prefs_dialog import DialogResult, PrefsDialog
from tts import TTSPiper

log = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

class AppWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.player_to_throw = None
        self.tts = TTSPiper()
        self.prefs = Preferences()
        self.has_physical_keyboard = has_physical_keyboard()

        #----------------------------------------------------------------------------
        # Prepare resources (fonts, bitmaps, stylesheets) before building main window
        #----------------------------------------------------------------------------
        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), "fonts/7segment.ttf"))
        QFontDatabase.addApplicationFont(os.path.join(os.path.dirname(__file__), "fonts/Chalky.otf"))
        self.ledPixmapOn = QPixmap("images/led-on.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
        self.ledPixmapOff = QPixmap("images/led-off.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
        self.setStyleSheet("font-family: Verdana;")
        stylesheet_player_name = "font-size:36pt;"
        stylesheet_player_score = "font-family: '7-Segment'; font-size:72pt; color: #E31B23; background-color: black;"
        stylesheet_player_score_history = "font-size:18pt; font-family: Chalky; background: #333333; color: white;"
        # stylesheet_tab_widget = "QTabBar::tab { width: 300px; height: 50px; font-size: 18px;}"

        # Paint the background of the main window with a wood effect
        palette = QPalette()
        pixmap = QPixmap("images/wood.jpg")
        brush = QBrush(pixmap)
        palette.setBrush(QPalette.Window, brush)
        self.setPalette(palette)

        #-----------------------------------------------------------------------------
        # Group per-player display elements into an array (dictionary) of named tuples
        #-----------------------------------------------------------------------------

        class TouchLineEdit(QLineEdit):
            name_updated = Signal(int, str)
            _clicked = Signal()

            def __init__(self, parent, player):
                super().__init__()
                self.parent = parent
                self.player = player
                if True: # not parent.has_physical_keyboard:
                    self.setReadOnly(True)
                    self.setFocusPolicy(Qt.FocusPolicy.NoFocus)
                    self._clicked.connect(self.on_clicked)

            def mousePressEvent(self, event):
                self._clicked.emit()
                super().mousePressEvent(event)

            def on_clicked(self):
                dialog = NameEditDialog(self, self.text())
                dialog.name_edit_dialog_ok.connect(self.on_dialog_ok)
                dialog.show()

            def on_dialog_ok(self, str):
                self.name_updated.emit(self.player, str)

        PlayerDisplay = namedtuple("PlayerDisplay", ["name", "score", "led", "history"])
        self.player_displays = {}
        for player in [1, 2]:
            self.player_displays[player] = PlayerDisplay(name = TouchLineEdit(self, player), score = QLineEdit(), led = QLabel(), history = QListWidget())
            self.player_displays[player].name.setStyleSheet(stylesheet_player_name)
            self.player_displays[player].name.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.player_displays[player].name.setFixedHeight(60)
            self.player_displays[player].name.setMinimumWidth(300)
            self.player_displays[player].name.name_updated.connect(self.on_name_updated)

            self.player_displays[player].score.setStyleSheet(stylesheet_player_score)
            self.player_displays[player].score.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.player_displays[player].score.setFixedSize(250, 100)
            self.player_displays[player].score.setReadOnly(True)

            self.player_displays[player].led.setFixedSize(30, 30)
            self.player_displays[player].led.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            self.player_displays[player].history.setItemAlignment(Qt.AlignmentFlag.AlignRight)
            self.player_displays[player].history.setStyleSheet(stylesheet_player_score_history)

        self.player_displays[1].name.setText(self.prefs.players_player1)
        self.player_displays[2].name.setText(self.prefs.players_player2)

        vLayout = QVBoxLayout(self)

        #-------------------
        # Top layout section
        #-------------------
        hLayoutTop = QtWidgets.QHBoxLayout()

        hLayoutTop.addWidget(self.player_displays[1].name)
        hLayoutTop.addWidget(self.player_displays[1].led)
        hLayoutTop.addWidget(self.player_displays[1].score)
        hLayoutTop.addWidget(self.player_displays[2].score)
        hLayoutTop.addWidget(self.player_displays[2].led)
        hLayoutTop.addWidget(self.player_displays[2].name)

        vLayout.addLayout(hLayoutTop)

        #----------------------
        # Middle layout section
        #----------------------
        hLayoutMiddle = QHBoxLayout()

        # TabWidget is to enable multiple input methods. Not needed for MVP.
        # tabWidget = QTabWidget()
        # tabWidget.addTab(keypadbytotal, "By Total")
        # tabWidget.addTab(KeypadByDart(), "By Dart")
        # tabWidget.setStyleSheet(stylesheet_tab_widget)

        self.keypadbytotal = KeypadByTotal(self.prefs)
        self.keypadbytotal.total_entered.connect(lambda total: self.handleScore(total))

        # Use grid layout for a single centred keypad. Replace with TabWidget later.
        keypad_layout = QGridLayout()
        keypad_layout.addWidget(self.keypadbytotal, 0, 0)

        hLayoutMiddle.addWidget(self.player_displays[1].history)
        spacer = QWidget()
        spacer.setFixedWidth(150)
        hLayoutMiddle.addWidget(spacer)
        # hLayoutMiddle.addWidget(tabWidget)
        hLayoutMiddle.addLayout(keypad_layout)
        hLayoutMiddle.addWidget(spacer)
        hLayoutMiddle.addWidget(self.player_displays[2].history)

        vLayout.addLayout(hLayoutMiddle)

        #----------------------
        # Bottom layout section
        #----------------------
        hLayoutBottom = QHBoxLayout()

        self.edStatusBar = QLineEdit()
        self.edStatusBar.setFont(QFont("Verdana", 18))
        self.edStatusBar.setText("This is the status bar")
        self.edStatusBar.setReadOnly(True)
        hLayoutBottom.addWidget(self.edStatusBar)

        btnMenu = QPushButton()
        btnMenu.setText("More...")
        btnMenu.setStyleSheet("QPushButton { font-family: Verdana; font-size: 36px; background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 white, stop: 1 grey); border-style: solid; border-color: #888; border-width: 5px; border-radius: 10px; width: 180px}")
        btnMenu.clicked.connect(lambda: self.on_btnMenu_clicked())
        hLayoutBottom.addWidget(btnMenu)

        vLayout.addLayout(hLayoutBottom)

    def closeEvent(self, event):
        self.tts.shutdown()
        event.accept()

    def reset_scores(self):
        [self.player_displays[player].score.setText("501") for player in [1, 2]]
        [self.player_displays[player].history.clear() for player in [1, 2]]
        [self.appendHistory(player, self.player_displays[player].score.text()) for player in (1, 2)]
        self.setPlayer(1)
        if self.player_to_throw == 1 and self.player_displays[1].score.text() == "501":
            self.edStatusBar.setText("Player 1 to throw. Enter score using keypad and press green Enter button when done.")

    def reset_everything(self):
        self.player_displays[1].name.setText("Player 1")
        self.player_displays[2].name.setText("Player 2")
        self.prefs.players_player1 = "Player 1"
        self.prefs.players_player2 = "Player 2"
        self.reset_scores()
        self.keypadbytotal.reset()

    def appendHistory(self, player_number, itemString):
        item = QListWidgetItem(itemString)
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        self.player_displays[player_number].history.addItem(item)
        self.player_displays[player_number].history.scrollToBottom()

    def setPlayer(self, player_number):
        [self.player_displays[p].led.setPixmap(self.ledPixmapOff) for p in (1, 2)]
        self.player_to_throw = player_number
        self.player_displays[player_number].led.setPixmap(self.ledPixmapOn)
        self.edStatusBar.setText("{} to throw".format(self.player_displays[player_number].name.text()))

    def togglePlayer(self):
        match self.player_to_throw:
            case 1: self.setPlayer(2)
            case 2: self.setPlayer(1)
            case _: raise ValueError("Invalid player number")
        score_remaining = int(self.player_displays[self.player_to_throw].score.text())
        if score_utils.checkout_exists(score_remaining):
            if self.prefs.tts_say_score_required:
                self.tts.say("{} you require {}".format(self.player_displays[self.player_to_throw].name.text(), score_remaining))
            self.edStatusBar.setText("Suggested checkout: " + " or ".join(score_utils.suggested_checkouts(score_remaining)))

    def handleScore(self, score):
        before = int(self.player_displays[self.player_to_throw].score.text())
        after = before - score
        if score_utils.is_valid_score(score) and after >= 0 and after != 1:
            self.player_displays[self.player_to_throw].score.setText(str(after))
            self.appendHistory(self.player_to_throw, "{} - {} = {}".format(before, score, after))
            if self.prefs.tts_say_totals:
                self.tts.say(str(score))
                if after == 0:
                    self.tts.say("Game shot!")
            if after > 0:
                self.togglePlayer()
        else:
            if self.prefs.tts_say_totals:
                self.tts.say("Invalid score")
            self.edStatusBar.setText("Invalid score. Try again.")

    def debugDimensions(self):
        log.debug("window width={} height={}".format(self.width(), self.height()))
        log.debug("ed1.width={}".format(self.player_displays[1].name.width()))
        log.debug("ed2.width={}".format(self.player_displays[2].name.width()))
        log.debug("ed1.height={}".format(self.player_displays[1].name.height()))
        log.debug("ed2.height={}".format(self.player_displays[2].name.height()))

    def on_btnMenu_clicked(self):
        dialog = PrefsDialog(self, self.prefs)
        dialog.accepted.connect(lambda: self.handle_dialog_result(dialog.result))
        dialog.show()

    def handle_dialog_result(self, result):
        match result:
            case DialogResult.OK: log.debug("OK button pressed")
            case DialogResult.NEW_GAME_P1: self.new_game(1)
            case DialogResult.NEW_GAME_P2: self.new_game(2)
            case DialogResult.RESET: self.reset_everything()
            case DialogResult.EXIT: self.close()
            case _: raise ValueError("Invalid dialog result")

    def new_game(self, player_number):
        self.reset_scores()
        self.setPlayer(player_number)

    def on_name_updated(self, player, name):
        self.player_displays[player].name.setText(name)
        match player:
            case 1: self.prefs.players_player1 = name
            case 2: self.prefs.players_player2 = name
            case _: raise ValueError("Invalid player number")

def has_physical_keyboard() -> bool:
    try:
        if not os.path.exists('/dev/input/by-path/'):
            return True  # Not Linux, assume keyboard exists
        kbd_devices = [f for f in os.listdir('/dev/input/by-path/') if 'kbd' in f]
        return True if len(kbd_devices) > 0 else False
    except:
        return True

def main():
    log.debug("starting main()")
    log.debug(os.path.dirname(__file__))

    app = QApplication(sys.argv)
    appWindow = AppWindow()
    appWindow.reset_scores()

    if sys.argv[-1] == "fullscreen":
        log.debug("starting in full-screen (release) mode")
        appWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        appWindow.showFullScreen()
    else:
        log.debug("starting in windowed (debug) mode")
        appWindow.setWindowTitle("Darts Scoreboard")
        # appWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        appWindow.setGeometry(800, 300, 1280, 720)
        appWindow.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
