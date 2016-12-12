import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# Wall stop state machine
# input = io.SensorInput()[0] - [7]
# next state = K * (D_desired - inp[3])
# 

k = -0.1
dDesired = 2.5

class WallStopController(sm.SM):
    def getNextValues(self, state, inp):
        sminput = ''
        print inp
        if inp=='undefined':
            sminput = 'undefined'
        else:
            sminput = inp.sonars[3]
        
        fv = sm.safeMul(k, sm.safeAdd(dDesired, sm.safeMul(-1, sminput)))
        rv = 0.0
        print 'fvel..', fv, 'rvel..', rv
        action = io.Action(fvel = fv, rvel = rv)
        return (action, action)

#deltaT = 0.1
#class WallWorld(sm.SM):
#    startState = 5
#    def getNextValues(self, state, inp):
#        sminput = ''
#        print inp
#        if inp == 'undefined':
#            sminput = inp
#        else:
#            sminput = inp.sonars[3]
#        
#        news = sm.safeAdd(state, safeMul(safeMul(-1, deltaT), sminput))
#        print 'news..', news, 'olds..', state
#        return (news, state)

mySM = WallStopController()#sm.Feedback(sm.Cascade(WallStopController(), WallWorld()))
mySM.name = 'WallStopSM'

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
    # print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
