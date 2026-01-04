import sys, logging

from PySide6 import QtWidgets#, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton, QListView, QListWidget

from keypadbydart import KeypadByDart
from keypadbytotal import KeypadByTotal

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        vLayout = QVBoxLayout(self)

        hLayoutTop = QtWidgets.QHBoxLayout()

        edPlayer1 = QLineEdit()
        edPlayer1.setFont(QFont("Verdana", 24))
        edPlayer1.setAlignment(Qt.AlignmentFlag.AlignRight)
        edPlayer1.setText("Player 1")

        edPlayer2 = QLineEdit()
        edPlayer2.setFont(QFont("Verdana", 24))
        edPlayer2.setAlignment(Qt.AlignmentFlag.AlignLeft)
        edPlayer2.setText("Player 2")

        QFontDatabase.addApplicationFont("fonts/7segment.ttf")

        edScore1 = QLineEdit()
        edScore1.setFont(QFont("7-segment", 72))
        edScore1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edScore1.setText("501")
        edScore1.setFixedSize(160, 80)

        edScore2 = QLineEdit()
        edScore2.setFont(QFont("7-segment", 48))
        edScore2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edScore2.setText("501")
        edScore2.setFixedSize(160, 80)

        hLayoutTop.addWidget(edPlayer1)
        hLayoutTop.addWidget(edScore1)
        hLayoutTop.addWidget(edScore2)
        hLayoutTop.addWidget(edPlayer2)
        vLayout.addLayout(hLayoutTop)

        hLayoutMiddle = QHBoxLayout()

        edPlayer1History = QListWidget()
        edPlayer1History.setItemAlignment(Qt.AlignmentFlag.AlignRight)
        edPlayer1History.setFont(QFont("Verdana", 18))
        edPlayer1History.addItems(["501 - 26 = 475", "475 - 100 = 375", "375 - 57 = 318"])
        edPlayer1History.addItems((str(i) for i in range(50)))
        edPlayer1History.scrollToBottom()

        edPlayer2History = QTextEdit()
        tabWidget = QTabWidget()
        tabWidget.addTab(KeypadByTotal(), "By Total")
        tabWidget.addTab(KeypadByDart(), "By Dart")
        hLayoutMiddle.addWidget(edPlayer1History)
        hLayoutMiddle.addWidget(tabWidget)
        hLayoutMiddle.addWidget(edPlayer2History)
        tabWidget.setStyleSheet("QTabBar::tab { width: 200px; height: 60px; font-family: Verdana; font-size: 18px;}")
        vLayout.addLayout(hLayoutMiddle)

        hLayoutBottom = QHBoxLayout()
        edStatusBar = QLineEdit()
        edStatusBar.setFont(QFont("Verdana", 18))
        edStatusBar.setText("This is the status bar")
        hLayoutBottom.addWidget(edStatusBar)
        btnExit = QPushButton()
        btnExit.setText("Exit")
        btnExit.setStyleSheet("font-family: Verdana; font-size: 18px;")
        btnExit.clicked.connect(lambda: self.close())
        hLayoutBottom.addWidget(btnExit)
        vLayout.addLayout(hLayoutBottom)

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.debug("starting main()")
    app = QApplication(sys.argv)
    appWindow = AppWindow()
    if sys.argv[-1] != "debug":
        log.debug("starting in full-screen (release) mode")
        appWindow.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        appWindow.showFullScreen()
    else:
        log.debug("starting in windowed (debug) mode")
        appWindow.setWindowTitle("Darts Scoreboard")
        appWindow.setGeometry(800, 300, 1280, 720)
        appWindow.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()
