# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from PyQt6 import QtWidgets, QtGui
from PyQt6.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(300, 300, 400, 400)
    window.setWindowTitle("Hello World")

    label = QtWidgets.QLabel(window)
    label.setText("Hello World")
    label.setFont(QtGui.QFont("Arial", 36))
    label.move(40, 20)
    label.adjustSize()

    button = QtWidgets.QPushButton(window)
    button.setText("Click Me")
    button.move(40, 100)
    button.clicked.connect(lambda: print_hi('John'))

    window.show()
    sys.exit(app.exec())

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__':
    # print_hi('PyCharm')
    window()
