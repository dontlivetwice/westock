import random
import core.models.base as base
from server.views import exceptions


def get_stocks_for_user(user_id, recommended=True):
    # TODO (amine) change user_id to context and then get user id from context
    if not user_id:
        raise exceptions.AuthenticationFailed()

    user = base.managers.user_manager.get_one(id=user_id)

    result_stocks = []

    if user:
        # 1. get the list of stocks the user owns
        own_stocks = user.get_stocks_for_user()

        if not recommended:
            return own_stocks

        # 2. get a recommended list of stocks based on interest (just concatenate for now)
        random_stocks = user.get_recommended_stocks_for_user(limit=25)

        # 3. construct a list of stocks
        result_stocks_dict = {}

        for own_stock in own_stocks:
            result_stocks_dict.update({own_stock.get('ticker'): own_stock})

        for random_stock in random_stocks:
            ticker = random_stock.get('ticker')

            if not result_stocks_dict.get(ticker):
                result_stocks_dict.update({random_stock.get('ticker'): random_stock})

        result_stocks = result_stocks_dict.values()

        random.shuffle(result_stocks)

    return result_stocks


def add_stock_for_user(user_id, stock):
    # 1. get the user
    user = base.managers.user_manager.get_one(id=user_id)

    if not user:
        raise exceptions.AuthenticationFailed()

    # 2. add stock to user
    stock = base.managers.stock_manager.get_one(ticker=stock)

    try:
        # add the stock to the user
        ret = user.add_stock_to_user(stock.get('id'))

        # increase followers count
        if not ret:
            raise exceptions.FollowStockFailed()

        stock.increase_followers()

        ret = base.managers.stock_manager.update_one(stock)

        if not ret:
            raise exceptions.FollowStockFailed()

        return ret

    except:
        raise exceptions.FollowStockFailed()


def delete_stock_for_user(user_id, stock):
    # 1. get the user
    user = base.managers.user_manager.get_one(id=user_id)

    if not user:
        raise exceptions.AuthenticationFailed()

    # 2. add stock to user
    stock = base.managers.stock_manager.get_one(ticker=stock)

    try:
        ret = user.delete_stock_from_user(stock.get('id'))

        if not ret:
            raise exceptions.FollowStockFailed()

        # decrease followers count
        stock.decrease_followers()

        ret = base.managers.stock_manager.update_one(stock)

        if not ret:
            raise exceptions.FollowStockFailed()

        return ret
    except:
        raise exceptions.UnFollowStockFailed()
