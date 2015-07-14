import core
from core.models import fields
import core.models.base as base


class UserInterest(core.models.base.Model):

    DB_MAPPINGS = [
        'user_id',
        'interest_id'
    ]

    user_id = fields.IDField()
    interest_id = fields.IDField()

    def __init__(self, *args, **kwargs):
        super(UserInterest, self).__init__(*args, **kwargs)
