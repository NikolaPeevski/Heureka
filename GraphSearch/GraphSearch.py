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

def expand(node):
    childList = [] # A named list of children (Coordinates, Step-cost)
    Edges = Graph[node] # Get edges from Vertex - these are the children
    for child in Edges:
        # print(child.Coordinate)
        child = frontierObj(Coordinate=child.Coordinate, stepCost=child.stepCost)
        childList.append(child)
    return childList


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


def expand2(node):
    childNodes = []
    children = Graph[node.State] # Gets the children of a node
    for child in children:
          childObj = Node(Parent=node.State, State=child.Coordinate, stepCost=child.stepCost)
          childNodes.append(childObj)
    return childNodes


def pathReconstruction(initState,currState,List,solutionPath):
    for node in List:
        if node.State == currState:
            currNode = node
            parentState = node.Parent
    if currState == initState:
        solutionPath.reverse()
        return
    solutionPath.append(currNode)
    pathReconstruction(initState,currNode.Parent,List,solutionPath)

def GraphSearch2(initialState, goalState):
    frontier = [] # Will contain the nodes in the frontier
    frontierSet = [] # Will contain the current state in the frontier
    pathCost=0
    fCost=0
    initNode = Node(Parent=initialState, State=initialState, stepCost=0)
    pathTrail = []
    solutionPath = []
    frontier.append(Frontier(nodeObj=initNode, cost=fCost))
    frontierSet.append(initialState) # The current state in the frontier
    exploredSet =[] # Will contain a list of visited nodes
    while len(frontier) > 0:
        currNode = (frontier.pop(0))[0] # Remove the node having top priority
        pathCost = currNode.stepCost + pathCost # Calculate path cost -> Path Cost = Path Cost + step cost (g)
        if currNode.State == goalState:
            pathTrail.append(currNode)
            pathReconstruction(initialState, goalState, pathTrail, solutionPath) # Reconstruct solution path using trail
            print("SUCCESS!")
            return solutionPath
        # print("Intermediate Location: ",node.State)
        pathTrail.append(currNode)
        exploredSet.append(currNode.State)
        children = expand2(currNode)
        for child in children:
            if child.State not in frontierSet and child.State not in exploredSet:
                g = child.stepCost
                fCost = calcCost(child.State,goalState)  # f = g + h
                frontier.append(Frontier(nodeObj=child,cost=fCost))
                frontierSet.append(child.State)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to cost
    print("FAIL")
    return "Fail"

if __name__ == '__main__':
    start = (10,70)
    end = (65,110)

    print_directions2(GraphSearch2(start,end), end)
