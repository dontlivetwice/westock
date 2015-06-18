import core
from core.models import fields
import core.models.base as base


class Interest(core.models.base.Model):

    DB_MAPPINGS = [
        'id',
        'access_time',
        'name',
        'image_url',
        'body'
    ]

    id = fields.IDField()
    name = fields.StringField()
    image_url = fields.StringField(default="")
    body = fields.StringField(default="{}")

    def __init__(self, *args, **kwargs):
        super(Interest, self).__init__(*args, **kwargs)
