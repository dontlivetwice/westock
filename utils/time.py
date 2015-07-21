from datetime import datetime


class Time(object):
    def __init(self):
        pass

    @classmethod
    def get_utc_time(cls):
        return datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_local_time(cls):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    @classmethod
    def get_utc_hours_minutes(cls):
        return datetime.utcnow().strftime('%H:%M')

    @classmethod
    def get_local_hours_minutes(cls):
        return datetime.now().strftime('%H:%M')

    @classmethod
    def get_utc_day(cls):
        return datetime.utcnow().strftime('%Y%m%d')

    @classmethod
    def get_local_day(cls):
        return datetime.utcnow().strftime('%Y%m%d')

    @classmethod
    def get_business_day(cls):
        import datetime
        day_of_week = datetime.datetime.utcnow().strftime('%w')

        hours = cls.get_utc_hours_minutes()
        hours = hours.replace(':', '.')
        delta = 0

        if float(hours) >= 0 and float(hours) <= 13.30:
            delta = 1

        if day_of_week == 0:
            # this is a Sunday, remove 2 days
            time_delta = datetime.timedelta(days=2+delta)
        elif day_of_week == 5:
            # this is a Saturday, remove 1 days
            time_delta = datetime.timedelta(days=1+delta)
        else:
            time_delta = datetime.timedelta(days=delta)

        day = datetime.datetime.utcnow() - time_delta

        return day.strftime('%Y%m%d')

    @classmethod
    def is_market_open(cls):
        import datetime
        day_of_week = datetime.datetime.utcnow().strftime('%w')
        hours = cls.get_utc_hours_minutes()
        hours = hours.replace(':', '.')

        if day_of_week in [0, 5]:
            return False

        if float(hours) >= 13.30 and float(hours) <= 20:
            return True
        return False

    @classmethod
    def get_utc_offset(cls):
        l = Time.get_local_hours_minutes()
        u = Time.get_utc_hours_minutes()
        offset = float(l.replace(':', '.')) - float(u.replace(':', '.'))

        if offset >= 12:
            return offset - 24
        return offset

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
            now = datetime.datetime.utcnow()
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
