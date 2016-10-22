from .utils import unquote


class SMS(object):
    @classmethod
    def fromJson(cls, sms_json):
        return cls(
            sms_json["sms_id"],
            sms_json["status"],
            sms_json["sender"],
            sms_json["date"],
            sms_json["time"],
            sms_json["message"]
        )

    @classmethod
    def from_AT_response(cls, header, message):
        (sms_id_txt, status, sender, something, date, time) = header.split(",")

        sms_id = int(sms_id_txt.replace("+CMGL: ", ""))
        status = unquote(status)
        sender = unquote(sender)
        date = unquote(date)
        time = unquote(time)
        message = message.strip()

        return cls(sms_id, status, sender, date, time, message)

    def __init__(self, sms_id, status, sender, date, time, message):
        self.sms_id = sms_id
        self.status = status
        self.sender = sender
        self.date = date
        self.time = time
        self.message = message

    def toJson(self):
        return {
            "sms_id": self.sms_id,
            "status": self.status,
            "sender": self.sender,
            "date": self.date,
            "time": self.time,
            "message": self.message,
        }
