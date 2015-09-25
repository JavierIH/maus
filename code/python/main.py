import time
import smbus
from libraries.pca9865.pca9865 import ServoController
from libraries.bno055.bno055 import Inclinometer
from control.kinematics.kinematics import MausKinematics
import control.octosnake.octosnake as octosnake

osc = []
xamp_left = 10 
xamp_right = 20
zamp = 30
T=1000
osc.append(octosnake.Oscillator(T, xamp_left, 0, -20))
osc.append(octosnake.SemiSine(T, zamp, 90, -75))
osc.append(octosnake.Oscillator(T, xamp_right, 180, -20))
osc.append(octosnake.SemiSine(T, zamp, 270, -75))
osc.append(octosnake.Oscillator(T, 70, 335, 0))
#osc.append(octosnake.Oscillator(T*14, 10, 0, 10))


osc[1].ref_time = osc[0].ref_time
osc[2].ref_time = osc[0].ref_time
osc[3].ref_time = osc[0].ref_time
osc[4].ref_time = osc[0].ref_time


bus = smbus.SMBus(0)

pca9865_address = 0x40
bno055_address = 0x29

if not bus:
    raise Exception('I2C bus connection failed!')

sensor=Inclinometer(bus, bno055_address)
control=ServoController(bus, pca9865_address)

ik = MausKinematics()

control.addServo(8, -15)
control.addServo(9, 8)
control.addServo(10, 0)
control.addServo(11, -18)
control.addServo(4, 21)

control.servos[9].reverse = True
control.servos[11].reverse = True


def test():
    #var_phase = 250
    while True:
	roll=sensor.getRoll()
        for i in range(len(osc)):
            osc[i].refresh()
        try:
            left_joints = ik.getJoints(osc[0].output, 0, osc[1].output-roll/7)
            right_joints = ik.getJoints(osc[2].output, 0, osc[3].output+roll/7)
            control.move(8, left_joints[0])
            control.move(10, left_joints[1])
            control.move(9, right_joints[0])
            control.move(11, right_joints[1])
            control.move(4, osc[4].output - 0.5*sensor.getRoll())
            
            #var_phase+=0.1
            #osc[4].phase=var_phase
            #print '\n\n\nleft: ', osc[0].output, '\tq0: ', left_joints[0], '\tq1', left_joints[1]
            #print 'right: ', osc[2].output, '\tq0: ', right_joints[0], '\tq1', right_joints[1]
            #print 'phase: ', osc[4].phase

        except IOError:
            bus = smbus.SMBus(0)
		#print '\n'*8, '------------- I2C reiniciado -------------'

		#print 'Servo 1:  ' + str(position1) + '    \t Servo 2: ' + str(position2) + '    \t Servo 3: ' + str(position3) + '    \t Servo 4: '  + str(position4)
		#time.sleep(1)

test()
#control.sleep()
