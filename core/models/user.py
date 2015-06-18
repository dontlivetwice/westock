import core
from core.models import fields
from core.utils import password_utils
import core.models.base as base


class User(core.models.base.Model):

    DB_MAPPINGS = [
        'id',
        'access_time',
        'username',
        'first_name',
        'last_name',
        'email',
        'password',
        'about',
        'location',
        'website',
        'image_url',
        'gender',
        'birthday',
        'body'
    ]

    id = fields.IDField()
    username = fields.StringField()
    email = fields.EmailField()
    first_name = fields.StringField()
    last_name = fields.StringField(default="")
    password = fields.StringField()
    about = fields.StringField(default="")
    location = fields.StringField(default="")
    website = fields.StringField(default="")
    image_url = fields.StringField(default="")
    gender = fields.StringField(default="unspecified")
    birthday = fields.IntField(default=None)  # Unix timestamp in seconds of user's birthday
    body = fields.StringField(default="{}")

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.stock_manager = base.managers.stock_manager

    def check_password(self, password):
        """Return true if password matches, using password_utils."""
        return password_utils.check_password(password, self.password)
