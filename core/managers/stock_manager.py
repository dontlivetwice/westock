from utils.time import Time
from core.models.stock import Stock
from core.managers.base_manager import Manager, ManagerException


class StockManagerException(ManagerException):
    pass


class StockManager(Manager):
    def __init__(self):
        super(StockManager, self).__init__('stocks')

    @classmethod
    def _serialize(cls, stock):
        if stock:
            return (Time.get_time(), stock.get('ticker'), stock.get('name'), stock.get('link'),
                    stock.get('time'), stock.get('call_link'), stock.get('body'), stock.get('interest_id', 1))

        return ()

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object based on DB mapping """
        if obj:
            args = {}

            count = 0

            for var in obj:
                args.update({Stock.DB_MAPPINGS[count]: var})
                count += 1

            return Stock(**args)

        return None

    def add_one(self, stock):
        query = ''' (access_time, ticker, name, link, time, call_link, body, interest_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

        return self.db_manager.add_one(query, StockManager._serialize(stock))

    def get_many(self, limit=None):
        stocks = self.db_manager.get_many(limit)

        deserialized_stocks = []

        if stocks:
            for stock in stocks:
                deserialized_stocks.append(StockManager._deserialize(stock))

        return deserialized_stocks
