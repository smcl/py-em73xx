class GPS(object):
    def __init__(self, gps_raw):
        gps_parsed = gps_raw.split(",")
        # from pprint import pprint
        # pprint(gps_parsed)
        self.latitude = gps_parsed[1].strip()
        self.longitude = gps_parsed[2].strip()
