from collections import *
from namedlist import namedlist
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


KB = readPaths('KB2.txt')
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


def resolutionAlgorithm(EntryArrayState):

    resolvedList = []
    cnfList = EntryArrayState
    #cnfList2 = cnfList[1:len(cnfList)]
    #
    # for clause in cnfList:
    #
    #
    # #We can negate every item in cnfList
    # for clause,clause2 in cnfList,cnfList2:
    #     # We need to find NOT (x) and (x) pairs in any two clauses and eliminate this -> produce a new clause
    #     for symbols,symbols2 in clause,clause2:
    #         # compare the symbols in the clauses
    #         symbols_neg = negation(symbols)
    #         if symbols_neg == symbols2:
    #             clause2.remove(symbols2)
    #             clause.remove(symbols)
    #             newclause = list([clause, clause2])

    #Iterate over each state of the entry array
    for state in cnfList:
        defaultState = EntryArrayState
        formatterOutput = resolutionArrayFormatter(state, defaultState.remove(state))
        if formatterOutput != []:
            #Concat with resolvedList
            resolvedList.append((formatterOutput))
    #Compare each state with the rest

    #True - Remove the duplicable entries, Save into the new list - resolvedList
    #False - Save into the new list

    #Resolve the list
    return resolvedList

def resolutionArrayFormatter(entry, array):
    for i in array:
        resolutionArrayCheck(entry, i)
    return []

def resolutionArrayCheck(entry, array):
    return True

def resolutionEntryCheck(entry, clause):
    return True


def formatEntry(entry1,entry2):
    newEntry = []
    for element in entry1:
        if resolutionElementCheck(element,entry2):
            newEntry = entry1.remove(element)
    return newEntry

def resolutionElementCheck(element, entryCheck):
    for i in entryCheck:
        if negation(element) == i:
            return True
    return False


def expandNode(kbList):
    edges = []
    return edges

KB = parseKB(KB)
# KB = resolutionAlgorithm(KB)
for i in KB:
    print(i)
