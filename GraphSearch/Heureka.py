from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtCore import Qt
import GraphSearch
from GraphUtils import *
import sys
import random
import time
import re
import statistics

from mainwindow import Ui_MainWindow


class MainUiClass(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainUiClass, self).__init__(parent)
        self.setupUi(self)
        self.findPathBtn.clicked.connect(self.run_search)
        self.testBtn.clicked.connect(self.run_search_exhaustive)
        self.street_info = initialize_street_information()

    def run_search(self):
        start = str(self.sourceEdit.text())
        destination = str(self.dstEdit.text())
        start_coord = re.findall(r'\d+', start)
        destination_coord = re.findall(r'\d+', destination)

        result = GraphSearch.GraphSearch2((int(start_coord[0]), int(start_coord[1])),
                                          (int(destination_coord[0]), int(destination_coord[1])))
        self.map.mark_paths(result)
        self.statusConsole.clear()
        street_string_info = "\n".join(str(a) for a in self.street_info)
        self.statusConsole.insertPlainText(street_string_info)
        self.statusConsole.insertPlainText('\n\nDirections...\n\n')
        total_cost = 0
        for node in result:
            cost = node.stepCost
            total_cost += cost
            msgFormat = 'Walk from {} through {} to get to {}, Cost: {:.2f}\n'
            self.statusConsole.insertPlainText(msgFormat.format(node.Parent, get_street_name(
                node.Parent, node.State, self.street_info), node.State, cost))
        self.statusConsole.insertPlainText(
            '\nTotal Cost: {:.2f}'.format(total_cost) + '\n')
        self.statusConsole.insertPlainText(
            '\nRaw Result\n' + str(result) + '\n')

    def run_search_exhaustive(self):
        self.statusConsole.clear()
        msgFormat = 'Run {}: {} -> {}, Cost: {:.2f}, Time Elapsed: {:.2f}ms\n'
        coordinates = extract_coordinates()
        counter = 0
        benchmark = list()
        final_cost = list()
        for i in coordinates:
            for j in coordinates:
                if (i != j):
                    counter = counter+1
                    t0 = time.perf_counter()
                    total_cost = 0

                    #print('Computing, {} to {}'.format(i, j))
                    try:
                       result = GraphSearch.GraphSearch2(i, j)
                    except:
                       print('Failed {} to {}'.format(i,j)) 
                    t1 = time.perf_counter()
                    for node in result:
                        cost = node.stepCost
                        total_cost += cost

                    print('Computing, {} to {}'.format(i, j))
                    try:
                       result = GraphSearch.GraphSearch2(i, j)
                    except:
                       print('Failed {} to {}'.format(i,j))	
                    t1 = time.perf_counter()
                    for node in result:
                    	cost = node.stepCost
                    	total_cost += cost
                    final_cost.append(total_cost)
                    benchmark.append((t1-t0)*1000)
                    self.statusConsole.insertPlainText(
                        msgFormat.format(counter, i, j, total_cost, (t1 - t0)*1000))
        msgFormat = '\nBenchmarks:\nMean Cost: {:.2f}\nAvg Time: {:.2f}ms\nMin Time: {:.2f}ms\nMax Time: {:.2f}ms'             
        self.statusConsole.insertPlainText(msgFormat.format(
            statistics.mean(final_cost), statistics.mean(benchmark), min(benchmark), max(benchmark)))            


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainUiClass()

    window.show()
    sys.exit(app.exec_())
