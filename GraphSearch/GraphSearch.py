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

for i in readPaths('Paths.txt'):
    obj = parsePaths(i)
    parentCoordinate = Coordinate(x=obj[0][0], y=obj[0][1])
    Vertices.append(parentCoordinate)
    edgeCoordinate = obj[2] # Getting the coordinate of the child node
    g = calcCost(parentCoordinate,edgeCoordinate)
    e = EdgeLabel(streetStretch=obj[1], Coordinate=edgeCoordinate, stepCost=g)
    Edge.append(e)
    Graph[parentCoordinate].append(e)


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

def calcPathcost(initState,currState,List,pathCost):
    for node in List:
        if node.State == currState:
            pathCost = node.stepCost + pathCost
            currNode = node
            parentState = node.Parent
    if currState == initState:
        return
    calcPathcost(initState, parentState, List, pathCost)
    return pathCost


def GraphSearch2(initialState, goalState):
    frontier = [] # Will contain the nodes in the frontier
    frontierSet = [] # Will contain the current state in the frontier
    pathCost=0
    fCost=0
    initNode = Node(Parent=initialState, State=initialState, stepCost=0)
    solutionPath = [] # Will contain the solution path
    frontier.append(Frontier(nodeObj=initNode, cost=fCost)) # This frontier holds a list of nodes
    frontierSet.append(initialState) # This is the same as the frontier but just holds a list of states (makes it easier in IF statements to compare states and not nodes)
    exploredSet =[] # Will contain a list of visited states (makes it easier in IF statements to compare states and not nodes)
    pathTrail = []  # Contains a list of visited NODES (used to retrieve the solution path)
    while len(frontier) > 0:
        currNode = (frontier.pop(0))[0] # Visit the node having top priority
        if currNode.State == goalState: # Goal Test stage
            pathTrail.append(currNode) # Add goal node to current path
            pathReconstruction(initialState, goalState, pathTrail, solutionPath) # Reconstruct solution path using trail
            print("SUCCESS!")
            return solutionPath
        pathTrail.append(currNode) # Add to explored
        exploredSet.append(currNode.State) # Add to explored
        children = expand2(currNode) # Get the children of the current node
        for child in children:
            if child.State not in frontierSet and child.State not in exploredSet:
                test = pathTrail
                test.append(child)
                pathCost = calcPathcost(initialState,child.State,test,pathCost) # Get path cost to current node using parent pointers - IMP to use this approach since path cost may change during the search
                h = calcCost(child.State,goalState)  # Get heuristic cost
                f = h + pathCost # f = g + h
                frontier.append(Frontier(nodeObj=child,cost=f))
                frontierSet.append(child.State)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to f cost
    print("FAIL")
    return "Fail"


if __name__ == '__main__':
    start = (10,70)
    end = (65,110)
    # GraphSearch2(start, end)
    # print_directions2(GraphSearch2(start,end), end)
