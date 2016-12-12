import lib601.sm as sm

class Accumulator(sm.SM):
    startState = 0

    def __init__(self, initialValue):
        self.startState = initialValue

    def getNextValues(self, state, inp):
        return (state + inp, state + inp)

    def run(self, n=10):
        return self.transduce([None]*n)

class Delay(sm.SM):
    startState = 0

    def getNextValues(self, state, inp):
        return (inp, state)

class Average2(sm.SM):
    startState = 0

    def getNextValues(self, state, inp):
        return (inp, (inp + state) / 2.0)

class SumLastThree(sm.SM):
    startState = (0, 0)

    def getNextValues(self, state, inp):
        return ((state[1], inp), state[0] + state[1] + inp)




class Cascade(sm.SM):
    startState = ()
    def __init__(self, sm_in, sm_out):
        self.sm_in = sm_in
        self.sm_out = sm_out

    def start(self):
        self.sm_in.start()
        self.sm_out.start()
        self.state = (self.sm_in.startState, self.sm_out.startState)

    def step(self, inp):
        o = self.sm_in.step(inp)
        
        o_out = self.sm_out.step(o)

        self.state = (self.sm_in.state, self.sm_out.state)
        
        return o_out

    def transduce(self, inputs, verbose=False, compact=False):
        self.start()
        return [self.step(inp) for inp in inputs]





# Test!
def testSMs():
    acc = Accumulator(100)
    acc.transduce([20, 30], verbose=True)

    de = Delay()
    de.transduce([1, 2, 3, 4, 5], verbose=True)

    avg = Average2()
    avg.transduce([1.0, 2.0, 3.0, 4, 5], verbose=True)

    slt = SumLastThree()
    slt.transduce([1, 2, 3, 4, 5, 6, 7], verbose=True)


testSMs()

# Test!
def testCombinators():
    acc1 = Accumulator(0)
    acc2 = Accumulator(0)
    cas = Cascade(acc1, acc2)
    print cas.transduce([1, 2, 3, 4, 5], verbose=True)

    de1 = Delay()
    de2 = Delay()
    decas1 = Cascade(de1, de2)
    print decas1.transduce([1, 2, 3, 4, 5], verbose=False)

    de3 = Delay()
    de4 = Delay()
    decas2 = Cascade(de3, de4)

    decas3 = Cascade(decas1, decas2)
    print decas3.transduce([1, 2, 3, 4, 5], verbose=False)
    

testCombinators()

