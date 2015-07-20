import collections
from utils.time import Time
from core.models.base import Model
from core.models import fields


class Stock(Model):

    DB_MAPPINGS = [
        'id',
        'access_time',
        'ticker',
        'name',
        'about',
        'time',
        'followers',
        'body',
        'interest_id'
    ]

    id = fields.IDField()
    name = fields.StringField()
    ticker = fields.StringField()
    about = fields.StringField(default="")
    time = fields.StringField()
    followers = fields.IDField()
    body = fields.DictField()
    interest_id = fields.IDField()

    def __init__(self, *args, **kwargs):
        super(Stock, self).__init__(*args, **kwargs)
        if Time.is_market_open():
            self.day = Time.get_utc_day()
        else:
            self.day = Time.get_business_day()

    def get_followers(self):
        return self.followers

    def increase_followers(self):
        self.followers += 1

    def decrease_followers(self):
        if self.followers > 0:
            self.followers -= 1

    def get_open(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('open')

        if self.body.get(self.day):
            return self.body.get(self.day).get('open')
        return None

    def get_days_high(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('days_high')
        if self.body.get(self.day):
            return self.body.get(self.day).get('days_high')
        return None

    def get_days_low(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('days_low')

        if self.body.get(self.day):
            return self.body.get(self.day).get('days_low')
        return None

    def get_year_high(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('year_high')

        if self.body.get(self.day):
            return self.body.get(self.day).get('year_high')
        return None

    def get_year_low(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('year_low')

        if self.body.get(self.day):
            return self.body.get(self.day).get('year_low')
        return None

    def get_volume(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('volume')

        if self.body.get(self.day):
            return self.body.get(self.day).get('volume')
        return None

    def get_market_cap(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('market_cap')

        if self.body.get(self.day):
            return self.body.get(self.day).get('market_cap')
        return None

    def get_pe_ratio(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('pe_ratio')

        if self.body.get(self.day):
            return self.body.get(self.day).get('pe_ratio')
        return None

    def get_div_yield(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('div_yield')

        if self.body.get(self.day):
            return self.body.get(self.day).get('div_yield')
        return None

    def get_change(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('change')

        if self.body.get(self.day):
            return self.body.get(self.day).get('change')
        return None

    def get_change_percent(self, date=None):
        if not self.body:
            return None

        if date:
            return self.body.get(date).get('change_percent')

        if self.body.get(self.day):
            return self.body.get(self.day).get('change_percent')
        return None

    def get_price(self, date=None):
        if not self.body:
            return None

        if date:
            price_dict = self.body.get(date).get('price')
        else:
            if self.body.get(self.day):
                price_dict = self.body.get(self.day).get('price')
            else:
                price_dict = None

        labels = []
        values = []

        if not price_dict:
            return labels, values

        keys = price_dict.keys()

        # sort labels by ascending time
        keys.sort()

        # now sort the values list
        prices = []

        for key in keys:
            current_column = []
            # convert times to local time
            offset = Time.get_utc_offset()
            local_time = float(key.replace(':', '.')) + offset

            current_column.append(str(local_time))
            if not price_dict.get(key):
                current_column.append(0)
            else:
                current_column.append(float(price_dict.get(key)))
            prices.append(current_column)

        return prices

    def to_json_dict(self):
        model_dict = collections.OrderedDict()

        model_dict.update({'ticker': self.get('ticker')})
        model_dict.update({'name': self.get('name')})
        model_dict.update({'time': self.get('time')})
        model_dict.update({'about': self.get('about')})
        model_dict.update({'open': self.get_open()})
        model_dict.update({'days_high': self.get_days_high()})
        model_dict.update({'days_low': self.get_days_low()})
        model_dict.update({'year_high': self.get_year_high()})
        model_dict.update({'year_low': self.get_year_low()})
        model_dict.update({'volume': self.get_volume()})
        model_dict.update({'market_cap': self.get_market_cap()})
        model_dict.update({'pe_ratio': self.get_pe_ratio()})
        model_dict.update({'div_yield': self.get_div_yield()})
        model_dict.update({'change': self.get_change()})
        model_dict.update({'change_percent': self.get_change_percent()})
        model_dict.update({'followers': self.get_followers()})
        model_dict.update({'prices': self.get_price()})

        return model_dict