#! python2

##http://playground.arduino.cc/Interfacing/Python
## take away. py3 ser.write(b'5') # prefix b is required for Python 3.x, optional for Python 2.x
import serial.tools.list_ports
import serial
import time
from time import sleep
import threading

class MySerial:
	def delay(self):
		time.sleep(0.2)

	def __init__(self):
		self.serial = 0
		self.baud = 9600
		self.thread = None
		
	def setScreenSize(self, x, y):
		self.serial.write('a' + str(x) + ' ' + str(y) + 'z')
		print 'send set screen size: a', x, y, 'z'
		self.delay()
			
	def mouseButton(self, flag):
		self.serial.write('c' + str(flag) + 'z')
		if (flag):
			print 'send mouse down: c', flag, 'z'
		else:
			print 'send mouse up: c', flag, 'z'
		self.delay()
		
	def moveTo(self, x, y):
		self.serial.write('b' + str(x) + ' ' + str(y) + 'z')
		print 'send mouse: b', x, y, 'z'
		self.delay()
		
	def port(self, port):
		self.serial = serial.Serial(str(port), self.baud)
		self.delay()
		
	def selectPort(self):
		print ("Select Port:\n")
		ports = serial.tools.list_ports.comports()

		i = 0
		for port in ports:
			print '#', i, ports[i]
			i += 1

		selection = int(raw_input("?#"))

		if selection > i-1:
			print "you're dumb."
			exit()

		port = str(ports[selection]).split(" - ")[0]
		self.serial = serial.Serial(port, self.baud)
		self.delay()
		
	def swipe(self, xyList):
		for x,y in xyList:
			self.moveTo(x, y)
	
	def test(self):
		print("provide 'x y' to move the mouse. '1|0|3' to click or unclick or single click. 'q' to quit.")
		while True:
			input = raw_input()
			
			if len(input) == 1:
				if (input == 'q'):
					break
				if not input.isdigit():
					print "you're dumb"
					continue
				self.mouseButton(int(input))
			else:
				if ' ' in input:
					x, y = input.split(' ')
					if not x.isdigit() or not y.isdigit():
						print "you're dumb"
						continue
					self.moveTo(x, y)
				else:
					print "you're dumb"

	def close(self):
		self.stopReading()
		self.serial.close()
		
	def readingWorker(self):
		if self.thread is None:
			return
		while True:
			bytesToRead = self.serial.inWaiting()
			print(self.serial.read(bytesToRead))

	def stopReading(self):
		if self.thread is not None:
			self.thread.stop()
		self.thead = None
				
	def startReading(self):
		if self.thread is None:
			return
		self.thread = threading.Thread(target=readingWorker)
		self.thread.start()
		
ms = MySerial()
ms.selectPort()

#ms.startReading() # I don't think this works

sleep(1)

# ms.swipe([(500,1400), (500,1000), (500,600), (500,200)])

# exit()

# ms.setScreenSize(1438, 2557)
ms.test()

ms.moveTo(720, 1900)
ms.mouseButton(1)
ms.swipe([(720, 1300), (350, 1300), (350, 1000)])
ms.mouseButton(0)
sleep(4)
ms.moveTo(350, 1000)
ms.mouseButton(1)
ms.moveTo(720, 1900)
ms.mouseButton(0)

if False:
	ms.moveTo(360, 2000)
	ms.mouseButton(1)
	ms.moveTo(360, 1700)
	ms.moveTo(360, 1400)
	ms.moveTo(360, 1100)
	ms.moveTo(360, 800)
	ms.moveTo(360, 500)
	ms.moveTo(360, 200)
	ms.mouseButton(0)

	sleep(3)

	ms.moveTo(360, 2060)
	ms.mouseButton(1)
	ms.moveTo(1090, 2060)
	ms.moveTo(1090, 1700)
	ms.moveTo(1090, 1700)
	ms.moveTo(700, 1300)
	ms.mouseButton(0)


ms.close()