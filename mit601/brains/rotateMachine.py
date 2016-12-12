import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io
from __builtin__ import False

class RotateTSM(sm.SM):
    rotationGain = 3.0
    angleEpsilon = 0.01
    startState = 'start'
    
    def __init__(self, headingDelta):
        self.headingDelta = headingDelta
    
    def getNextValues(self, state, inp):
        currentTheta = inp.odometry.theta
        
        if state == 'start':
            thetaDesired = util.fixAnglePlusMinusPi(currentTheta + self.headingDelta)
        else:
            (thetaDesired, thetaLast) = state
        
        newState = (thetaDesired, currentTheta)
        rotation = self.rotationGain * util.fixAnglePlusMinusPi(thetaDesired - currentTheta)
        print "NewState: ", newState, " rvel: ", rotation
        return (newState, io.Action(rvel = rotation))
    
    def done(self, state):
        if state == 'start':
            return False
        else:
            (thetaDesired, thetaLast) = state
            return util.nearAngle(thetaDesired, thetaLast, self.angleEpsilon)

class ForwardTSM(sm.SM):
    forwardGain = 1.0
    distTargetEpsilon = 0.01
    startState = 'start'
    
    def __init__(self, delta):
        self.deltaDesired = delta
    
    def getNextValues(self, state, inp):
        currentPos = inp.odometry.point()
        if state == 'start':
            startPos = currentPos
        else:
            (startPos, lastPos) = state
        
        newState = (startPos, currentPos)
        error = self.deltaDesired - startPos.distance(currentPos)
        forward = error * self.forwardGain
        print "forward: ", forward, "currentpos: ", currentPos
        return (newState, io.Action(fvel = forward))
    
    def done(self, state):
        if state == 'start':
            return False
        else:
            (startPos, lastPos) = state
            return util.within(startPos.distance(lastPos), self.deltaDesired, self.distTargetEpsilon)

class XYDriver(sm.SM):
    forwardGain = 2.0
    rotationGain = 2.0
    angleEps = 0.05
    distEps = 0.02
    startState = False
    
    def getNextValues(self, state, inp):
        (goalPoint, sensors) = inp
        robotPos = sensors.odometry
        robotPoint = robotPos.point()
        robotTheta = robotPos.theta
        
        if goalPoint == None:
            return (True, io.Action())
        
        headingTheta = robotPoint.angleTo(goalPoint)
        if util.nearAngle(robotTheta, headingTheta, self.angleEps):
            r = robotPoint.distance(goalPoint)
            if r < self.distEps:
                return (True, io.Action())
            else:
                return (False, io.Action(fvel = r * self.forwardGain))
        else:
            headingError = util.fixAnglePlusMinusPi(headingTheta - robotTheta)
            return (False, io.Action(rvel = headingError * self.rotationGain))
    
    def done(self, state):
        return state
        

class SpyroGyra(sm.SM):
    distEps = 0.02
    def __init__(self, incr):
        self.incr = incr
        self.startState = ('south', 0, None)
    
    def getNextValues(self, state, inp):
        (direction, length, subGoal) = state
        robotPos = inp.odometry
        robotPoint = robotPos.point()
        if subGoal == None:
            subGoal = robotPoint
        
        if robotPoint.isNear(subGoal, self.distEps):
            length = length + self.incr
            if direction == 'east':
                direction = 'north'
                subGoal.y += length
            elif direction == 'north':
                direction = 'west'
                subGoal.x -= length
            elif direction == 'west':
                direction = 'south'
                subGoal.y -= length
            else:
                direction = 'east'
                subGoal.x += length
            
            print 'new:', direction, length, subGoal
        
        return ((direction, length, subGoal), (subGoal, inp))

class StopStopStop(sm.SM):
    def getNextValues(self, state, inp):
        return (True, io.Action)
    
    def done(self, state):
        return state

#mySM = RotateTSM(1)
#mySM.name = 'rotateSM'

#mySM = ForwardTSM(2.0)
#mySM.name = "forwardSM"

mySM = sm.Cascade(SpyroGyra(0.5), sm.Switch(lambda inp: (inp[1].sonars[3]+inp[1].sonars[4])/2 < 4, StopStopStop(), XYDriver()))
mySM.name = "spiral"

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=True) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
