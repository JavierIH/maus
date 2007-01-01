import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maus.maus import Maus
import time

print 'yyeeyyeye'

maus = Maus(servo_trims=[-15, 8, 0, -18, 15])

print 'uouououou'
maus.walk(300)
#maus.run(10)
#maus.turnLeft(10)
#maus.walk(30)
#maus.turnLeft(30)
#maus.moveJoints([45,45,-45,-45,0],3000)
#maus.walkBackwards(10)

maus.zero()
maus.moveJoints([90,90,-90,-90,0],1000)
maus.sleep()
maus.sleep()
maus.sleep()
maus.sleep()

print 'TA-DAAHHHHHHH!!!!!!'
