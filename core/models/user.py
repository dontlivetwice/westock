from core.models.base import Model
from core.models import fields

from core.managers.stock_manager import StockManager
from core.managers.db_manager import DBManager


class User(Model):
	stock_manager = StockManager()

	DB_MAPPINGS = [
		'id',
		'access_time',
		'username',
		'name',
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
	location = fields.StringField(default='')
	website = fields.StringField(default="")
	image_url = fields.StringField(default="")
	gender = fields.StringField(default="unspecified")
	birthday = fields.IntField(default=None)  # Unix timestamp in seconds of user's birthday
	stock_list = fields.ListField(default=list)

	def __init__(self, *args, **kwargs):
		super(User, self).__init__(*args, **kwargs)
