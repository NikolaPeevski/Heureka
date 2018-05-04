from collections import *
from namedlist import namedlist

from copy import deepcopy
import  itertools
import itertools


Street = namedtuple('Street', 'StreetName start end')
Coordinate = namedtuple('Coordinate', 'x y')
EdgeLabel = namedtuple('EdgeLabel', 'streetStretch Coordinate stepCost')
frontierObj = namedlist('frontierObj', 'Coordinate stepCost')
Frontier = namedlist('Frontier', 'nodeObj cost')
Children = namedlist('Children','Parent Child')
Node = namedlist('Node','Parent State stepCost')
filename = "Paths.txt"

def get_street_name(coord1, coord2, street_info):
    for i in street_info:
        if (i.start == coord1 and i.end == coord2):
            return i.StreetName


def calcCost(Node1, Node2):
    return ((Node1[0] - Node2[0])**2 + (Node1[1] - Node2[1])**2)**0.5


def isLineEmpty(line):
    return len(line.strip()) == 0


def readPaths(filename):
    Paths = []
    with open(filename) as paths:
        for line in paths:
            if not isLineEmpty(line):
                Paths.append(line.replace("\n", ""))
    return Paths


def parsePaths(paths):
    (x1, x2, SC, x3, x4) = paths.split(' ')
    Start = (int(x1), int(x2))
    StreetLabel = SC
    End = (int(x3), int(x4))
    return (Start, StreetLabel, End)


def pairwise(lst):
    if not lst:
        return
    i = 0
    while i < (len(lst) - 1):
        yield lst[i], lst[i + 1]
        i += 2


def initialize_street_information():
    street_info = []
    with open(filename) as paths:
        for line in paths:
            entry = line.rstrip('\n').split(' ')
            if len(entry) == 5:
                street_info.append(Street(StreetName=entry[2], 
                	start=Coordinate(x=int(entry[0]), y=int(entry[1])), 
                	end=Coordinate(x=int(entry[3]), y=int(entry[4]))))
    return street_info


def extract_coordinates():
	street_info = initialize_street_information()
	coordinate_set = set()
	for i in street_info:
		coordinate_set.add(i.start)
		coordinate_set.add(i.end)
	return coordinate_set


def print_directions(explored, end):
    street_info = initialize_street_information()
    print(explored)
    explored.append(end)
    print('Directions...')
    for start, end in pairwise(explored):
        print('Walk from {} through {} to get to {}'.format(
            start, get_street_name(start, end, street_info), end))


def print_directions2(explored, end):
    street_info = initialize_street_information()
    print(explored)
    print('Directions...')
    for node in explored:
        print('Walk from {} through {} to get to {}'.format(
            node.Parent, get_street_name(node.Parent, node.State, street_info), node.State))


def readPaths(filename):
    Paths = []
    with open(filename) as paths:
        for line in paths:
            if not isLineEmpty(line):
                Paths.append(line.replace("\n", ""))
    return Paths


def extract_coordinates():
    street_info = initialize_street_information()
    coordinate_set = set()
    for i in street_info:
        coordinate_set.add(i.start)
        coordinate_set.add(i.end)
    return coordinate_set


def parseKB(kbList):
    for i in range(0, len(kbList)):
        kbList[i] = kbList[i].replace(' ', '').split("IF")

        if len(kbList[i]) == 1:
            kbList[i].append([])
        else:
            kbList[i][1] = kbList[i][1].split(',')
            kbNotSplit = kbList[i][0].split(negsymbol)

            kbList[i][0] = negation(kbNotSplit)

    expDistribution(kbList)

    return kbList


def negation(splittedEntry):
    if ((len(splittedEntry) - 1) % 2 == 0):
        final = ''
        for k in splittedEntry:
            if k != negsymbol:
                final += k
        return negsymbol + ' ' + final
    return splittedEntry.pop()


def genResolution(kbList,negSymbol,toProve):
    toProve = negation(toProve.split(negSymbol))
    kbList.append(toProve)
    return kbList


def expDistribution(kbList):
    for i in range(0,len(kbList)):
        if(len(kbList[i][1])>1):
            #Entire array
            test = kbList[i][1]
            entry = kbList[i]
            kbList.pop(i) # Removing the entry from kbList
            for j in range(0, len(entry[1])):
                newEntry = [entry[0], [entry[1][j]]]
                if newEntry not in kbList:
                    kbList.insert(i, newEntry) # adding a new entry for each individual RHS item in kbList entry
    return kbList


def negateList(posList):
    negList = []
    for i in posList:
        negList.append(negation([i]))
    return negList


def removeRNOT(symbol): # Removes Redundant NOT symbols
    condensed = symbol.split("NOT ")
    if (len(condensed)%2 == 0):
        return 'NOT ' + condensed[-1]
    else:
        return condensed[-1]


def removeRNOTlist(List):
    notList = []
    for i in range(0,len(List)):
        notList.append(removeRNOT(List[i]))
    return notList


