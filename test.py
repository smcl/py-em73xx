#!/usr/bin/python

import time
from em73xx import Modem


em7345 = Modem("/dev/ttyACM0", pin="1234", debug=True)

# sending a message:
if False:
	em7345.sendSMS("775356278", "test message from em73xx!")

# getting GPS co-ords:
if False:
    gps = em7345.getGPS()
    if gps:
        print(gps.latitude)
        print(gps.longitude)


# reading messages
messages = em7345.getSMS()
