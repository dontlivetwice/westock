import json
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
            about = stock.get('about')
            if about:
                about = about.encode('ascii', errors='ignore')

            name = stock.get('name')
            if name:
                name = name.encode('ascii', errors='ignore')

            return (Time.get_utc_time(), stock.get('ticker'), name, about, stock.get('time'),
                    stock.get('followers'), json.dumps(stock.get('body')), stock.get('interest_id', 1))

        return ()

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object based on DB mapping """
        if obj:
            args = {}

            count = 0

            for var in obj:
                if Stock.DB_MAPPINGS[count] in ['about', 'name'] and var is not None:
                    try:
                        var = var.decode('ascii', errors='ignore')
                    except:
                        pass

                args.update({Stock.DB_MAPPINGS[count]: var})
                count += 1

            return Stock(**args)

        return None

    def add_one(self, stock):
        query = ''' (access_time, ticker, name, about, time, followers, body, interest_id)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''

        return self.db_manager.add_one(query, StockManager._serialize(stock))

    def get_stocks_for_interest(self, interest_id, limit=None):
        query = "interest_id = \"%s\"" % interest_id

        stocks = self.db_manager.get_many(limit, query)

        result_list = []

        if stocks:
            for stock in stocks:
                result_list.append(StockManager._deserialize(stock))

        return result_list