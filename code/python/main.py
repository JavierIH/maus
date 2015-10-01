import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maus.maus import Maus
import time

maus = Maus(servo_trims=[-15, 8, 0, -18, 21])
maus.run(30)
#maus.zero()
#time.sleep(2)
#time.sleep(1)
#maus.sleep()

maus.turnLeft(10)
maus.walkBackwards(20)

maus.zero()
maus.moveJoints([90,90,-90,-90,0],1000)
maus.sleep()
maus.sleep()
maus.sleep()
maus.sleep()

print 'TA-DAAHHHHHHH!!!!!!'
