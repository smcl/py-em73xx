#!/usr/bin/python
import serial
import time
 
ctrlZ = chr(26)

smsTimeout = 2
gpsTimeout = 5

class Modem(object):
	def __init__(self, dev, bps=460800, pin=None):
		self.device = serial.Serial(dev, bps, timeout=1)
		self.setTextMode()
		if pin:
			self.unlockSIM(pin)

	def raw(self, message):
		self.device.write(message)

	def AT(self, message):
		self.raw(message + "\r\n")

	def setTextMode(self):
		self.AT("AT+CMGF=1")

	def unlockSIM(self, pin):
		self.AT("AT+CPIN?")
		responses = self.device.readlines()
		pinNeeded = True
		for r in responses:
			if "READY" in r:
				pinNeeded = False

		if pinNeeded:
			self.AT("AT+CPIN=\"%s\"" % (pin))

	def sendSMS(self, number, message):
		self.AT("AT+CMGS=\"%s\"" % (number))
		self.AT(message)
		self.raw(ctrlZ)
		time.sleep(smsTimeout)
		return self.device.readlines()

	def getGPS(self):
		self.AT("AT+XLCSLSR=1,1,,,,,,,,,,")
		
		gpsFix = False
		attempts = 0

		while attempts < 5:
			time.sleep(gpsTimeout)
			gpsLines = self.device.readlines()
			for line in gpsLines:
				if "XLCSLSR" in line and "XLCSLSR: request" not in line:
					return gpsLines
			attempts += 1

		return []

em7345 = Modem("/dev/ttyACM0", pin="1234")
em7345.sendSMS("+420775356278", "test message from py!")
gps = em7345.getGPS()

if gps:
        print(gps[1].split(",")[1])
        print(gps[1].split(",")[2])
