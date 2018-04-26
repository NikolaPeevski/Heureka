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

KB = readPaths('KB.txt')
print(KB)

negsymbol = 'NOT'

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



def expandNode(kbList):
    edges = []
    return edges

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


KB = parseKB(KB)
print(KB)
# KB = expDistribution(KB)
# KB = resolutionAlgorithm(KB)
print(KB)


testList1 = ['bu','NOT fo','te']
# negateList(KB)
simpleKB = simplifyKB(KB)
checker = 'NOT NOT NOT NOT NOT fo'
print(simpleKB)
testList2 = ['bu','NOT fo']
#commons = set(testList1).intersection(testList2)
#print(negateList([testList1]))

negKB = negateKB(deepcopy(simpleKB))


# Preliminary Code for Resolution Algorithm - Finding the common pairwise elements using intersection
# Note that some sets are the same but inverted : Comparing set 2 and 5 is like comparing set 5 and 2 - room for optimization in that regard
# For resolution: we want to choose the set which contains the highest number of elements and then remove those two items from our original KB list
for i in range(0,len(simpleKB)):
    x = []
    for j in range(0,len(simpleKB)):
        if i != j:
            x.append(set(simpleKB[i]).intersection(simpleKB[j]))

    print('Set Number ',i, ': ',x)