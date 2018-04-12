import math
from collections import *
from PyQt5.QtWidgets import QApplication
from MapPlotter import MapPlotter
from GraphUtils import *
import sys

Vertices = [] # Empty List
Edge = [] # Empty List
Graph = defaultdict(list)
street_info = []

for i in readPaths():
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
            #print("Goal Location: ",goalState)
            print("SUCCESS!")
            return exploredSet
        #print("Intermediate Location: ", node.Coordinate)

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

if __name__ == '__main__':
    start = (10,70)
    end = (65,110)

    print_directions(GraphSearch(start,end), end)