def negateKB(KBlist):
    negatedList = []
    for i in KBlist:
        x = negateList(i)
        y = removeRNOTlist(x)
        negatedList.append(y)
    return negatedList


def simplifyKB(KB):
    simpleKB = []
    for i in KB:
        if (len(i[1]) > 0):
            store = [i[0],i[1][0]]
        else:
            store = [i[0]]
        simpleKB.append(store)
    return simpleKB


def resolvePair(Ci,Cj):
    Ci_new = Ci
    Cj_new = Cj
    resolvedClause = []
    negatedCj = removeRNOTlist(negateList(Cj))
    resolvedElements = set(Ci).intersection(negatedCj)
    for i in resolvedElements:
        Ci_new.remove(i)
        j = removeRNOT('NOT ' + i)
        Cj_new.remove(j)
    if len(resolvedElements) > 0:
        resolvedClause.extend(Ci_new)
        resolvedClause.extend(Cj_new)
    else:
        return False
    return list(set(resolvedClause)) # Removing duplicates


def Resolution(rules):
    newClauses = []
    for i in range(0, len(rules)):
        for j in range(0, len(rules)):
            if i < j:
                Clause1 = deepcopy(rules[i])
                Clause2 = deepcopy(rules[j])
                resolved = resolvePair(Clause1, Clause2)
                if resolved != False and resolved not in newClauses:
                    newClauses.append(resolved)
    return newClauses


def matchNegThesis(clause, goal):
    return len(goal) - len(set(clause).intersection(goal))

def heuristicCost(clause):
    return len(clause)

def clauseCost(resolvedClauses, thesis):
    costList = []
    neg_thesis = removeRNOTlist(negateList(thesis))
    for i in resolvedClauses:
        score = matchNegThesis(i, neg_thesis)
        costList.append(score)
    return costList


def createNode(currKB,newClause,stepCost):
    parentState = currKB
    childState = deepcopy(currKB)
    if newClause not  in childState:
        childState.append(newClause)
    childNode = Node(Parent=currKB,State=childState,stepCost=stepCost)
    return childNode


def expand(currKB):
    Children = []
    stepCost = 1
    possClauses = Resolution(deepcopy(currKB))
    for i in possClauses:
        child = createNode(deepcopy(currKB),i,stepCost)
        if child.Parent != child.State: # No self loops
            Children.append(child)
    return Children


def goalTest(testList,goal):
    for i in testList:
        if i == goal:
            return True
    return False


KB = readPaths('KB.txt')
negsymbol = 'NOT'


KB = parseKB(KB)
print(KB)
# KB = expDistribution(KB)
# KB = resolutionAlgorithm(KB)

# negateList(KB)
simpleKB = simplifyKB(KB)
print(simpleKB)


thesis = ['fo','bu']
toProve = negateList(deepcopy(thesis))
toProve = ['fo','NOT e']
RULES = simpleKB
#toProve = ['NOT fo']
RULES.append(toProve)


y = Resolution(deepcopy(RULES))
#print(y)

testing1 = expand(deepcopy(RULES))[0].State
testing = expand(testing1)


initialState = RULES
goalState = []

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


def GraphSearch3(initialState, goalState):
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
        if goalTest(currNode.State,goalState): # Goal Test stage
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
        children = expand(currNode.State) # Get the children of the current node
        for child in children:
            if child.State in frontierSet: #Check if we need to update the path cost of any node (a shorter path was found) and hence parent
                if reevalPathcost(deepcopy(everyNode), initialState, deepcopy(child)) == True:
                    updateParent(frontier,deepcopy(child))
            if child.State not in frontierSet and child.State not in exploredSet:
                pathCost = 0
                pathTrail.append(child)
                if child not in everyNode:
                    everyNode.append(child)
                pathCost = calcPathcost(initialState, child.State, deepcopy(pathTrail), pathCost)
                addedClause = child.State[-1]
                h = matchNegThesis(deepcopy(addedClause),removeRNOTlist(negateList(deepcopy(thesis))))
                h = heuristicCost(addedClause)
                # pathCost = calcPathcost(initialState,child.State,deepcopy(pathTrail),pathCost) # Get path cost to current node using parent pointers - IMP to use this approach since path cost may change during the search
                f = pathCost + h# f = g + h  -> A* Algorithm
                # f = pathCost # Dijkstra's Algorithm
                # f = calcCost(child.State,goalState) # GBFS
                frontier.append(Frontier(nodeObj=child,cost=f))
                frontierSet.append(child.State)
        frontier = sorted(frontier, key=lambda cost: cost[1])  # Sorting according to f cost
    return "FAIL!"

SOLUTION = GraphSearch3(deepcopy(initialState),deepcopy(goalState))
if SOLUTION != 'FAIL!':
    print('Step ',1,': ',SOLUTION[0].State)
    for i in range(0,len(SOLUTION)):
        print('Step ',i+2,': ',SOLUTION[i].State)
else:
    print(SOLUTION)
