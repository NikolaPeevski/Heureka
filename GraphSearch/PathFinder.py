from collections import *
from namedlist import namedlist
from GraphUtils import *
from GraphSearch import GraphSearch
from copy import deepcopy

start = (10,70)
end = (20,50)
x = GraphSearch(start, end,"path")
print(x)