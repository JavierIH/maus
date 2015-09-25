import time

class Inclinometer(object):

    def __init__(self, bus, address):
        
	self.address = address
	self.bus = bus
        
        #configuration
	self.bus.write_byte_data(self.address, 0x3d, 0x00) #configuration mode
        self.bus.write_byte_data(self.address, 0x3f, 0x20) #reset
        time.sleep(0.1)
        self.waitBus()
        self.bus.write_byte_data(self.address, 0x3e, 0x00) #power mode normal
	if self.bus.read_byte_data(self.address, 0x3e) != 0:
            print 'ERROR!'
               
        self.bus.write_byte_data(self.address, 0x3d, 0x0c) #mode ndof
     
    def getPitch(self):
        out = self.bus.read_word_data(self.address, 0x1e)
	return self.raw2deg(out)

    def getRoll(self):
	out = self.bus.read_word_data(self.address, 0x1c)
	return self.raw2deg(out)   

    def getYaw(self):
	out = self.bus.read_word_data(self.address, 0x1a)
        return self.raw2deg(out)

    def raw2deg(self, input):
	if input > 65535/2:
            input -= 65535
        out = float(input)*90/1440
        return out

    def waitBus(self):
	try:
            self.bus.read_byte_data(self.address, 0x39) #sys_status
	except IOError:
            print 'waiting...'
            time.sleep(0.5)
            self.waitBus()
