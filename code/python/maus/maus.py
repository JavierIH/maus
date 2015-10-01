import time
import smbus
from hardware.pca9685.pca9685 import ServoController
from hardware.bno055.bno055 import Inclinometer
from control.kinematics.kinematics import MausKinematics
import control.octosnake.octosnake as octosnake


class Maus(object):
    
    def __init__(self, name='maus', i2c_bus=0, servo_trims=[0, 0, 0, 0, 0], servo_pins=[8, 9, 10, 11, 4], pca9685_address=0x40, bno055_address=0x29):
        
        #Configuration
        self._name = name
        self._i2c_bus = i2c_bus
        self._servo_trims = servo_trims
        self._servo_pins = servo_pins
        self._pca9685_address = pca9685_address
        self._bno055_address = bno055_address
    
        #Setting up hardware
        self._bus = smbus.SMBus(self._i2c_bus)
        if not self._bus:
            raise Exception('I2C bus connection failed!')

        self.control = ServoController(self._bus, self._pca9685_address)
        self.sensor = Inclinometer(self._bus, self._bno055_address)
        self.sensor.trim_pitch = -14

        #Setting up OctoSnake
        self.osc = []
        self.osc.append(octosnake.Oscillator())
        self.osc.append(octosnake.Oscillator(octosnake.semiSin))
        self.osc.append(octosnake.Oscillator())
        self.osc.append(octosnake.Oscillator(octosnake.semiSin))
        self.osc.append(octosnake.Oscillator())

        self.osc[1].ref_time = self.osc[0].ref_time
        self.osc[2].ref_time = self.osc[0].ref_time
        self.osc[3].ref_time = self.osc[0].ref_time
        self.osc[4].ref_time = self.osc[0].ref_time

        #Setting up PyKDL
        self.ik = MausKinematics()

        #Setting up servo controller
        for i in range(len(self._servo_pins)):
            self.control.addServo(self._servo_pins[i], self._servo_trims[i])

        self.control.servos[self._servo_pins[1]].reverse = True
        self.control.servos[self._servo_pins[3]].reverse = True


    def walk(self, steps):

        left_x_amp = 20		#millimeters
        right_x_amp = 20	#millimeters
        z_amp = 30		#millimeters
        swing_amp = 70		#degrees
        T = 900                 #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, z_amp, right_x_amp, z_amp, swing_amp]
        offset = [-20, -75, -20, -75, 0]
        phase = [90, 180, 270, 0, 335+90]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]
 
        final = time.time() +float(T*steps/1000) 
        while time.time() < final:
            try:
                roll_data=self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output+roll_data)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)

    def slowWalk(self, steps):

        left_x_amp = 20         #millimeters
        right_x_amp = 20        #millimeters
        z_amp = 60              #millimeters
        swing_amp = 100          #degrees
        T = 5000                 #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, z_amp, right_x_amp, z_amp, swing_amp]
        offset = [-20, -80, -20, -80, 0]
        phase = [90, 180, 270, 0, 90]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]

        final = time.time() +float(T*steps/1000)
        while time.time() < final:
            try:
                roll_data=self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output+roll_data)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)



    def run(self, steps):

        left_x_amp = 10         #millimeters
        right_x_amp = 10        #millimeters
        z_amp = 20              #millimeters
        swing_amp = 0          #degrees
        T = 150                 #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, z_amp, right_x_amp, z_amp, swing_amp]
        offset = [-20, -60, -20, -60, 0]
        phase = [0, 270, 0, 270, 0]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]

        final = time.time() +float(T*steps/1000)
        while time.time() < final:
            try:
                roll_data=self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)


    def walkBackwards(self, steps):

        left_x_amp = 20         #millimeters
        right_x_amp = 20        #millimeters
        z_amp = 30              #millimeters
        swing_amp = 70          #degrees
        T = 900                #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, z_amp, right_x_amp, z_amp, swing_amp]
        offset = [-20, -75, -20, -75, 0]
        phase = [90, 0, 270, 180, 335-90]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]

        final = time.time() +float(T*steps/1000)
        while time.time() < final:
            try:
                roll_data=0#self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output-0.5*roll_data)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)

    def turnLeft(self, steps):

        left_x_amp = 0         #millimeters
        right_x_amp = 20        #millimeters
        z_amp = 30              #millimeters
        swing_amp = 70          #degrees
        T = 900                #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, 0, right_x_amp, z_amp, swing_amp]
        offset = [-20, -75, -20, -75, 0]
        phase = [90, 180, 270, 0, 335+90]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]

        final = time.time() +float(T*steps/1000)
        while time.time() < final:
            try:
                roll_data=0#self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output-0.5*roll_data)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)

    def turnRight(self, steps):

        left_x_amp = 20         #millimeters
        right_x_amp = 0        #millimeters
        z_amp = 30              #millimeters
        swing_amp = 70          #degrees
        T = 900                #milliseconds 

        period = [T, T, T, T, T]
        amplitude = [left_x_amp, z_amp, right_x_amp, 0, swing_amp]
        offset = [-20, -75, -20, -75, 0]
        phase = [90, 180, 270, 0, 335+90]

        for i in range(len(self.osc)):
            self.osc[i].period = period[i]
            self.osc[i].amplitude = amplitude[i]
            self.osc[i].phase = phase[i]
            self.osc[i].offset = offset[i]

        final = time.time() +float(T*steps/1000)
        while time.time() < final:
            try:
                roll_data=0#self.sensor.getRoll()
                for i in range(len(self.osc)):
                    self.osc[i].refresh()

                left_joints = self.ik.getJoints(self.osc[0].output, 0, self.osc[1].output-roll_data/7)
                right_joints = self.ik.getJoints(self.osc[2].output, 0, self.osc[3].output+roll_data/7)
                self.control.move(self._servo_pins[0], left_joints[0])
                self.control.move(self._servo_pins[1], right_joints[0])
                self.control.move(self._servo_pins[2], left_joints[1])
                self.control.move(self._servo_pins[3], right_joints[1])
                self.control.move(self._servo_pins[4], self.osc[4].output-0.5*roll_data)

            except IOError:
                self._bus = smbus.SMBus(self._i2c_bus)


    #def jump(self):

    def moveJoints(self, joint_target, execution_time=0, sample_time=18):
        if execution_time > sample_time:
            increment = []
            initial_position = []
            for i in range(len(self._servo_pins)):
                initial_position.append(self.control.getPosition(self._servo_pins[i]))
                increment.append(float(joint_target[i] - initial_position[i]) / (execution_time / sample_time))

            final_time = time.time()*1000 + execution_time

            iteration = 1
            while time.time()*1000 < final_time:
                partial_time = time.time()*1000 + sample_time
                for i in range(len(self._servo_pins)):
                    self.control.move(self._servo_pins[i], initial_position[i] + (iteration * increment[i]))

                iteration += 1
                while (time.time()*1000 < partial_time):
                    pass
        else:
            for i in range(len(self._servo_pins)):
                self.control.move(self._servo_pins[i], joint_target[i])

    def moveCart(self, x_left, z_left, x_right, z_right):
        pass

    def zero(self):
        for i in range(len(self._servo_pins)):
            self.control.move(self._servo_pins[i], 0)

    def sleep(self):
	self.control.sleep()
