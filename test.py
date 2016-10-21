#!/usr/bin/python

import time
from em73xx import Modem


em7345 = Modem("/dev/ttyACM1", pin="1234")

# sending a message:
if False:
	em7345.sendSMS("775356278", "test message from em73xx!")

# getting GPS co-ords:
if False:
	gps = em7345.getGPS()
	if gps:
	    print(gps[1].split(",")[1])
	    print(gps[1].split(",")[2])

# reading messages
messages = em7345.getSMS()
