import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def accumulatorDelay(init):
    return sm.Cascade(sm.R(0), sm.FeedbackAdd(sm.Gain(1), sm.R(init)))
    #return sm.Cascade(sm.FeedbackAdd(sm.Gain(1), sm.R(init)), sm.R(init))
    #return sm.FeedbackAdd(sm.R(init), sm.Gain(1))

f = accumulatorDelay(100)
print f.transduce(range(10))

def accumulator(init):
    return sm.FeedbackAdd(sm.Gain(1), sm.R(init))
e = accumulator(100)
print e.transduce(range(10))

def accumulatorDelayScaled(s, init):
    return sm.Cascade(sm.Cascade(sm.R(0), sm.FeedbackAdd(sm.Gain(1), sm.R(init))), sm.Gain(s))

g = accumulatorDelayScaled(2, 100)
print g.transduce(range(10))
