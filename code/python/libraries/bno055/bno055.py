import time

class Inclinometer:

    def __init__(self, bus, address):
        
	self.address = address
	self.bus = bus
        
        #configuration
	self.bus.write_byte_data(self.address, 0x3d, 0x00) #configuration mode
        self.bus.write_byte_data(self.address, 0x3f, 0x20) #reset
	self.wait_bus()
        self.bus.write_byte_data(self.address, 0x3e, 0x00) #power mode normal
        self.bus.write_byte_data(self.address, 0x3d, 0x0c) #mode ndof
     
    def get_pitch(self):
        out = self.bus.read_word_data(self.address, 0x1e)
	return self.raw_to_degrees(out)

    def get_roll(self):
	out = self.bus.read_word_data(self.address, 0x1c)
	return self.raw_to_degrees(out)   

    def get_yaw(self):
	out = self.bus.read_word_data(self.address, 0x1a)
        return self.raw_to_degrees(out)

    def raw_to_degrees(self, input):
	if input > 65535/2:
            input -= 65535
        out = float(input)*90/1400
        return out

    def wait_bus(self):
	try:
            self.bus.read_byte_data(self.address, 0x39) #sys_status
            time.sleep(0.2)
	except IOError:
            print 'LOL'
            self.wait_bus()
