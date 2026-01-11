import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QListWidget, QGridLayout, QMainWindow, QLabel, QListWidgetItem

from keypadbytotal import KeypadByTotal

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    player_to_throw = None

    def __init__(self):
        super().__init__()

        QFontDatabase.addApplicationFont("fonts/7segment.ttf")
        QFontDatabase.addApplicationFont("fonts/Chalky.otf")
        self.setStyleSheet("font-family: Verdana;")
        stylesheet_player_name = "font-size:36pt;"
        stylesheet_player_score = "font-family: '7-Segment'; font-size:72pt; color: #E31B23; background-color: black;"
        stylesheet_player_score_history = "font-size:18pt; font-family: Chalky; background: #333333; color: white;"
        # stylesheet_tab_widget = "QTabBar::tab { width: 300px; height: 50px; font-size: 18px;}"

        vLayout = QVBoxLayout(self)

        hLayoutTop = QtWidgets.QHBoxLayout()

        self.edPlayer1 = QLineEdit()
        self.edPlayer1.setStyleSheet(stylesheet_player_name)
        self.edPlayer1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edPlayer1.setFixedHeight(60)
        self.edPlayer1.setMinimumWidth(300)
        self.edPlayer1.setText("Player 1")

        self.edPlayer2 = QLineEdit()
        self.edPlayer2.setStyleSheet(stylesheet_player_name)
        self.edPlayer2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edPlayer2.setFixedHeight(60)
        self.edPlayer2.setMinimumWidth(300)
        self.edPlayer2.setText("Player 2")

        self.edScore1 = QLineEdit()
        self.edScore1.setStyleSheet(stylesheet_player_score)
        self.edScore1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edScore1.setFixedSize(250, 100)
        self.edScore1.setReadOnly(True)

        self.edScore2 = QLineEdit()
        self.edScore2.setStyleSheet(stylesheet_player_score)
        self.edScore2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edScore2.setFixedSize(250, 100)
        self.edScore2.setReadOnly(True)

        self.ledPixmapOn = QPixmap("images/led-on.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)
        self.ledPixmapOff = QPixmap("images/led-off.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio)

        self.led1 = QLabel()
        self.led1.setFixedSize(30, 30)
        self.led1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.led1.setPixmap(self.ledPixmapOn)

        self.led2 = QLabel()
        self.led2.setFixedSize(30, 30)
        self.led2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.led2.setPixmap(self.ledPixmapOff)

        hLayoutTop.addWidget(self.edPlayer1)
        hLayoutTop.addWidget(self.led1)
        hLayoutTop.addWidget(self.edScore1)
        hLayoutTop.addWidget(self.edScore2)
        hLayoutTop.addWidget(self.led2)
        hLayoutTop.addWidget(self.edPlayer2)
        vLayout.addLayout(hLayoutTop)

        hLayoutMiddle = QHBoxLayout()

        self.lwPlayer1History = QListWidget()
        self.lwPlayer1History.setItemAlignment(Qt.AlignmentFlag.AlignRight)
        self.lwPlayer1History.setStyleSheet(stylesheet_player_score_history)

        self.lwPlayer2History = QListWidget()
        self.lwPlayer2History.setItemAlignment(Qt.AlignmentFlag.AlignRight)
        self.lwPlayer2History.setStyleSheet(stylesheet_player_score_history)

        keypadbytotal = KeypadByTotal()
        keypadbytotal.total_entered.connect(lambda total: self.handleScore(total))

        # TabWidget is to enable multiple input methods. Not needed for MVP.
        # tabWidget = QTabWidget()
        # tabWidget.addTab(keypadbytotal, "By Total")
        # tabWidget.addTab(KeypadByDart(), "By Dart")
        # tabWidget.setStyleSheet(stylesheet_tab_widget)

        # Use grid layout for a single centred keypad. Replace with TabWidget later.
        keypad_layout = QGridLayout()
        keypad_layout.addWidget(keypadbytotal, 0, 0)

        hLayoutMiddle.addWidget(self.lwPlayer1History)
        # hLayoutMiddle.addWidget(tabWidget)
        spacer = QWidget()
        spacer.setFixedWidth(150)
        hLayoutMiddle.addWidget(spacer)
        hLayoutMiddle.addLayout(keypad_layout)
        hLayoutMiddle.addWidget(spacer)
        hLayoutMiddle.addWidget(self.lwPlayer2History)
        vLayout.addLayout(hLayoutMiddle)

        hLayoutBottom = QHBoxLayout()
        self.edStatusBar = QLineEdit()
        self.edStatusBar.setFont(QFont("Verdana", 18))
        self.edStatusBar.setText("This is the status bar")
        self.edStatusBar.setReadOnly(True)
        hLayoutBottom.addWidget(self.edStatusBar)
        btnExit = QPushButton()
        btnExit.setText("Exit")
        btnExit.setStyleSheet("font-size: 18px;")
        btnExit.clicked.connect(lambda: self.close())
        hLayoutBottom.addWidget(btnExit)
        vLayout.addLayout(hLayoutBottom)

    def reset(self):
        self.edScore1.setText("501")
        self.edScore2.setText("501")
        self.lwPlayer1History.clear()
        self.lwPlayer2History.clear()
        self.appendHistory(1, self.edScore1.text())
        self.appendHistory(2, self.edScore2.text())
        self.setPlayer(1)
        if self.player_to_throw == 1 and self.edScore1.text() == "501":
            self.edStatusBar.setText("Player 1 to throw. Enter score using keypad and press green Enter button when done.")

    def appendHistory(self, player_number, itemString):
        item = QListWidgetItem(itemString)
        item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        if player_number == 1:
            self.lwPlayer1History.addItem(item)
            self.lwPlayer1History.scrollToBottom()
        elif player_number == 2:
            self.lwPlayer2History.addItem(item)
            self.lwPlayer2History.scrollToBottom()

    def setPlayer(self, player_number):
        if player_number == 1:
            self.player_to_throw = 1
            self.led1.setPixmap(self.ledPixmapOn)
            self.led2.setPixmap(self.ledPixmapOff)
            self.edStatusBar.setText("Player 1 to throw")
        elif player_number == 2:
            self.player_to_throw = 2
            self.led1.setPixmap(self.ledPixmapOff)
            self.led2.setPixmap(self.ledPixmapOn)
            self.edStatusBar.setText("Player 2 to throw")
        else:
            raise ValueError("Invalid player number")

    def handleScore(self, score):
        self.debugDimensions()
        if self.player_to_throw == 1:
            before = int(self.edScore1.text())
            after = before - score
            self.edScore1.setText(str(after))
            self.appendHistory(self.player_to_throw, "{} - {} = {}".format(before, score, after))
            self.setPlayer(2)
        elif self.player_to_throw == 2:
            before = int(self.edScore2.text())
            after = before - score
            self.edScore2.setText(str(after))
            self.appendHistory(self.player_to_throw, "{} - {} = {}".format(before, score, after))
            self.setPlayer(1)
        else:
            raise ValueError("Invalid player number")

    def debugDimensions(self):
        log.debug("window width={} height={}".format(self.width(), self.height()))
        log.debug("ed1.width={}".format(self.edPlayer1.width()))
        log.debug("ed2.width={}".format(self.edPlayer2.width()))
        log.debug("ed1.height={}".format(self.edPlayer1.height()))
        log.debug("ed2.height={}".format(self.edPlayer2.height()))

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.debug("starting main()")
    app = QApplication(sys.argv)
    appWindow = AppWindow()

    # Paint the background of the main window with a wood effect
    palette = QPalette()
    pixmap = QPixmap("images/wood.jpg")
    brush = QBrush(pixmap)
    palette.setBrush(QPalette.Window, brush)
    appWindow.setPalette(palette)

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
