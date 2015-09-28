import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__).replace('examples/bno055','')))

import smbus
from hardware.bno055.bno055 import Inclinometer
import time

bus = smbus.SMBus(0)

device_address = 0x29

if not bus:
    raise Exception('I2C bus connection failed!')

sensor=Inclinometer(bus, device_address)

while True:
    print 'Pitch: ', sensor.getPitch(), '\tRoll: ', sensor.getRoll(), '\tYaw: ', sensor.getYaw()     
    time.sleep(0.1)
