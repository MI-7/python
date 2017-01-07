import lib601.sig  as sig # Signal
import lib601.ts as ts  # TransducedSignal
import lib601.sm as sm  # SM

######################################################################
##  Make a state machine model using primitives and combinators
######################################################################

def plant(T, initD):
    return sm.Cascade(sm.Cascade(sm.Gain(-1 * T), sm.R(initD)), sm.FeedbackAdd(sm.Gain(1), sm.R(initD)))

def controller(k):
    return sm.Gain(k)

def sensor(initD):
    return sm.R(initD)

def wallFinderSystem(T, initD, k):
    p = plant(T, initD)
    c = controller(k)
    m1 = sm.Cascade(c, p)
    m2 = sensor(initD)
    return sm.FeedbackSubtract(m1, m2)
    

# Plots the sequence of distances when the robot starts at distance
# initD from the wall, and desires to be at distance 0.7 m.  Time step
# is 0.1 s.  Parameter k is the gain;  end specifies how many steps to
# plot. 

initD = 1.5

def plotD(k, end = 50):
  d = ts.TransducedSignal(sig.ConstantSignal(0.7),
                          wallFinderSystem(0.1, initD, k))
  d.plot(0, end, newWindow = 'Gain '+str(k))

plotD(-20)
plotD(-10)
plotD(-5)
plotD(-2)
plotD(-1)
plotD(-0.5)
plotD(-0.25)
plotD(0.25)
plotD(0.5)
plotD(0.75)
plotD(1)
plotD(10)

