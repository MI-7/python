# towers of hanoi

steps = 0

# n levels of tower, from pole A to pole B, using pole C
def move(n, A, B, C):
    if n == 1:
        print "move 1 from ", A, " to ", B
        global steps
        steps+=1
    else:
        move(n-1, A, C, B)
        # move(n, A, B, C)
        print "move ", n , " from ", A, " to ", B
        global steps
        steps+=1
        move(n-1, C, B, A)

move(5, 'a', 'b', 'c')
print "total steps: ", steps
