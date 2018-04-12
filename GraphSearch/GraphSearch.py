import math
from collections import *
from namedlist import namedlist
from PyQt5.QtWidgets import QApplication
from MapPlotter import MapPlotter
import sys

def isLineEmpty(line):
    return len(line.strip()) == 0


def readPaths(pathFile):
    Paths = []
    for line in PathsFile:
        if not isLineEmpty(line):
            Paths.append(line.replace("\n",""))
    return Paths


def parsePaths(paths):
    (x1, x2, SC, x3, x4) = paths.split(' ')
    Start = (int(x1),int(x2))
    StreetLabel = SC
    End = (int(x3),int(x4))
    return (Start,StreetLabel,End)


# Reading the Paths from a text file and store them in Paths
PathsFile = open("Paths.txt", "r")
Paths = readPaths(PathsFile)
PathsFile.close()


Coordinate = namedtuple('Coordinate', 'x y') # namedtuple() just makes a tuple readable
Vertices = [] # Empty List
EdgeLabel = namedtuple('EdgeLabel', 'streetStretch Coordinate stepCost')
Edge = [] # Empty List
Graph = defaultdict(list)
Street = namedtuple('Street', 'StreetName start end')
street_info = []

with open('Paths.txt') as paths:
    for line in paths:
        entry = line.rstrip('\n').split(' ')
        if len(entry) == 5:
            street_info.append(Street(StreetName=entry[2], 
                start=Coordinate(x=int(entry[0]), y=int(entry[1])), 
                end=Coordinate(x=int(entry[3]), y=int(entry[4]))))

def getStreetName(coord1, coord2):
    for i in street_info:
        if (i.start == coord1 and i.end == coord2):
            return i.StreetName

def calcCost(Node1,Node2):
    return ((Node1[0]-Node2[0])**2 + (Node1[1] - Node2[1])**2)**0.5


for i in Paths:
    obj = parsePaths(i)
    parentCoordinate = Coordinate(x=obj[0][0], y=obj[0][1])
    Vertices.append(parentCoordinate)
    edgeCoordinate = obj[2] # Getting the coordinate of the child node
    g = calcCost(parentCoordinate,edgeCoordinate)
    e = EdgeLabel(streetStretch=obj[1], Coordinate=edgeCoordinate, stepCost=g)
    Edge.append(e)
    Graph[parentCoordinate].append(e)

# for k, v in Graph.items():
#    for a in v:
#        print("Vertex: (",k.x,", ", k.y, ") " "[",  a.streetStretch, ": ", a.Coordinate, "]"," Step Cost: ",a.pathCost)

frontierObj = namedlist('frontierObj', 'Coordinate stepCost')


def expand(node):
    childList = [] # A named list of children (Coordinates, Step-cost)
    Edges = Graph[node] # Get edges from Vertex
    for child in Edges:
        # print(child.Coordinate)
        child = frontierObj(Coordinate=child.Coordinate, stepCost=child.stepCost)
        childList.append(child)
    return childList


correct_path = list()

def GraphSearch(initialState, goalState):
    pathCost = 0 # Initiliase path cost to zero
    initialFront = frontierObj(Coordinate=initialState, stepCost=0)
    frontier = [initialFront] # Initialising Frontier as an empty set of vertices & step-costs
    exploredSet =[] # Will contain a list of vertices
    while len(frontier) > 0:
        node = frontier.pop(0)
        if node.Coordinate == goalState:
            print("Goal Location: ",goalState)
            print("SUCCESS!")
            return exploredSet
        print("Intermediate Location: ", node.Coordinate)

        exploredSet.append(node.Coordinate)
        children = expand(node.Coordinate)
        for child in children:
            if child not in frontier and child.Coordinate not in exploredSet:
                pathCost = pathCost + child.stepCost
                child.stepCost = calcCost(node.Coordinate,goalState) + child.stepCost
                frontier.append(child)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to cost
    print("FAIL")
    return "Fail"

def pairwise(lst):
    if not lst: return
    i = 0
    while i < (len(lst) - 1):
        yield lst[i], lst[i+1]
        i+=2

if __name__ == '__main__':
    start = (10,70)
    end = (65,110)

    explored = GraphSearch(start,end)
    print(explored)
    explored.append(end)
    print('Directions...')
    for start,end in pairwise(explored):
        print('Walk from {} through {} to get to {}'.format(start, getStreetName(start, end), end))