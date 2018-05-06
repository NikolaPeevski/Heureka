import math
from collections import *
from PyQt5.QtWidgets import QApplication
from MapPlotter import MapPlotter
from GraphUtils import *
from copy import deepcopy
import sys


def GraphSearch(initialState, goalState,type):
    frontier = [] # Will contain the nodes in the frontier
    frontierSet = [] # Will contain the current state in the frontier
    initNode = Node(Parent=initialState, State=initialState, stepCost=0) # Initial State - Points to itself - Parent is itself
    frontier.append(Frontier(nodeObj=initNode, cost=0)) # This frontier holds a list of nodes
    frontierSet.append(initialState) # This is the same as the frontier but just holds a list of states (makes it easier in IF statements to compare states and not nodes)
    exploredSet =[] # Will contain a list of visited states (makes it easier in IF statements to compare states and not nodes)
    pathTrail = []  # Contains a list of visited NODES (used to retrieve the solution path)
    everyNode = [] # Keeping track of every node in the graph
    solutionPath = [] # Will contain the solution path
    pathCost = 0
    while len(frontier) > 0:
        currNode = (frontier.pop(0))[0] # Visit the node having top priority
        pathCost = pathCost + currNode.stepCost
        frontierSet.remove(currNode.State) # Same as above (remove from frontier)
        if goalTest(currNode.State,goalState,type): # Goal Test stage
            pathTrail.append(currNode) # Add goal node to current path
            pathReconstruction(initialState, currNode.State, pathTrail, solutionPath) # Reconstruct solution path using trail
            print('GENERATED STATES: ',len(pathTrail))
            return solutionPath
        if currNode not in pathTrail:
            pathTrail.append(currNode) # Add to explored
        if currNode not in everyNode: # Just to avoid repeated nodes
            everyNode.append(currNode)
        if currNode.State not in exploredSet:
            exploredSet.append(currNode.State) # Add to explored
        children = []  # Reset children
        children = expand(currNode.State,type) # Get the children of the current node
        for child in children:
            # Comment these 3 lines to try GBFS
            if child.State in frontierSet: #Check if we need to update the path cost of any node (a shorter path was found) and hence parent
                if reevalPathcost(deepcopy(everyNode), initialState, deepcopy(child)) == True:
                    updateParent(frontier,deepcopy(child),type)
            if child.State not in frontierSet and child.State not in exploredSet:
                pathCost = 0
                pathTrail.append(child)
                if child not in everyNode:
                    everyNode.append(child)
                pathCost = calcPathcost(initialState, child.State, deepcopy(pathTrail), pathCost)
                if type == "logic": # Heuristic for theorem Proving
                    addedClause = child.State[-1]
                    h = heuristicCost(addedClause)
                if type == "path": # Heuristic for path finding
                    h = calcCost(child.State,goalState,'path')
                f = pathCost + h
                # f = pathCost # Dijkstra's Algorithm # Uncomment to try Dijsktra's Algorithm
                # f = calcCost(child.State,goalState) # Uncomment to try GBFS
                frontier.append(Frontier(nodeObj=child,cost=f))
                frontierSet.append(child.State)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to f cost
    return "FAIL!"


if __name__ == '__main__':
    start = (10,70)
    end = (20,50)
    x = GraphSearch(start, end,"path")
    print (x)
    # print_directions2(GraphSearch2(start,end), end)




