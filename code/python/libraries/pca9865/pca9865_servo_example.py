import smbus
from pca9865 import servo_controller
import time

bus = smbus.SMBus(0)

device_address = 0x40

if not bus:
    raise Exception('I2C bus connection failed!')

control=servo_controller(bus, device_address)

while True:
    control.move(5,-45)
    time.sleep(3)
    control.move(5, 45)
    time.sleep(3)


