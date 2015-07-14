import core
from core.models import fields
import core.models.base as base


class Interest(core.models.base.Model):

    DB_MAPPINGS = [
        'id',
        'access_time',
        'name',
        'image_url',
        'body',
        'followers'
    ]

    id = fields.IDField()
    name = fields.StringField()
    image_url = fields.StringField()
    body = fields.DictField()
    followers = fields.IDField()

    def __init__(self, *args, **kwargs):
        super(Interest, self).__init__(*args, **kwargs)

    def increase_followers(self):
        self.followers += 1

    def decrease_followers(self):
        if self.followers > 0:
            self.followers -= 1
