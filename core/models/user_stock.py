import core
from core.models import fields
import core.models.base as base


class UserStock(core.models.base.Model):

    DB_MAPPINGS = [
        'user_id',
        'stock_id'
    ]

    user_id = fields.IDField()
    stock_id = fields.IDField()

    def __init__(self, *args, **kwargs):
        super(UserStock, self).__init__(*args, **kwargs)
