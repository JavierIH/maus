import time 
import octosnake
import smbus
from pca9865 import Servo_controller

#Caminata estatica
AMP=25
servo1 = octosnake.Oscillator(1600, AMP, 0, -45, -15)
servo2 = octosnake.Oscillator(1600, AMP, 0, 45, 8)
servo3 = octosnake.Oscillator(1600, AMP, 90, 30, 0)
servo4 = octosnake.Oscillator(1600, AMP, 90, -30, -18)
servo5 = octosnake.Oscillator(1600, 110, 180, 0, 21)



servo2.ref_time = servo1.ref_time
servo3.ref_time = servo1.ref_time
servo4.ref_time = servo1.ref_time
servo5.ref_time = servo1.ref_time

bus = smbus.SMBus(0)

device_address = 0x40

if not bus:
	raise Exception('I2C bus connection failed!')

control=Servo_controller(bus, device_address)

def test():
	ref=time.time()
	while True:
		position1 = servo1.refresh()
                position2 = servo2.refresh()
                position3 = servo3.refresh()
		position4 = servo4.refresh()
		position5 = servo5.refresh()

 		try:
			control.move(8, position1)
			control.move(9, position2)
			control.move(10, position3)
                	control.move(11, position4)
			control.move(4, position5)
		except IOError:
			bus = smbus.SMBus(0)
			print '\n'*8, '------------- I2C reiniciado -------------'

		print 'Servo 1:  ' + str(position1) + '    \t Servo 2: ' + str(position2) + '    \t Servo 3: ' + str(position3) + '    \t Servo 4: '  + str(position4)
		#time.sleep(0.1)



