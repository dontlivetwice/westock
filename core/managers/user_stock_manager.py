from utils.time import Time
from core.managers.base_manager import Manager, ManagerException


class UserStockManagerException(ManagerException):
    pass


class UserStockManager(Manager):
    def __init__(self):
        super(UserStockManager, self).__init__('users_stocks')

    @classmethod
    def _serialize(cls, interest):
        if interest:
            return (Time.get_time(), interest.get('name'), interest.get('image_url'),
                    interest.get('body'))

        return ()

    def add_one(self, user_stock):
        query = ''' (user_id, stock_id) VALUES (%s, %s)'''

        return self.db_manager.add_one(query, UserStockManager._serialize(user_stock))
