import random
import core.models.base as base
from server.views import exceptions


def get_stocks_for_user(user_id):
    # TODO (amine) change user_id to context and then get user id from context
    if not user_id:
        raise exceptions.AuthenticationFailed()

    user = base.managers.user_manager.get_one(id=user_id)

    if not user:
        raise exceptions.AuthenticationFailed()

    stocks = user.get_stocks_for_user()

    result_stocks = []

    for stock in stocks:
        result_stocks.append(stock.to_json_dict())

    return result_stocks


def get_recommended_stocks_for_user(user_id):
    if not user_id:
        raise exceptions.AuthenticationFailed()

    user = base.managers.user_manager.get_one(id=user_id)

    random_stocks = user.get_recommended_stocks_for_user(limit=20)

    result_stocks = []

    for random_stock in random_stocks:
        if user.is_following_stock(random_stock.get('id')):
            continue

        result_stocks.append(random_stock.to_json_dict())

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
