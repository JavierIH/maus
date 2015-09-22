import smbus
from pca9865 import ServoController
import time

bus = smbus.SMBus(0)

device_address = 0x40

if not bus:
    raise Exception('I2C bus connection failed!')

servo_id = 4
servo_trim = 21

control = ServoController(bus, device_address)
control.addServo(servo_id, servo_trim)

while True:
    control.move(servo_id, 20)
    time.sleep(3)

    control.move(servo_id, -20)
    time.sleep(3)



