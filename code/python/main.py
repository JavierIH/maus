import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maus.maus import Maus
import time

maus = Maus(servo_trims=[-12, 8, -3, -18, 15])#[-15, 8, 0, -18, 15])
maus.walk(500)
maus.run(10)
#maus.zero()
#time.sleep(2)
#time.sleep(1)
#maus.sleep()

maus.turnLeft(10)
maus.turnRight(10)
maus.moveJoints([45,45,-45,-45,0],3000)
maus.walkBackwards(10)

maus.zero()
maus.moveJoints([90,90,-90,-90,0],1000)
maus.sleep()
maus.sleep()
maus.sleep()
maus.sleep()

print 'TA-DAAHHHHHHH!!!!!!'
