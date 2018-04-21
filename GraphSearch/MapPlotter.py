from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtCore import Qt, QPoint, QLine
from PyQt5.QtGui import QPen, QPainter, QColor, QFont
from collections import *
from GraphUtils import *
import sys, random
import time 

class MapPlotter(QWidget):

    def __init__(self, parent):
        super().__init__()
        self.initUI()
        self.street_info = initialize_street_information()
        self.displace_x = 25 #0 #25
        self.displace_y = -25 #0 #-25
        self.displace_coord = QPoint(10,0) #QPoint(0,0)
        self.displace_street = QPoint(10, -5)  #QPoint(0,0)
        self.scaler = 6.5#85 #6.5
        self.traversed_paths = []
        
    def initUI(self):        
        self.setGeometry(500, 0, 1900, 900)
        self.setWindowTitle('Map Plotter')
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_map(painter)
        painter.end()

    def get_mid_point(self, p1, p2):
        p_mid_x = (p1.x()+p2.x())/2
        p_mid_y = (p1.y()+p2.y())/2
        return QPoint(p_mid_x, p_mid_y)

    def mark_paths(self, traversed_paths):
        self.traversed_paths = traversed_paths
        print('Marked Paths!')
        print(traversed_paths)
        self.repaint()

    def draw_map(self, painter):
        pen = QPen()
        pen.setWidth(4)
        pen.setColor(Qt.black)
        pen.setCapStyle(Qt.RoundCap)
        painter.setPen(pen)
        painter.setFont(QFont('Decorative', 8))

        street_name_set = set()
        for i in self.street_info:
            startPoint = QPoint(i.start.x + self.displace_x, i.start.y + self.displace_y)*self.scaler
            endPoint = QPoint(i.end.x + self.displace_x, i. end.y + self.displace_y)*self.scaler
            painter.drawLine(startPoint, endPoint)
            painter.drawText(self.displace_coord + startPoint, ('(' + str(i.start.x) + ', ' + str(i.start.y) + ')'))
            painter.drawText(self.displace_coord + endPoint, ('(' + str(i.end.x) + ', ' + str(i.end.y) + ')'))
            if i.StreetName not in street_name_set:
                painter.drawText(self.displace_street + self.get_mid_point(startPoint, endPoint), i.StreetName)
                street_name_set.add(i.StreetName)

        pen.setColor(Qt.red)
        painter.setPen(pen)

        for j in self.traversed_paths:
            start = Coordinate(j.Parent[0], j.Parent[1])
            end = Coordinate(j.State[0], j.State[1])
            startPoint = QPoint(start.x + self.displace_x, start.y + self.displace_y)*self.scaler
            endPoint = QPoint(end.x + self.displace_x, end.y + self.displace_y)*self.scaler
            painter.drawLine(startPoint, endPoint)
            