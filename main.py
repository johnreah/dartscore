import logging
import os
import sys
from collections import namedtuple

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QSize, QPoint
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush, QIcon, QCursor
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QListWidget, QGridLayout, QMainWindow, QLabel, QListWidgetItem, QMenu

from keypadbytotal import KeypadByTotal

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    player_to_throw = None

    def __init__(self):
        super().__init__()

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
        PlayerDisplay = namedtuple("PlayerDisplay", ["name", "score", "led", "history"])
        self.player_displays = {}
        for player in [1, 2]:
            self.player_displays[player] = PlayerDisplay(name = QLineEdit(), score = QLineEdit(), led = QLabel(), history = QListWidget())
            self.player_displays[player].name.setStyleSheet(stylesheet_player_name)
            self.player_displays[player].name.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.player_displays[player].name.setFixedHeight(60)
            self.player_displays[player].name.setMinimumWidth(300)
            self.player_displays[player].name.setText("Player {}".format(player))

            self.player_displays[player].score.setStyleSheet(stylesheet_player_score)
            self.player_displays[player].score.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
            self.player_displays[player].score.setFixedSize(250, 100)
            self.player_displays[player].score.setReadOnly(True)

            self.player_displays[player].led.setFixedSize(30, 30)
            self.player_displays[player].led.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)

            self.player_displays[player].history.setItemAlignment(Qt.AlignmentFlag.AlignRight)
            self.player_displays[player].history.setStyleSheet(stylesheet_player_score_history)

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

        keypadbytotal = KeypadByTotal()
        keypadbytotal.total_entered.connect(lambda total: self.handleScore(total))

        # Use grid layout for a single centred keypad. Replace with TabWidget later.
        keypad_layout = QGridLayout()
        keypad_layout.addWidget(keypadbytotal, 0, 0)

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
        btnMenu.setIcon(QIcon("icons/settings.png"))
        btnMenu.setIconSize(QSize(60, 60))

        self.menu = QMenu()
        self.menu.addAction("Reset", self.reset)
        self.menu.addAction("Exit", self.close)

        self.menu.show() # This is a hack that doesn't work everywhere
        h = self.menu.sizeHint()
        self.menu.hide()
        btnMenu.clicked.connect(lambda: self.menu.popup(QPoint(QCursor.pos().x() - h.width(), QCursor.pos().y() - h.height())))
        btnMenu.setStyleSheet("border-style: inset")
        hLayoutBottom.addWidget(btnMenu)

        vLayout.addLayout(hLayoutBottom)


    def reset(self):
        [self.player_displays[player].score.setText("501") for player in [1, 2]]
        [self.player_displays[player].history.clear() for player in [1, 2]]
        [self.appendHistory(player, self.player_displays[player].score.text()) for player in (1, 2)]
        self.setPlayer(1)
        if self.player_to_throw == 1 and self.player_displays[1].score.text() == "501":
            self.edStatusBar.setText("Player 1 to throw. Enter score using keypad and press green Enter button when done.")

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

    def handleScore(self, score):
        self.debugDimensions()
        before = int(self.player_displays[self.player_to_throw].score.text())
        after = before - score
        self.player_displays[self.player_to_throw].score.setText(str(after))
        self.appendHistory(self.player_to_throw, "{} - {} = {}".format(before, score, after))
        self.togglePlayer()

    def debugDimensions(self):
        log.debug("window width={} height={}".format(self.width(), self.height()))
        log.debug("ed1.width={}".format(self.player_displays[1].name.width()))
        log.debug("ed2.width={}".format(self.player_displays[2].name.width()))
        log.debug("ed1.height={}".format(self.player_displays[1].name.height()))
        log.debug("ed2.height={}".format(self.player_displays[2].name.height()))

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.debug("starting main()")
    log.debug(os.path.dirname(__file__))

    app = QApplication(sys.argv)
    appWindow = AppWindow()
    appWindow.reset()

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
