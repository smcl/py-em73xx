#!/usr/bin/python
import serial
import time
 
ctrlZ = chr(26)

smsTimeout = 2
gpsTimeout = 5

class SMS(object):
	def __init__(self, sender, message, date):
		self.sender = sender.strip("\"")
		self.message = message
		self.date = date

def quote(s):
	return "\"" + s + "\""

class Modem(object):
	def __init__(self, dev, bps=460800, pin=None):
		self.device = serial.Serial(dev, bps, timeout=1)
		self.setTextMode()
		if pin:
			self.unlockSIM(pin)

	# -- serial interaction via AT commands etc, maybe should be separate class
	def raw(self, message):
		print message
		self.device.write(message)

	def AT(self, separator, message):
		self.raw("AT%s%s\r\n" % (separator, message))

	def Command(self, command, args=[], sep="+"):
		if not args:
			self.AT(sep, command)
		else:
			self.AT(sep, "%s=%s" % (command, ",".join(args)))

	def Query(self, query, sep="+"):
		self.AT(sep, "%s?" % (query))	
# --------------------------------------------------------------------------

	def setTextMode(self):
		self.Command("CMGF", [ str(1) ])

	def unlockSIM(self, pin):
		self.Query("CPIN")
		responses = self.device.readlines()
		pinNeeded = True
		for r in responses:
			if "READY" in r:
				pinNeeded = False

		if pinNeeded:
			self.Command("CPIN", [ quote(pin) ])

	def sendSMS(self, number, message):
		self.Command("CMGS", [ quote(number) ])
		self.raw(message)
		self.raw(ctrlZ)
		time.sleep(smsTimeout)
		return self.device.readlines()

	def deleteSMS(self, index):
		self.Command("CMGD", [ str(index) ])

	def getGPS(self):
		self.Command("XLCSLSR", [ str(1), str(1), "", "", "", "", "", "", "", "", "", "" ])
		
		attempts = 0

		while attempts < 5:
			time.sleep(gpsTimeout)
			gpsLines = self.device.readlines()
			for line in gpsLines:
				if "XLCSLSR" in line and "XLCSLSR: request" not in line:
					return gpsLines
			attempts += 1

		return []

	def getSMS(self):
		self.Command("CMGL", [ quote("ALL") ])
		return self.device.readlines()

        def listCommands(self):
                self.Command("CLAC")
                return self.device.readlines()

em7345 = Modem("/dev/ttyACM0", pin="1234")

# sending a message:
if False:
	em7345.sendSMS("775356278", "test message from py!")

# getting GPS co-ords:
if False:
	gps = em7345.getGPS()
	if gps:
	    print(gps[1].split(",")[1])
	    print(gps[1].split(",")[2])

# reading messages
raw_messages = [ s.strip() for s in em7345.getSMS() if s.strip() and s.strip() != "OK" ]
messages = []
for i, message in enumerate(raw_messages):
	if not i % 2:
		smsinfo = message.split(",")
		print(smsinfo[0])
		print(smsinfo[1])
		sender = smsinfo[2]
		date = " ".join(smsinfo[4:])
	else:
		messages.append(SMS(sender, message, date))

