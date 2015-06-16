import json
from utils.time import Time
from yahoo_finance import Share
from collections import defaultdict

from core.models.stock import Stock
from core.managers.db_manager import DBManager


class StockManagerException(object):
	pass


class StockManager(object):
	def __init__(self):
		self.db_manager = DBManager('stocks')

	@classmethod
	def _serialize_stock(cls, user_id, stock):
		if stock:
			return (user_id, stock.get('ticker'), Time.get_time(), stock.get('name'), stock.get('link'),
			stock.get('time'), stock.get('call_link'), stock.get('body'))

		return ()

	@classmethod
	def _deserialize_stock(cls, stock):
		if stock:
			args = {}

			count = 0

			for var in stock:
				args.update({Stock.DB_MAPPINGS[count]: var})
				count = count + 1

			return Stock(**args)

		return None

	def add_one(self, user_id, ticker):
		# 1. validate stock tiker with yahoo finance API
		share = Share(ticker.upper())

		name = share.data_set.get('Name')
		symbol = share.data_set.get('Symbol')
		currency = share.data_set.get('Currency')

		if not name and not currency:
			StockManagerException('StockNotFoundError:')

		stock = Stock(ticker=symbol, name=name)

		query = ''' (user_id, ticker, access_time, name, link, time, call_link, body) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

		return self.db_manager.add_one(query, StockManager._serialize_stock(user_id, stock))

	def update_one(self, user_id, ticker):
		share = Share(ticker.upper())

		symbol = share.get_info().get('symbol')
		name = share.get_info().get('CompanyName')
		stock = Stock(ticker=symbol)

		self.db_manager.update_one(123, stock.serialize_stock())

	def get_one(self, user_id, ticker):
		pass

	def get_many(self, user_id):
		query = "user_id = \"%s\"" % user_id

		stocks = self.db_manager.get_many(query)

		deserialized_stocks = []

		if stocks:
			for stock in stocks:
				deserialized_stocks.append(StockManager._deserialize_stock(stock))

		return deserialized_stocks
