import smbus
from pca9865 import Servo_controller
import time

bus = smbus.SMBus(0)

device_address = 0x40

if not bus:
    raise Exception('I2C bus connection failed!')

control = Servo_controller(bus, device_address)

id = 4

while True:
    control.move(id,-30)
    time.sleep(3)

    control.move(id, 30)
    time.sleep(3)



