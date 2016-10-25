from dateutil import parser as iso_parser
from datetime import datetime
from .utils import unquote


def parse_date_time(date, time):
    date_format = "%y/%m/%d %H:%M:%S"
    date_and_time = (date + " " + time)[:-3]
    return datetime.strptime(date_and_time, date_format)


class SMS(object):
    @classmethod
    def fromJson(cls, sms_json):
        return cls(
            sms_json["sms_id"],
            sms_json["status"],
            sms_json["sender"],
            iso_parser.parse(sms_json["date_received"]),
            sms_json["message"],
            sms_json["read"]
        )

    @classmethod
    def from_AT_response(cls, header, message):
        (sms_id_txt, status, sender, something, date, time) = header.split(",")

        sms_id = int(sms_id_txt.replace("+CMGL: ", ""))
        status = unquote(status)
        sender = unquote(sender)
        date = unquote(date.strip())
        time = unquote(time.strip())
        date_received = parse_date_time(date, time)
        message = message.strip()

        return cls(sms_id, status, sender, date_received, message, False)

    def __init__(self, sms_id, status, sender, date_received, message, read):
        self.sms_id = sms_id
        self.status = status
        self.sender = sender
        self.date_received = date_received
        self.message = message
        self.read = read

    def toJson(self):
        return {
            "sms_id": self.sms_id,
            "status": self.status,
            "sender": self.sender,
            "date_received": self.date_received.isoformat(),
            "time": self.time,
            "message": self.message,
            "read": self.read
        }
