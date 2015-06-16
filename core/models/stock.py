from core.models.base import Model
from core.models import fields
from collections import defaultdict

class Stock(Model):

	DB_MAPPINGS = [
		'id',
		'ticker',
		'access_time',
		'name',
		'link',
		'time',
		'call_link',
		'body'
	]

	name = fields.StringField()
	ticker = fields.StringField()
	link = fields.StringField()
	time = fields.StringField()
	call_link = fields.StringField()
	body = fields.StringField()

	def __init__(self, *args, **kwargs):
		super(Stock, self).__init__(*args, **kwargs)
