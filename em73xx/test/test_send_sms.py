from em73xx import Modem
from .mock_serial import MockSerial
import unittest2

dev = "/dev/ttyACM0"
bps = 460800
pin = None
debug = False

# message information
recipient = "+420775123456"
content = "test"

# at commands we expect
text_mode_AT = "AT+CMGF=1"
sms_number_AT = "AT+CMGS=\"%s\"" % (recipient)
sms_content_AT = content
end_AT = "\x1a"


class SendSmsTest(unittest2.TestCase):
    def __init__(self, *args, **kwargs):
        serial = MockSerial([])
        self.modem = Modem(dev, bps, pin, serial, debug)
        self.received_sms_messages = self.modem.sendSMS(recipient, content)
        super(SendSmsTest, self).__init__(*args, **kwargs)

    def test_AT_commands(self):
        self.assertEqual(text_mode_AT, self.modem.device.inputs[0].strip())
        self.assertEqual(sms_number_AT, self.modem.device.inputs[1].strip())
        self.assertEqual(sms_content_AT, self.modem.device.inputs[2].strip())
        self.assertEqual(end_AT, self.modem.device.inputs[3].strip())
