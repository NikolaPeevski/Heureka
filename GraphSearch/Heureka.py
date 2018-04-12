from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
from collections import *
import sys, random
import time 

from mainwindow import Ui_MainWindow

class MainUiClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.findPathBtn

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainUiClass()
	
	window.show()
	sys.exit(app.exec_())