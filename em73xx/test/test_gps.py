from em73xx import Modem
from .mock_serial import MockSerial
import unittest2

dev = "/dev/ttyACM0"
bps = 460800
pin = None
debug = False

expected_latitude = "49.195407 N"
expected_longitude = "16.606729 E"

# flake8: noqa
stub_gps_data = [
    '\r\n',
    '+XLCSLSR: 2, %s, %s, 231.177947, 60.431427, 25.304975,149, 81.534980,67,2016/10/21,21:33:31,0,1,320.07,0.72,-0.66,2.73,0.90,509628,509628.47,,,3.50,2.25,2.50,104.59,65.52,81.53,,,1,1919,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,6,81.04,285.14,32.00,1,,,,13 ,74.04,307.16,0.00,1,,,,10 ,65.03,85.04,32.00,1,,,,28 ,65.03,231.12,26.00,1,,,,8 ,39.02,318.16,24.00,1,,,,1 ,39.02,48.02,26.00,1,,,,9 \r\n' % (expected_latitude, expected_longitude),
    '\r\n',
    'OK\r\n'
]

text_mode_AT = "AT+CMGF=1"
gps_command_AT = "AT+XLCSLSR=1,1,,,,,,,,,,"

class GetGpsTest(unittest2.TestCase):
    def __init__(self, *args, **kwargs):
        serial = MockSerial(stub_gps_data)
        self.modem = Modem(dev, bps, pin, serial, debug)
        self.gps_data = self.modem.getGPS()
        super(GetGpsTest, self).__init__(*args, **kwargs)

    def test_lat_lon(self):
        self.assertEqual(self.gps_data.latitude, expected_latitude)
        self.assertEqual(self.gps_data.longitude, expected_longitude)

    def test_AT_commands(self):
        commands = self.modem.device.inputs
        self.assertEqual(text_mode_AT, commands[0].strip())
        self.assertEqual(gps_command_AT, commands[1].strip())
