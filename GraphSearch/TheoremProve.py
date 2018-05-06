from collections import *
from namedlist import namedlist

from copy import deepcopy
from GraphUtils import *
from GraphSearch import *

KB = readPaths('KB.txt')

KB = parseKB(KB)

simpleKB = simplifyKB(KB) #Turns the parsed KB into [A,B,...],[C,D,...] : A list of clauses
print(simpleKB)

thesis = ['bu','e','to'] # What we are trying to prove  bu and e
toProve = negateList(deepcopy(thesis)) # Proof by contradiction -> not bu or not e
RULES = simpleKB # The Rules we have
RULES.append(toProve) # We append the negated thesis to it

y = Resolution(deepcopy(RULES)) # One step of the resolution algorithm

initialState = RULES # Our initial state will be the rules
goalState = [] # Our goal state is the empty clause


SOLUTION = GraphSearch(deepcopy(initialState),deepcopy(goalState),'logic')
if SOLUTION != 'FAIL!':
    print('Step ',1,': ',SOLUTION[0].State)
    for i in range(0,len(SOLUTION)):
        print('Step ',i+2,': ',SOLUTION[i].State)
else:
    print(SOLUTION)