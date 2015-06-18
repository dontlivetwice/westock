from core.models.base import Model
from core.models import fields


class Stock(Model):

    DB_MAPPINGS = [
        'id',
        'access_time',
        'ticker',
        'name',
        'link',
        'time',
        'call_link',
        'body',
        'interest_id'
    ]

    id = fields.IDField()
    name = fields.StringField()
    ticker = fields.StringField()
    link = fields.StringField()
    time = fields.StringField()
    call_link = fields.StringField()
    body = fields.StringField()
    interest_id = fields.IDField()

    def __init__(self, *args, **kwargs):
        super(Stock, self).__init__(*args, **kwargs)
