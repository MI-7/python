"""
def member(x, items):
    for i in items:
        if x == i:
            return True
        else:
            return False

print member(1, [1, 2])
"""

from operator import *

# list comprehensions
print [x*x for x in range(3)] * 3

# zip
print zip([1, 2, 3], ["x", "y", "z"])

def isSubSet(a, b):
    return reduce(and_, [x in b for x in a])

print isSubSet([2], [1, 3, 5])


print "abc"[2]