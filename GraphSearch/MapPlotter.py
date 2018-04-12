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

        self.street_info = []

        with open('Paths.txt') as paths:
            for line in paths:
                entry = line.rstrip('\n').split(' ')
                if len(entry) == 5:
                    self.street_info.append(Street(StreetName=entry[2], 
                    start=Coordinate(x=int(entry[0]), y=int(entry[1])), 
                    end=Coordinate(x=int(entry[3]), y=int(entry[4]))))
        
    def initUI(self):        
        self.setGeometry(500, 0, 1900, 900)
        self.setWindowTitle('Map Plotter')
        self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        self.draw_point(painter)
        painter.end()

    def get_mid_point(self, p1, p2):
        p_mid_x = (p1.x()+p2.x())/2
        p_mid_y = (p1.y()+p2.y())/2
        return QPoint(p_mid_x, p_mid_y)

        
    def draw_point(self, painter):
        pen = QPen()
        pen.setWidth(4)
        pen.setColor(Qt.black)
        pen.setCapStyle(Qt.RoundCap)
        
        painter.setPen(pen)
        painter.setFont(QFont('Decorative', 8))
        displace_x = 25
        displace_y = -25
        displace_coord = QPoint(10,0)
        displace_street = QPoint(10, -5)
        scaler = 6.5
        street_name_set = set()
        for i in self.street_info:
            startPoint = QPoint(i.start.x + displace_x, i.start.y + displace_y)*scaler
            endPoint = QPoint(i.end.x + displace_x, i. end.y + displace_y)*scaler
            painter.drawLine(startPoint, endPoint)
            painter.drawText(displace_coord + startPoint, ('(' + str(i.start.x) + ', ' + str(i.start.y) + ')'))
            painter.drawText(displace_coord + endPoint, ('(' + str(i.end.x) + ', ' + str(i.end.y) + ')'))
            if i.StreetName not in street_name_set:
                painter.drawText(displace_street + self.get_mid_point(startPoint, endPoint), i.StreetName)
                street_name_set.add(i.StreetName)
            