import serial
import time
from .sms import SMS
from .gps import GPS
from .utils import (
    pairwise,
    quote
)


smsTimeout = 2
gpsTimeout = 5
ctrlZ = chr(26)


class Modem(object):
    def __init__(self, dev, bps=460800, pin=None, device=None, debug=False):
        self.debug = debug

        if device:
            self.device = device
        else:
            self.device = serial.Serial(dev, bps, timeout=1)

        self.setTextMode()
        if pin:
            self.unlockSIM(pin)

    # -- serial interaction via AT commands etc, maybe should be separate class
    def raw(self, message):
        self.log(message)
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
        self.Command("CMGF", [str(1)])

    def unlockSIM(self, pin):
        self.Query("CPIN")
        responses = self.device.readlines()
        pinNeeded = True
        for r in responses:
            if "READY" in r:
                pinNeeded = False

        if pinNeeded:
            self.Command("CPIN", [quote(pin)])

    def sendSMS(self, number, message):
        self.Command("CMGS", [quote(number)])
        self.raw(message)
        self.raw(ctrlZ)
        time.sleep(smsTimeout)
        return self.device.readlines()

    def deleteSMS(self, index):
        self.Command("CMGD", [str(index)])

    def getGPS(self):
        self.Command("XLCSLSR",
                     [str(1), str(1), "", "", "", "", "", "", "", "", "", ""])

        attempts = 0

        while attempts < 10:
            time.sleep(gpsTimeout)
            raw_input = self.device.readlines()
            raw_gps = [l for l in raw_input if l.strip() and l.strip() != "OK"]
            for line in raw_gps:
                if "XLCSLSR" in line and "XLCSLSR: request" not in line:
                    return GPS(line)
            attempts += 1

        return None

    def getSMS(self):
        self.Command("CMGL", [quote("ALL")])
        raw_input = self.device.readlines()
        raw_sms = [l for l in raw_input if l.strip() and l.strip() != "OK"]

        messages = []

        for header, content in pairwise(raw_sms):
            message = SMS(header, content)
            messages.append(message)

        return messages

    def listCommands(self):
            self.Command("CLAC")
            return self.device.readlines()

    def log(self, message):
        if self.debug:
            print(message)
