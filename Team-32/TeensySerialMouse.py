#! python3
# https://github.com/fireflyes/Team-32-tsum-

import serial.tools.list_ports
import serial


def listCOMPorts():
	return [str(ports) for ports in serial.tools.list_ports.comports()]
	
class TeensySerialMouse:
	def delay(self):
		# time.sleep(0.2) # a sleep to play around with if needed
		pass
		
	def __init__(self):
		self.serial = 0
		self.baud = 9600
		self.DEBUG = False
		
	def setDEBUG(self, tf):
		"""tf must be True or False"""
		self.DEBUG = tf
		
	def port(self, COMport):
		"""COMport is given as 'COM1', 'COM2', or 'COM3'"""
		self.serial = serial.Serial(str(COMport), self.baud)
		self.delay()
		
	def setScreenSize(self, x, y):
		data = 'a' + str(x) + ' ' + str(y) + 'z'
		self.serial.write(data.encode('utf-8'))
		if self.DEBUG:
			print('send set screen size: a', x, y, 'z')
		self.delay()
			
	def mouseButton(self, flag):
		data = 'c' + str(flag) + 'z'
		self.serial.write(data.encode('utf-8'))
		if self.DEBUG:
			if (flag):
				print('send mouse down: c', flag, 'z')
			else:
				print('send mouse up: c', flag, 'z')
		self.delay()
		
	def moveTo(self, x, y):
		data = 'b' + str(x) + ' ' + str(y) + 'z'
		self.serial.write(data.encode('utf-8'))
		if self.DEBUG:
			print('send mouse: b', x, y, 'z')
		self.delay()
	
	def swipe(self, xyList):
		xy = xyList[0]
		self.moveTo(xy[0], xy[1])
		self.mouseButton(1)
		for x,y in xyList:
			self.moveTo(x, y)
		self.moveButton(0)
			
	def close(self):
		self.serial.close()
		
