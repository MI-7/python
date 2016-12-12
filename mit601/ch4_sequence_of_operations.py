# the problem to solve is, given two operations, and a target number.
# how to reach the target number from 1 using combinations of operations
# and, more importantly, what is the mininum steps of operation

# i wish there is a function, that takes input of the target and a list of operations
# and it would return the sequence of operations that did the job


def increment(x):
    return x+1

def square(x):
    return x*x

# the initial list of op is [increment, square]
def apply_operations(op_list, arg):
    #what's the base case?  the application of the operations == target
    #if there are no match for current list, go for next
    if len(op_list) == 0:
        return arg
    else:
        return apply_operations(op_list[1:], op_list[0](arg))

def addLevel(op_list_list, func_list):
    return [x+[y] for x in op_list_list for y in func_list]

def find_sequence(func_list, arg, target):
    #
    op_list_list = [[]]
    bingo = False

    while not bingo:
        op_list_list = addLevel(op_list_list, func_list)
        print len(op_list_list)
        for op_list in op_list_list:
            print op_list
            if target == apply_operations(op_list, arg):
                bingo = True
                break

f_list=[increment, square]
find_sequence(f_list, 1, 100)
