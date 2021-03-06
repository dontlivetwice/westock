import functools
import time

from flask import render_template
from flask import request
from flask import session

from settings import prod


def login_user(user_id, name):
    session['user_id'] = user_id
    session['name'] = name
    session['expires'] = int(time.time()) + prod.SESSION_EXPIRE_TIME


def user_logout():
    for key in ('user_id', 'expires', 'name'):
        try:
            del session[key]
        except KeyError:
            continue


def require_login(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if get_current_user() is not None:
            return f(*args, **kwargs)
        return render_template('login.html', redirect_uri='%s?%s' % (
            request.path, request.query_string))
    return wrapped


def get_current_user_id():
    # TODO: Keep track of sessions
    if 'expires' in session:
        if session['expires'] < time.time():
            user_logout()
        return session.get('user_id')
    return None


def get_current_user():
    # TODO: Keep track of sessions
    if 'expires' in session:
        if session['expires'] < time.time():
            user_logout()
        return session.get('name')
    return None


def is_interests_set():
    # TODO: Keep track of sessions
    if 'expires' in session:
        if session['expires'] < time.time():
            user_logout()
        return session.get('interest_set')
    return None


def set_interests_flag(is_set):
    if 'expires' in session:
        if session['expires'] < time.time():
            user_logout()
    session['interest_set'] = is_set
