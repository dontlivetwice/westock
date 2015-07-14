from datetime import datetime


class Time(object):
    def __init(self):
        pass

    @classmethod
    def get_time(cls):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_hours_minutes(cls):
        return datetime.utcnow().strftime('%H:%M')

    @classmethod
    def get_time_for_yahoo(cls):

        return datetime.utcnow().strftime('%Y%m%d')

    @classmethod
    def get_time_for_delta(cls, unit, time_delta, start_date=None):
        import datetime
        # 1. Get the time_delta as a

        if unit == 'days':
            time_delta = datetime.timedelta(days=time_delta)
        else:
            return None

        # 2. get the current time
        if not start_date:
            now = datetime.datetime.now()
        else:
            now = datetime.datetime.strptime(str(start_date), '%Y%m%d')

        # 3. add the delta and return the time
        future = now + time_delta

        return future

    @classmethod
    def time_to_str_time(cls, time):
        return time.strftime('%Y%m%d')

    @classmethod
    def time_to_str_time_with_dash(cls, time):
        return time.strftime('%Y-%m-%d')