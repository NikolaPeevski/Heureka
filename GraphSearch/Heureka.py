from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
import GraphSearch
from GraphUtils import *
import sys
import random
import time

from mainwindow import Ui_MainWindow


class MainUiClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.findPathBtn.clicked.connect(self.run_search)
        self.street_info = []
        initialize_street_information()

    def run_search(self):
        result = GraphSearch.GraphSearch((10, 70), (65, 110))
        self.statusConsole.clear()
        self.statusConsole.insertPlainText('Directions...\n\n')
        street_info = initialize_street_information()
        total_cost = 0
        for start, end in pairwise(result):
            cost = calcCost(start, end)
            total_cost += cost
            msgFormat = 'Walk from {} through {} to get to {}, Cost: {:.2f}\n'
            self.statusConsole.insertPlainText(msgFormat.format(start, get_street_name(start, end, street_info), end, cost))
        self.statusConsole.insertPlainText('\nTotal Cost: {:.2f}'.format(total_cost) + '\n')
        self.statusConsole.insertPlainText('\nRaw Result\n' + str(result) + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUiClass()

    window.show()
    sys.exit(app.exec_())
