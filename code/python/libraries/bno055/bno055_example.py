import smbus
from bno055 import Inclinometer
import time

bus = smbus.SMBus(0)

device_address = 0x29

if not bus:
    raise Exception('I2C bus connection failed!')

sensor=Inclinometer(bus, device_address)

while True:
    print 'Word: ', sensor.get_roll_2()
    print '2 bytes: ', sensor.get_roll(), '\n'
    time.sleep(0.4)
