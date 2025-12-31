from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QWidget
import sys, logging

log = logging.getLogger(__name__)

class AppWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        self.setGeometry(300, 300, 400, 400)
        self.setWindowTitle("Hello World")

        label = QtWidgets.QLabel(self)
        label.setText("Hello World")
        label.setFont(QtGui.QFont("Arial", 36))
        label.move(40, 20)
        label.adjustSize()

        button = QtWidgets.QPushButton(self)
        button.setText("Click Me")
        button.move(40, 100)
        button.clicked.connect(lambda: log.debug('Clicked'))

        btnExit = QtWidgets.QPushButton(self)
        btnExit.setText("Exit")
        btnExit.move(40, 160)
        btnExit.clicked.connect(lambda: self.close())

def main():
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    log.debug("starting main()")
    app = QApplication(sys.argv)
    appWindow = AppWindow()
    appWindow.showFullScreen()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
