import time 
import libraries.octosnake.octosnake as octosnake
import smbus
from libraries.pca9865.pca9865 import Servo_controller
from libraries.bno055.bno055 import Inclinometer


calibration=0

#AMP=25
#servo1 = octosnake.Oscillator(1600, AMP, 0, -45, -15)
#servo2 = octosnake.Oscillator(1600, AMP, 0, 45, 8)
#servo3 = octosnake.Oscillator(1600, AMP, 90, 30, 0)
#servo4 = octosnake.Oscillator(1600, AMP, 90, -30, -18)
#servo5 = octosnake.Oscillator(1600, 110, 180, 0, 21)

AMP=25
T=1000
servo1 = octosnake.Oscillator(T, AMP, 0, -60-calibration, -15)
servo2 = octosnake.Oscillator(T, AMP, 0, 60+calibration, 8)
servo3 = octosnake.Oscillator(T, AMP, 90, 30-calibration, 0)
servo4 = octosnake.Oscillator(T, AMP, 90, -30+calibration, -18)
servo5 = octosnake.Oscillator(T, 60, 220, 0, 21)

servo2.ref_time = servo1.ref_time
servo3.ref_time = servo1.ref_time
servo4.ref_time = servo1.ref_time
servo5.ref_time = servo1.ref_time

bus = smbus.SMBus(0)

pca9865_address = 0x40
bno055_address = 0x29

if not bus:
    raise Exception('I2C bus connection failed!')

control=Servo_controller(bus, pca9865_address)
sensor=Inclinometer(bus, bno055_address)

def test():
	ref=time.time()
	while True:
		position1 = servo1.refresh()
                position2 = servo2.refresh()
                position3 = servo3.refresh()
		position4 = servo4.refresh()
		position5 = servo5.refresh()

 		try:
                        data = sensor.get_roll()
			control.move(8, position1 - data/2)
			control.move(9, position2 - data/2)
			control.move(10, position3 + data/2)
                	control.move(11, position4 + data/2)
			control.move(4, position5 - data*3)
                        print data
		except IOError:
			bus = smbus.SMBus(0)
			#print '\n'*8, '------------- I2C reiniciado -------------'

		#print 'Servo 1:  ' + str(position1) + '    \t Servo 2: ' + str(position2) + '    \t Servo 3: ' + str(position3) + '    \t Servo 4: '  + str(position4)
		#time.sleep(1)

test()
