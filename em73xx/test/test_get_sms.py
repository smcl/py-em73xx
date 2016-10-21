from em73xx import Modem
from .mock_serial import MockSerial
import unittest2

dev = "/dev/ttyACM0"
bps = 460800
pin = None
debug = None

message_senders = [
    "+420775123456",
    "+420775123457",
    "+420775123458"
]

test_responses = []

for i, sender in enumerate(message_senders):
    test_responses.append('+CMGL: 1,"REC READ","%s",,"21/10/16,12:00:00+08"\r\n' % (sender))
    test_responses.append('%s\r\n' % str(i))

serial = MockSerial(test_responses)

class GetSmsTest(unittest2.TestCase):
    def __init__(self, *args, **kwargs):
        modem = Modem(dev, bps, pin, serial, debug)
        self.received_sms_messages = modem.getSMS()
        super(GetSmsTest, self).__init__(*args, **kwargs)

    def test_correct_number_sms(self):
        self.assertEqual(3, len(self.received_sms_messages))

    def test_correct_message(self):
        for i, sms in enumerate(self.received_sms_messages):
            self.assertEqual(sms.message, str(i))

    def test_correct_sender(self):
        for i, sms in enumerate(self.received_sms_messages):
            self.assertEqual(sms.sender, message_senders[i])
