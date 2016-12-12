from ch4_mysm import *
from ch4_mycombinators import *

# Test!
def testSMs():
    acc = Accumulator(100)
    acc.transduce([undef, 20, 30], verbose=True)

    de = Delay()
    de.transduce([1, 2, 3, undef, 4, 5], verbose=True)

    avg = Average2()
    avg.transduce([1.0, 2.0, undef, 3.0, 4, 5], verbose=True)

    slt = SumLastThree()
    slt.transduce([1, 2, 3, undef, 4, 5, 6, 7], verbose=True)


#testSMs()

# Test!
def testCombinators():
    acc1 = Accumulator(0)
    acc2 = Accumulator(0)
    cas = Cascade(acc1, acc2)
    cas.transduce([1, 2, undef, 3, 4, 5], verbose=True)

    de1 = Delay()
    de2 = Delay()
    decas1 = Cascade(de1, de2)
    print decas1.transduce([1, 2, undef, 3, 4, 5], verbose=True)

    de3 = Delay()
    de4 = Delay()
    decas2 = Cascade(de3, de4)

    decas3 = Cascade(decas1, decas2)
    print decas3.transduce([1, 2, undef, 3, 4, 5], verbose=True)

    acc5 = Accumulator(0)
    acc6 = Accumulator(0)
    para1_1 = Parallel(acc5, acc6)
    print para1_1.transduce([1, 2, undef, 3, 4, 5], verbose=True)

    acc3 = Accumulator(0)
    acc4 = Accumulator(0)
    para2_1 = Parallel2(acc3, acc4)
    print para2_1.transduce([(1, 2), (2, 3), (undef, undef), (3, 4), (4, 5), (5, 6)], verbose=True)

#testCombinators()

def testFeedback():
    counter = Feedback(Cascade(Increment(2), Delay(3)))
    #counter.run(verbose=True)

    fibonacci = Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(1), Delay(0))), Adder()))
    print fibonacci.run(verbose=False)

    fibonacci2 = Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(0), Delay(0))), Adder()))
    print fibonacci2.run(verbose=False)

    nodelay = Feedback(Increment(2))
    print nodelay.run(verbose=False)
    #print nodelay.transduce([1, 2, 3, 4, 5])

    fib3 = Feedback(Cascade(Cascade(Parallel(Delay(1), Cascade(Delay(1), Delay(0))), Adder()), Delay(1)))
    #print fib3.run(verbose=False)

    fib2 = Feedback(Cascade(Parallel(
                                        Cascade(Delay(1), Delay(1)),
                                        Cascade(Cascade(Delay(1), Delay(0)), Delay(0))
                                            ),
                                    Adder()
                                    ))
    #print fib2.run(verbose=False)

    fib4 = Feedback(Cascade(Parallel(
                                    Delay(1),
                                    Cascade(Cascade(Delay(0), Delay(0)), Delay(0))),
                            Adder()
                            )
                    )
    #print fib4.run(verbose=False)

    dd = DoubleDelay((0, 0))
    #print dd.transduce([1, 2, 3, 4, 5], verbose=False)

    fib5 = Feedback(Cascade(Parallel(Delay(1), DoubleDelay((0, 1))), Adder()))
    #print fib5.run(verbose=False)

    fib6 = Feedback(Cascade(Parallel(Delay(1), Cascade(DoubleDelay((0, 1)), Delay(0))), Adder()))
    #print fib6.run(verbose=False)

    fib7 = Feedback(Cascade(Parallel(DoubleDelay((1, 1)), Cascade(DoubleDelay((0, 1)), Delay(0))), Adder()))
    #print fib7.run(verbose=False)

    ddd = TripleDelay((1, 2, 3))
    #print ddd.transduce([4, 5, 6, 7, 8, 9], verbose=False)

    fib8 = Feedback(Cascade(Parallel(DoubleDelay((1, 1)), TripleDelay((0, 0, 1))), Adder()))
    #print fib8.run(verbose=False)

    fib9 = Feedback(Cascade(Parallel(DoubleDelay((0, 0)), TripleDelay((1, 1, 1))), Adder()))
    #print fib9.run(verbose=False)

    fib10 = Feedback(Cascade(Parallel(Delay(1), TripleCascade(Delay(1), Delay(0), Delay(0))), Adder()))
    #print fib10.run(verbose=False)

    #2 ** n
    nfactor = Feedback(Cascade(Parallel(Delay(1), Constant(2)), Multiplier()))
    print nfactor.run(verbose=False)

    #square each step
    ex49 = Feedback(Cascade(Parallel(Delay(3), Delay(3)), Multiplier()))
    print ex49.run(verbose=False)

    #double each step
    ex48 = Feedback(Cascade(Parallel(Delay(3), Constant(2)), Multiplier()))
    print ex48.run(verbose=False)

    #try fib with wire
    ex47 = Feedback(Cascade(Parallel(Delay(1), Cascade(Delay(0), Wire())), Adder()))
    print ex47.run(verbose=False)

    #factorial n!
    figure49 = Cascade(Feedback(Cascade(Increment(1), Delay(1))), Feedback2(Cascade(Multiplier(), Delay(1))))
    print figure49.transduce(range(10))

    ex411_m1 = Switch(lambda inp: inp>100, Accumulator(0), Accumulator(0))
    ex411_m2 = Multiplex(lambda inp: inp>100, Accumulator(0), Accumulator(0))
    print ex411_m1.transduce([2,3,4,200,300,400,1,2,3])
    print ex411_m2.transduce([2,3,4,200,300,400,1,2,3])
    
testFeedback()
