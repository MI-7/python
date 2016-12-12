from ch4_mysm import *
from ch4_myutility import *

class Cascade(MySM):
    def __init__(self, sm_in, sm_out):
        self.sm_in = sm_in
        self.sm_out = sm_out
        self.startState = (sm_in.startState, sm_out.startState)

    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = splitValue(state, 2)
        (news1, o1) = self.sm_in.getNextValues(s1, inp, verbose)
        (news2, o2) = self.sm_out.getNextValues(s2, o1, verbose)
        if verbose:
            print 'Cascade..', ' next state: ', (news1, news2)
        return ((news1, news2), o2)

class TripleCascade(MySM):
    def __init__(self, sm1, sm2, sm3):
        self.sm1 = sm1
        self.sm2 = sm2
        self.sm3 = sm3
        self.startState = (sm1.startState, sm2.startState, sm3.startState)

    def getNextValues(self, state, inp, verbose=False):
        (s1, s2, s3) = splitValue(state, 3)
        (news1, o1) = self.sm1.getNextValues(s1, inp, verbose)
        (news2, o2) = self.sm2.getNextValues(s2, o1, verbose)
        (news3, o3) = self.sm3.getNextValues(s3, o2, verbose)
        if verbose:
            print 'Triple Cascade', ' next state: ', (news1, news2, news3)
        return ((news1, news2, news3), o3)

class Parallel(MySM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (sm1.startState, sm2.startState)

    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = state
        (news1, o1) = self.sm1.getNextValues(s1, inp, verbose)
        (news2, o2) = self.sm2.getNextValues(s2, inp, verbose)
        return ((news1, news2), (o1, o2))

class Parallel2(MySM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (sm1.startState, sm2.startState)

    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = state
        (i1, i2) = splitValue(inp)
        (news1, o1) = self.sm1.getNextValues(s1, i1)
        (news2, o2) = self.sm2.getNextValues(s2, i2)
        return ((news1, news2), (o1, o2))

class ParallelAdd(MySM):
    def __init__(self, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.startState = (sm1.startState, sm2.startState)

    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = state
        (news1, o1) = self.sm1.getNextValues(s1, inp)
        (news2, o2) = self.sm2.getNextValues(s2, inp)
        return ((news1, news2), safeAdd(o1, o2))

class Feedback(MySM):
    def __init__(self, sm):
        self.sm = sm
        self.startState = sm.startState

    def getNextValues(self, state, inp, verbose=False):
        if verbose:
            print 'Feedback..', ' In: ', inp
        (ignore, o) = self.sm.getNextValues(state, undef, verbose)
        (news, ignore) = self.sm.getNextValues(state, o, verbose)
        #(news, o) = self.sm.getNextValues(state, inp, verbose)
        return (news, o)

class Feedback2(MySM):
    def __init__(self, sm):
        self.sm = sm
        self.startState = sm.startState
    def getNextValues(self, state, inp, verbose=False):
        if verbose:
            print 'Feedback 2..', ' In: ', inp
        (ignore, o) = self.sm.getNextValues(state, (inp, undef))
        (news, ignore) = self.sm.getNextValues(state, (inp, o))
        return (news, o)

class Switch(MySM):
    def __init__(self, condition, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.condition = condition
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = splitValue(state, 2)
        if self.condition(inp):
            (ns1, o) = self.sm1.getNextValues(s1, inp, verbose)
            return ((ns1, s2), o)
        else:
            (ns2, o) = self.sm2.getNextValues(s2, inp, verbose)
            return ((s1, ns2), o)

class Multiplex(MySM):
    def __init__(self, condition, sm1, sm2):
        self.sm1 = sm1
        self.sm2 = sm2
        self.condition = condition
        self.startState = (sm1.startState, sm2.startState)
    def getNextValues(self, state, inp, verbose=False):
        (s1, s2) = splitValue(state, 2)
        (ns1, o1) = self.sm1.getNextValues(s1, inp)
        (ns2, o2) = self.sm2.getNextValues(s2, inp)
        if self.condition(inp):
            return ((ns1, ns2), o1)
        else:
            return ((ns1, ns2), o2)

class Repeat(MySM):
    def __init__(self, sm, n = None):
        self.sm = sm
        self.n = n
        self.startState = (0, sm.startState)
    def advanceIfDone(self, counter, smState):
        pass