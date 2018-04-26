import math
from collections import *
from PyQt5.QtWidgets import QApplication
from MapPlotter import MapPlotter
from GraphUtils import *
from copy import deepcopy
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
    tempList = List
    if currState == initState or len(tempList) == 0:
        return 0
    for node in tempList:
        if node.State == currState:
            pathCost = node.stepCost
            currNode = node
            parentState = node.Parent
            tempList.remove(currNode)
    return pathCost + calcPathcost(initState, parentState, tempList, pathCost)

def updateParent(List,currentNode):
    for node in List:
        nodeOb = node[0]
        if nodeOb.State == currentNode.State:
            nodeOb.Parent = currentNode.Parent
            nodeOb.stepCost = calcCost(nodeOb.Parent,currentNode.State)
    return

def reevalPathcost(traversedNodes,initialState,currChild):
    prevPathCost = 0
    newPathCost = 0
    nodes = deepcopy(traversedNodes)
    prevPathCost = calcPathcost(initialState, currChild.State, deepcopy(nodes), prevPathCost)
    newPathCost = calcPathcost(initialState, currChild.Parent, deepcopy(nodes), newPathCost) + currChild.stepCost
    if prevPathCost > newPathCost:
        return True
    else:
        return False
        frontierSet.remove(child.State)

def GraphSearch2(initialState, goalState):
    frontier = [] # Will contain the nodes in the frontier
    frontierSet = [] # Will contain the current state in the frontier
    initNode = Node(Parent=initialState, State=initialState, stepCost=0) # Initial State - Points to itself - Parent is itself
    frontier.append(Frontier(nodeObj=initNode, cost=0)) # This frontier holds a list of nodes
    frontierSet.append(initialState) # This is the same as the frontier but just holds a list of states (makes it easier in IF statements to compare states and not nodes)
    exploredSet =[] # Will contain a list of visited states (makes it easier in IF statements to compare states and not nodes)
    pathTrail = []  # Contains a list of visited NODES (used to retrieve the solution path)
    everyNode = [] # Keeping track of every node in the graph
    solutionPath = [] # Will contain the solution path
    while len(frontier) > 0:
        currNode = (frontier.pop(0))[0] # Visit the node having top priority
        frontierSet.remove(currNode.State) # Same as above (remove from frontier)
        if currNode.State == goalState: # Goal Test stage
            pathTrail.append(currNode) # Add goal node to current path
            pathReconstruction(initialState, goalState, pathTrail, solutionPath) # Reconstruct solution path using trail
            return solutionPath
        pathTrail.append(currNode) # Add to explored
        if currNode not in everyNode: # Just to avoid repeated nodes
            everyNode.append(currNode)
        exploredSet.append(currNode.State) # Add to explored
        children = expand2(currNode) # Get the children of the current node
        for child in children:
            if child.State in frontierSet: #Check if we need to update the path cost of any node (a shorter path was found) and hence parent
                if reevalPathcost(deepcopy(everyNode), initialState, deepcopy(child)) == True:
                    updateParent(frontier,deepcopy(child))
            if child.State not in frontierSet and child.State not in exploredSet:
                pathCost = 0
                pathTrail.append(child)
                if child not in everyNode:
                    everyNode.append(child)
                pathCost = calcPathcost(initialState,child.State,deepcopy(pathTrail),pathCost) # Get path cost to current node using parent pointers - IMP to use this approach since path cost may change during the search
                f = calcCost(child.State,goalState) + pathCost # f = g + h  -> A* Algorithm
                # f = pathCost # Dijkstra's Algorithm
                # f = calcCost(child.State,goalState) # GBFS
                frontier.append(Frontier(nodeObj=child,cost=f))
                frontierSet.append(child.State)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to f cost
    return "Fail"


if __name__ == '__main__':
    start = (80,70)
    end = (35,120)
    GraphSearch2(start, end)
    # print_directions2(GraphSearch2(start,end), end)




