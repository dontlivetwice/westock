from yahoo_finance import Share
from collections import defaultdict

from core.models.stock import Stock
from core.managers.db_manager import DBManager

class StockManager(object):
	def __init__(self):
		self.db_manager = DBManager('stocks')

	def add_one(self, user_id, ticker):
		share = Share(ticker.upper())

		symbol = share.get_info().get('symbol')
		name = share.get_info().get('CompanyName')
		stock = Stock(ticker=symbol)

		self.db_manager.add_one(123, stock.serialize_stock())

	def update_one(self, user_id, ticker):
		share = Share(ticker.upper())

		symbol = share.get_info().get('symbol')
		name = share.get_info().get('CompanyName')
		stock = Stock(ticker=symbol)

		self.db_manager.update_one(123, stock.serialize_stock())

	def get_one(self, user_id, ticker):
		pass