class Servo_controller:

    def __init__(self, bus, address, servo_min=150, servo_max=550, servo_amp=180):
        
	self.address = address
	self.servo_min = servo_min
	self.servo_max = servo_max
	self.servo_inc = (servo_max-servo_min)/servo_amp
	self.servo_zero = (servo_max+servo_min)/2
	self.bus = bus
        
        #configuration
        self.bus.write_byte_data(self.address, 0x00, 0x10)
        self.bus.write_byte_data(self.address, 0xfe, 0x64)
        self.bus.write_byte_data(self.address, 0x00, 0x00)

    def move(self, id, position):
        position = int(self.servo_zero+position*self.servo_inc)
        self.bus.write_byte_data(self.address, id*4+6, 0)
        self.bus.write_byte_data(self.address, id*4+7, 0)
        self.bus.write_byte_data(self.address, id*4+8, position)
        self.bus.write_byte_data(self.address, id*4+9, position >> 8)
	
    def sleep(self):
	self.bus.write_byte_data(self.address, 0x00, 0x10)
        self.bus.write_byte_data(self.address, 0x00, 0x00)
