import logging
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase, QPalette, QPixmap, QBrush
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QListWidget, QGridLayout, QMainWindow, QLabel

from keypadbytotal import KeypadByTotal

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    player_to_throw = None

    def __init__(self):
        super().__init__()

        QFontDatabase.addApplicationFont("fonts/7segment.ttf")
        self.setStyleSheet("font-family: Verdana;")
        stylesheet_player_name = "font-size:36pt;"
        stylesheet_player_score = "font-family: '7-segment'; font-size:72pt; color: #E31B23; background-color: black;"
        stylesheet_player_score_history = "font-size:18pt;"
        # stylesheet_tab_widget = "QTabBar::tab { width: 300px; height: 50px; font-size: 18px;}"

        vLayout = QVBoxLayout(self)

        hLayoutTop = QtWidgets.QHBoxLayout()

        edPlayer1 = QLineEdit()
        edPlayer1.setStyleSheet(stylesheet_player_name)
        edPlayer1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edPlayer1.setText("Player 1")

        edPlayer2 = QLineEdit()
        edPlayer2.setStyleSheet(stylesheet_player_name)
        edPlayer2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edPlayer2.setText("Player 2")

        self.edScore1 = QLineEdit()
        self.edScore1.setStyleSheet(stylesheet_player_score)
        self.edScore1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edScore1.setFixedWidth(250)
        self.edScore1.setReadOnly(True)

        self.edScore2 = QLineEdit()
        self.edScore2.setStyleSheet(stylesheet_player_score)
        self.edScore2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        self.edScore2.setFixedWidth(250)
        self.edScore2.setReadOnly(True)

        ledPixmapOn = QPixmap("images/led-on.png")
        ledPixmapOff = QPixmap("images/led-off.png")
        led1 = QLabel()
        led1.setFixedSize(30, 30)
        led1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        led1.setPixmap(ledPixmapOn.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))

        led2 = QLabel()
        led2.setFixedSize(30, 30)
        led2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        led2.setPixmap(ledPixmapOff.scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))

        hLayoutTop.addWidget(edPlayer1)
        hLayoutTop.addWidget(led1)
        hLayoutTop.addWidget(self.edScore1)
        hLayoutTop.addWidget(self.edScore2)
        hLayoutTop.addWidget(led2)
        hLayoutTop.addWidget(edPlayer2)
        vLayout.addLayout(hLayoutTop)

        hLayoutMiddle = QHBoxLayout()

        self.lwPlayer1History = QListWidget()
        self.lwPlayer1History.setItemAlignment(Qt.AlignmentFlag.AlignRight)
        self.lwPlayer1History.setStyleSheet(stylesheet_player_score_history)
        self.lwPlayer1History.addItems(["501 - 26 = 475", "475 - 100 = 375", "375 - 57 = 318"])
        self.lwPlayer1History.addItems((str(i) for i in range(50)))
        self.lwPlayer1History.scrollToBottom()

        self.lwPlayer2History = QListWidget()
        self.lwPlayer2History.setItemAlignment(Qt.AlignmentFlag.AlignRight)
        self.lwPlayer2History.setStyleSheet(stylesheet_player_score_history)
        self.lwPlayer2History.addItems(["501 - 26 = 475", "475 - 100 = 375", "375 - 57 = 318"])
        self.lwPlayer2History.addItems((str(i) for i in range(50)))
        self.lwPlayer2History.scrollToBottom()

        keypadbytotal = KeypadByTotal()
        keypadbytotal.total_entered.connect(lambda xxx: log.debug(xxx))

        # TabWidget is to enable multiple inpout methods. Not needed for MVP.
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
        spacer.setFixedWidth(200)
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
        self.lwPlayer1History.addItem("501")
        self.lwPlayer1History.setStyleSheet("font-align: right;")
        self.lwPlayer2History.addItem("501")
        self.setPlayer(1)

    def setPlayer(self, player_number):
        if player_number == 1:
            self.edStatusBar.setText("Player 1 to throw")
            self.player_to_throw = 1
        elif player_number == 2:
            self.edStatusBar.setText("Player 2 to throw")
            self.player_to_throw = 2
        else:
            raise ValueError("Invalid player number")

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
