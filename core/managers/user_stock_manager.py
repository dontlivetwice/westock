from core.models.user_stock import UserStock
from core.managers.base_manager import Manager, ManagerException


class UserStockManagerException(ManagerException):
    pass


class UserStockManager(Manager):
    def __init__(self):
        super(UserStockManager, self).__init__('users_stocks')

    @classmethod
    def _serialize(cls, user_stock):
        if user_stock:
            return user_stock.get('user_id'), user_stock.get('stock_id')

        return ()

    @classmethod
    def _deserialize(cls, obj):
        """ Deserializes the passed in object based on DB mapping """
        if obj:
            args = {}

            count = 0

            for var in obj:
                args.update({UserStock.DB_MAPPINGS[count]: var})
                count += 1

            return UserStock(**args)

        return None

    def add_one(self, user_stock):
        query = ''' (user_id, stock_id) VALUES (%s, %s)'''

        return self.db_manager.add_one(query, UserStockManager._serialize(user_stock))

    def delete_one(self, user_stock):
        query = "user_id = \"%s\" and stock_id = \"%s\"" % (user_stock.get('user_id'), user_stock.get('stock_id'))

        return self.db_manager.delete_one(query)

    def get_stocks_for_user(self, user_id, limit=100):
        query = "user_id = \"%s\"" % user_id

        users_stocks = self.db_manager.get_many(limit, query)

        result_list = []

        if users_stocks:
            for stock in users_stocks:
                result_list.append(UserStockManager._deserialize(stock))

        return result_list
