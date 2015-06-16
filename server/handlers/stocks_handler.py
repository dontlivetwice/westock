import functools
import time

from flask import render_template
from flask import request
from flask import session

from settings import prod

import core.models.base as base

def get_stocks_list():
    # TODO: Keep track of sessions
    if 'expires' in session:
        if session['expires'] < time.time():
            user_logout()
        user_id = session.get('user_id')

        if user_id:
            user = base.managers.user_manager.get_one(user_id=user_id)

            if user:
                return user.stock_manager.get_many(user_id)

    return None
