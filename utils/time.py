from datetime import datetime


class Time(object):
    def __init(self):
        pass

    @classmethod
    def get_time(cls):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')