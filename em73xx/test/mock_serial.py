class MockSerial(object):
    def __init__(self, response):
        self.response = response
        self.inputs = []

    def write(self, message):
        self.inputs.append(message)

    def readlines(self):
        return self.response
