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
    def _serialize(cls, stock, serialize_id=False):
        if stock:
            about = stock.get('about')
            if about:
                about = about.encode('ascii', errors='ignore')

            name = stock.get('name')
            if name:
                name = name.encode('ascii', errors='ignore')

            if serialize_id:
                return (stock.get('id'), Time.get_utc_time(), stock.get('ticker'), name, about, stock.get('time'),
                        stock.get('followers'), json.dumps(stock.get('body')), stock.get('interest_id', 1))

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

        serialized_stock = StockManager._serialize(stock)

        ret = self.db_manager.add_one(query, serialized_stock)

        if ret:
            mc_key = self._derive_key('stocks', stock.get('id'))
            self.db_manager.mc.set(mc_key, serialized_stock, self.db_manager.expiration)

        return ret

    def get_one(self, stock_id):
        # 1. try to ge the stock from the cache
        mc_key = self._derive_key('stocks', stock_id)

        stock = self.db_manager.mc.get(mc_key)

        if not stock:
            # 2. if not in the cache get it from the DB
            stock = super(StockManager, self).get_one(id=stock_id)

            # 3. update the cache
            self.db_manager.mc.set(mc_key, StockManager._serialize(stock, True), self.db_manager.expiration)
        else:
            stock = StockManager._deserialize(stock)

        return stock

    def get_stocks_for_interest(self, interest_id, limit=None):
        query = "interest_id = \"%s\"" % interest_id

        # 1. get the list of stock ids for the interest from cache
        mc_key = self._derive_key('interests', interest_id)
        stock_ids = self.db_manager.mc.get(mc_key)

        result_list = []

        if not stock_ids:
            stocks = self.db_manager.get_many(limit, query)

            if stocks:
                stock_ids = []

                for stock in stocks:
                    des_stock = StockManager._deserialize(stock)
                    result_list.append(des_stock)

                    stock_id = des_stock.get('id')
                    stock_ids.append(stock_id)

                    curr_key = self._derive_key('stocks', stock_id)

                    if not self.db_manager.mc.get(curr_key):
                        self.db_manager.mc.set(curr_key, stock, self.db_manager.expiration)

                # now add this list of stock ids to the interest id in memory
                self.db_manager.mc.set(mc_key, stock_ids, self.db_manager.expiration)
        else:
            print "-->Getting stocks for interests from cache, key: %s" % mc_key
            for stock_id in stock_ids:
                stock = self.get_one(stock_id)
                result_list.append(stock)

        return result_list