from collections import *
from namedlist import namedlist

Street = namedtuple('Street', 'StreetName start end')
Coordinate = namedtuple('Coordinate', 'x y')
EdgeLabel = namedtuple('EdgeLabel', 'streetStretch Coordinate stepCost')
frontierObj = namedlist('frontierObj', 'Coordinate stepCost')
Frontier = namedlist('Frontier', 'nodeObj cost')
Children = namedlist('Children','Parent Child')
Node = namedlist('Node','Parent State stepCost')

def get_street_name(coord1, coord2, street_info):
    for i in street_info:
        if (i.start == coord1 and i.end == coord2):
            return i.StreetName


def calcCost(Node1, Node2):
    return ((Node1[0] - Node2[0])**2 + (Node1[1] - Node2[1])**2)**0.5


def isLineEmpty(line):
    return len(line.strip()) == 0


def readPaths(pathFile='Paths.txt'):
    Paths = []
    with open(pathFile) as paths:
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
    with open('Paths.txt') as paths:
        for line in paths:
            entry = line.rstrip('\n').split(' ')
            if len(entry) == 5:
                street_info.append(Street(StreetName=entry[2], 
                	start=Coordinate(x=int(entry[0]), y=int(entry[1])), 
                	end=Coordinate(x=int(entry[3]), y=int(entry[4]))))
    return street_info


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
