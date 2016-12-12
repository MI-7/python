undef = 'undefined'

def isUndef(v):
    if v == undef:
        return True
    else:
        return False

def splitValue(v, n):
    if isUndef(v):
        return (undef,) * n
    else:
        return v

def safeAdd(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 + i2

def safeMultiply(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 * i2

def safeDivide(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 / i2

def safeSubtract(i1, i2):
    if isUndef(i1) or isUndef(i2):
        return undef
    else:
        return i1 - i2
