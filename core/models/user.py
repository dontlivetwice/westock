import core
from core.models import fields
from core.utils import password_utils
import core.models.base as base

from core.models.user_stock import UserStock
from core.models.user_interest_model import UserInterest
from core.managers.user_stock_manager import UserStockManager
from core.managers.user_interest_manager import UserInterestManager


class User(core.models.base.Model):
    user_stock_manager = UserStockManager()
    user_interest_manager = UserInterestManager()

    DB_MAPPINGS = [
        'id',
        'access_time',
        'username',
        'first_name',
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
    location = fields.StringField(default="")
    website = fields.StringField(default="")
    image_url = fields.StringField(default="")
    gender = fields.StringField(default="unspecified")
    birthday = fields.IntField(default=None)  # Unix timestamp in seconds of user's birthday
    body = fields.DictField()

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.stock_manager = base.managers.stock_manager
        self.interest_manager = base.managers.interest_manager

    def check_password(self, password):
        """Return true if password matches, using password_utils."""
        return password_utils.check_password(password, self.get('password'))

    def get_stocks_for_user(self):
        """Return the list of stocks the user is following"""
        user_id = self.get('id')

        users_stocks = self.user_stock_manager.get_stocks_for_user(user_id)

        stocks = []

        for user_stock in users_stocks:
            stock_id = user_stock.get('stock_id')
            stock = self.stock_manager.get_one(stock_id)

            # remove this hack
            stock.is_owned = True

            if stock:
                stocks.append(stock)

        return stocks

    def is_following_stock(self, stock_id):
        """Return the stock if the user is following"""
        user_id = self.get('id')

        user_stock = self.user_stock_manager.get_stock_for_user(user_id, stock_id)

        return True if user_stock else None

    def get_recommended_stocks_for_user(self, limit=None):
        # 1. get user's interest list
        interests = self.get_interests_for_user()

        # 2. for each interest, get the list of stocks (limit 20 for now)
        stocks = []
        for interest in interests:
            stocks += self.stock_manager.get_stocks_for_interest(interest.get('id'), limit)

        return stocks

    def get_interests_for_user(self):
        user_id = self.get('id')

        users_interests = self.user_interest_manager.get_interests_for_user(user_id)

        interests = []

        for user_interest in users_interests:
            interest_id = user_interest.get('interest_id')
            interest = self.interest_manager.get_one(id=interest_id)

            if interest:
                interests.append(interest)

        return interests

    def add_stock_to_user(self, stock_id):
        user_id = self.get('id')

        user_stock = UserStock(user_id=user_id, stock_id=stock_id)

        return self.user_stock_manager.add_one(user_stock)

    def delete_stock_from_user(self, stock_id):
        user_id = self.get('id')

        user_stock = UserStock(user_id=user_id, stock_id=stock_id)

        return self.user_stock_manager.delete_one(user_stock)

    def add_interest_to_user(self, interest_id):
        user_id = self.get('id')

        user_interest = UserInterest(user_id=user_id, interest_id=interest_id)

        return self.user_interest_manager.add_one(user_interest)

    def get_interest_flow_state(self):
        return self.body.get('interests_flow_done') if self.body else False

    def set_interest_flow_state(self, interest_flow_state):
        if not self.body:
            self.body = {}

        self.body.update({'interests_flow_done': interest_flow_state})
        base.managers.user_manager.update_one(self)

    @classmethod
    def unmutable_fields(cls):
        return ['id', 'password']
