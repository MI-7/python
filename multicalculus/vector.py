import math as math

class Vector:
    def __init__(self, v):
        self.v = [x * 1.0 for x in v]
    
    def a(self, i):
        return self.v[i]

    def length(self):
        return math.sqrt(sum([x*x for x in self.v]))

    def dimension(self):
        return len(self.v)

    def dotProduct(self, v2):
        if self.dimension() != v2.dimension():
            print "impossible to perform op on vectors with different dimensions"
        else:
            return sum([x[0] * x[1] for x in zip(self.v, v2.v)])

    def unitVector(self):
        l = self.length()
        return Vector([x / l for x in self.v])

    def componentOf(self, v2):
        return self.dotProduct(v2) / v2.length()

    def isPerpendicularWithErr(self, v2, err=1e-20):
        product = self.dotProduct(v2)
        return product == 0 or product < err

    def __mul__(self, scalar):
        return Vector([x * scalar for x in self.v])

    def __add__(self, v2):
        if self.dimension() != v2.dimension():
            print "impossible to perform op on vectors with different dimensions"
        else:
            return Vector([sum(x) for x in zip(self.v, v2.v)])

    def theta(self, v2):
        if self.dimension() != v2.dimension():
            print "impossible to perform op on vectors with different dimensions"
        else:
            return math.acos(self.dotProduct(v2) / (2 * self.length() * v2.length()))

    def __str__(self):
        return "vector: " + str(self.v)

a=Vector([1,2])
b=Vector([3,4])
print a.dotProduct(b)
print a + b
print a * 2

x=Vector([1, 0])
y=Vector([0, 1])
print x.dotProduct(y)
print math.cos(x.theta(y))
print x.isPerpendicularWithErr(y)

z=Vector([3,4])
print z.unitVector()

print z.componentOf(y)

