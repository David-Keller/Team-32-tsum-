#! python3
# https://github.com/fireflyes/Team-32-tsum-

import serial.tools.list_ports
import serial


def listCOMPorts():
	return serial.tools.list_ports.comports()
	
class TeensySerial:
	def delay(self):
		# time.sleep(0.2) # a sleep to play around with if needed
		pass
		
	def __init__(self):
		self.serial = 0
		self.baud = 9600
		self.DEBUG = False
		
	def port(self, COMport):
	"""COMport is given as 'COM1', 'COM2', or 'COM3'"""
		self.serial = serial.Serial(str(COMport), self.baud)
		self.delay()
		
	def setScreenSize(self, x, y):
		self.serial.write('a' + str(x) + ' ' + str(y) + 'z')
		if self.DEBUG:
			print('send set screen size: a', x, y, 'z')
		self.delay()
			
	def mouseButton(self, flag):
		self.serial.write('c' + str(flag) + 'z')
		if self.DEBUG:
			if (flag):
				print('send mouse down: c', flag, 'z')
			else:
				print('send mouse up: c', flag, 'z')
		self.delay()
		
	def moveTo(self, x, y):
		self.serial.write('b' + str(x) + ' ' + str(y) + 'z')
		if self.DEBUG:
			print('send mouse: b', x, y, 'z')
		self.delay()
	
	def swipe(self, xyList):
		for x,y in xyList:
			self.moveTo(x, y)
			
	def close(self):
		self.serial.close()
		