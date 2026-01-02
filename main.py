import sys, logging

from PySide6 import QtWidgets#, QtGui
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QWidget, QTabWidget, QLineEdit, QHBoxLayout, QVBoxLayout, QTextEdit, \
    QPushButton

from keypad import Calculator

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setGeometry(0, 0, 1280, 720)
        self.setWindowTitle("Darts Scoreboard")

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

        edScore1 = QLineEdit()
        edScore1.setFont(QFont("Verdana", 36))
        edScore1.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edScore1.setText("501")
        edScore1.setFixedSize(160, 80)

        edScore2 = QLineEdit()
        edScore2.setFont(QFont("Verdana", 36))
        edScore2.setAlignment(Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter)
        edScore2.setText("501")
        edScore2.setFixedSize(160, 80)

        hLayoutTop.addWidget(edPlayer1)
        hLayoutTop.addWidget(edScore1)
        hLayoutTop.addWidget(edScore2)
        hLayoutTop.addWidget(edPlayer2)
        vLayout.addLayout(hLayoutTop)

        hLayoutMiddle = QHBoxLayout()
        edPlayer1History = QTextEdit()
        edPlayer2History = QTextEdit()
        tabWidget = QTabWidget()
        tabWidget.addTab(Calculator(), "By Total")
        tabWidget.addTab(Calculator(), "By Dart")
        hLayoutMiddle.addWidget(edPlayer1History)
        hLayoutMiddle.addWidget(tabWidget)
        hLayoutMiddle.addWidget(edPlayer2History)
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
    appWindow.showFullScreen()
    # appWindow.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
