import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from maus.maus import Maus
import time

maus = Maus(servo_trims=[-15, 8, 0, -18, 21])
#maus.run(1)
#maus.zero()
#time.sleep(2)
t=2000
while True:
    maus.moveJoints([70,70,-70,-70,0],3000)
    maus.moveJoints([50,50,-50,-50,0],3000)
time.sleep(1)
maus.sleep()

print 'TA-DAAHHHHHHH!!!!!!'
