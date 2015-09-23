import time
import libraries.octosnake.octosnake as octosnake
import smbus
from libraries.pca9865.pca9865 import ServoController
from libraries.bno055.bno055 import Inclinometer

#AMP=25
#servo1 = octosnake.Oscillator(1600, AMP, 0, -45, -15)
#servo2 = octosnake.Oscillator(1600, AMP, 0, 45, 8)
#servo3 = octosnake.Oscillator(1600, AMP, 90, 30, 0)
#servo4 = octosnake.Oscillator(1600, AMP, 90, -30, -18)
#servo5 = octosnake.Oscillator(1600, 110, 180, 0, 21)

#AMP=25
#T=1000
#servo1 = octosnake.Oscillator(T, AMP, 0, -60, -15)
#servo2 = octosnake.Oscillator(T, AMP, 0, 60, 8)
#servo3 = octosnake.Oscillator(T, AMP, 90, 30, 0)
#servo4 = octosnake.Oscillator(T, AMP, 90, -30, -18)
#servo5 = octosnake.Oscillator(T, 60, 220, 0, 21)

AMP=25
T=1000
ajuste = 0

osc=[] 

osc.append(octosnake.Oscillator(T, AMP, 0, -60))
osc.append(octosnake.Oscillator(T, AMP, 0, 60))
osc.append(octosnake.Oscillator(T, AMP, 90, 30))
osc.append(octosnake.Oscillator(T, AMP, 180, -30))
osc.append(octosnake.Oscillator(T, 60, 190, 0))

osc[1].ref_time = osc[0].ref_time
osc[2].ref_time = osc[0].ref_time
osc[3].ref_time = osc[0].ref_time
osc[4].ref_time = osc[0].ref_time

bus = smbus.SMBus(0)

pca9865_address = 0x40
bno055_address = 0x29

if not bus:
    raise Exception('I2C bus connection failed!')

control=ServoController(bus, pca9865_address)
sensor=Inclinometer(bus, bno055_address)

control.addServo(8, -15)
control.addServo(9, 8)
control.addServo(10, 0)
control.addServo(11, -18)
control.addServo(4, 21)

def test():
	ref=time.time()
	while True:
		for i in range(len(osc)):
                    osc[i].refresh()
                
 		try:
                        roll_data = 0#sensor.get_roll()
			control.move(8, osc[0].output - roll_data/2)
			control.move(9, osc[1].output - roll_data/2)
			control.move(10, osc[2].output + roll_data/2)
                	control.move(11, osc[3].output + roll_data/2)
			control.move(4, osc[4].output)# - roll_data*3)
                        #print roll_data, '\t', pitch_data
		except IOError:
			bus = smbus.SMBus(0)
			#print '\n'*8, '------------- I2C reiniciado -------------'

		#print 'Servo 1:  ' + str(position1) + '    \t Servo 2: ' + str(position2) + '    \t Servo 3: ' + str(position3) + '    \t Servo 4: '  + str(position4)
		#time.sleep(1)

#test()
