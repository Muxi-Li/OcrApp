from PyQt5 import QtCore, QtGui, QtWidgets
from guiocr.app import MainWindow
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__  == "__main__":
    main()