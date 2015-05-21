from core.models.base import Model
from core.models import fields
from collections import defaultdict

class Stock(Model):
	id = fields.IDField()
	name = fields.StringField()
	ticker = fields.StringField()
	link = fields.StringField()
	time = fields.StringField()
	call_link = fields.StringField()

	def __init__(self, *args, **kwargs):
		super(Stock, self).__init__(*args, **kwargs)

	def serialize_stock(self):
		if self.ticker:
			serialized_stock = defaultdict(dict)
			serialized_stock.update({self.ticker: {'link': self.link, 'time': self.time, 'call_link': self.call_link}})
			return serialized_stock
		return None		
