import lib601.poly as poly
import lib601.sig
from lib601.sig import *

## You can evaluate expressions that use any of the classes or
## functions from the sig module (Signals class, etc.).  You do not
## need to prefix them with "sig."


s = UnitSampleSignal()
#s.plot(-5, 5)

class MyStepSignal(Signal):
    def sample(self, n):
        if n < 0:
            return 0
        else:
            return 1

step = MyStepSignal()
#step.plot(-5, 5)

class MySummedSignal(Signal):
    def __init__(self, m1, m2):
        self.m1 = m1
        self.m2 = m2
    
    def sample(self, n):
        return self.m1.sample(n) + self.m2.sample(n)

summ = MySummedSignal(MyStepSignal(), MyStepSignal())
#summ.plot(-5, 5)

class MyScaledSignal(Signal):
    def __init__(self, s, c):
        self.s = s
        self.c = c

    def sample(self, n):
        return self.s.sample(n) * self.c

scale = MyScaledSignal(MyStepSignal(), 0)
#scale.plot(-5, 5)

class MyR(Signal):
    def __init__(self, s):
        self.s = s

    def sample(self, n):
        return self.s.sample(n-1)

mydelay = MyR(MyStepSignal())
#mydelay.plot(-5, 5)

class MyRn(Signal):
    def __init__(self, s, N):
        self.s = s
        self.N = N

    def sample(self, n):
        return self.s.sample(n - self.N)

mydelayN = MyRn(MyStepSignal(), 3)
#mydelayN.plot(-5, 5)

class MyPolynomial():
    def __init__(self, coeffs):
        self.coeffs = coeffs

    def coeff(self, i):
        return coeffs[i]

def myPolyR(s, p):
    x = None
    for idx in range(len(p.coeffs)):
        if p.coeffs[idx] != 0:
            sig = MyScaledSignal(MyRn(s, idx), p.coeffs[len(p.coeffs) - 1 - idx])
            if x == None:
                x = sig
            else:
                x = MySummedSignal(x, sig)

    return x

mypoly = MyPolynomial([7, 0, 1])
mypolyR = myPolyR(MyStepSignal(), mypoly)
#mypolyR.plot(-5, 5)

mitpolyR = polyR(StepSignal(), poly.Polynomial([7, 0, 1]))
#mitpolyR.plot(-5, 5)


step1 = ScaledSignal(Rn(StepSignal(), 3), 3.0)
#step1.plot(-10, 10)

step2 = ScaledSignal(Rn(StepSignal(), 7), -3.0)
#step2.plot(-10, 10)

stepUpDown = SummedSignal(step1, step2)
#stepUpDown.plot(-10, 10)

stepUpDownPoly = polyR(UnitSampleSignal(), poly.Polynomial([5.0, 0, 3.0, 0, 1.0, 0]))
stepUpDownPoly.plot(-10, 10)
