from .utils import unquote


class SMS(object):
    def __init__(self, header, message):
        self.parse_header(header)
        self.message = message.strip()

    def parse_header(self, header):
        (sms_id, status, sender, something, date, time) = header.split(",")

        self.sms_id = sms_id
        self.status = unquote(status)
        self.sender = unquote(sender)
        self.date = unquote(date)
        self.time = unquote(time)
