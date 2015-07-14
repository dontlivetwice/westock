from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import jsonify

from server import app
from server import csrf

from server.views import exceptions
from server.handlers import login_handler
from server.handlers import stock_handler
from server.handlers import interest_handler

import core.models.base as base
from core.models.user import User

# Get the running version at startup for the /v/ endpoint
try:
    with open('version.txt') as version_file:
        VERSION = version_file.read()
except IOError:
    VERSION = "0"

@app.context_processor
def add_jinja_utils():
    return dict(get_current_user=login_handler.get_current_user,
                get_current_user_id=login_handler.get_current_user_id,
                get_stocks_for_user=stock_handler.get_stocks_for_user,
                get_interest_list=interest_handler.get_interest_list,
                get_interest_flow_state=interest_handler.get_interest_flow_state,
                get_interests_for_user=interest_handler.get_interests_for_user)


@csrf.error_handler
def csrf_error(reason):
    flash("CSRF error.", "danger")
    return redirect('/')


def construct_response(result, **kwargs):
    response_dict = {}

    for key, value in kwargs.items():
        response_dict.update({key: value})

    if isinstance(result, exceptions.ApiError):
        status = result.error_code.http_status
        message = result.error_code.message
    else:
        message = "OK"
        status = result

    response_dict.update({"message": message})

    return jsonify(response_dict), status


@app.route('/v/', methods=['GET'])
def version():
    return VERSION


@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username').encode('utf-8')
        first_name = request.form.get('firstname').encode('utf-8')
        last_name = request.form.get('lastname').encode('utf-8')
        email = request.form.get('email').encode('utf-8')
        password = request.form.get('password').encode('utf-8')

        user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)
        user = base.managers.user_manager.add_one(user)

        # TODO: do this in a better way
        if user:
            login_handler.login_user(user.get('id'), user.get('username'))
            return render_template('profile.html')

        flash('Invalid login.', 'danger')

    return render_template('signup.html')


@app.route('/login/', methods=['GET', 'POST'])
def login():
    redirect_uri = '/'
    if request.method == 'POST':
        username = request.form.get('username').encode('utf-8')
        password = request.form.get('password').encode('utf-8')
        
        user = base.managers.user_manager.login(username, password)

        if user:
            login_handler.login_user(user.get('id'), user.get('username'))
            return redirect(redirect_uri)
        flash('Invalid login.', 'danger')

    return render_template('login.html', redirect_uri=redirect_uri)


@app.route('/interests/', methods=['GET', 'POST'])
def interests():
    redirect_uri = '/'

    if request.method == 'POST':
        # if there is a logged in user, and user did not go through the interest flow, add interests to user
        user_id = login_handler.get_current_user_id()

        if not user_id:
            raise exceptions.AuthenticationFailed()

        interests = []

        for key in request.form.keys():
            value = request.form.get(key)
            if value == 'true':
                interests.append(key)

        interest_handler.add_interests_for_user(user_id, interests)

        return render_template('profile.html'), 200

    return render_template('interests.html', redirect_uri=redirect_uri)


@app.route('/stocks/', methods=['GET', 'POST', 'DELETE'])
def stocks():
    redirect_uri = '/'

    if request.method in ['POST', 'DELETE']:
        # if there is a logged in user, and user did not go through the interest flow, add interests to user
        user_id = login_handler.get_current_user_id()

        if not user_id:
            raise exceptions.AuthenticationFailed()

        ticker = request.form.get('ticker').encode('utf-8')

        if request.method == 'POST':
            try:
                stock_handler.add_stock_for_user(user_id, ticker)
                return construct_response(200, ticker=ticker)
            except exceptions.FollowStockFailed as e:
                return construct_response(e, ticker=ticker)

        elif request.method == 'DELETE':
            try:
                stock_handler.delete_stock_for_user(user_id, ticker)
                return construct_response(200, ticker=ticker)
            except exceptions.UnFollowStockFailed as e:
                return construct_response(e, ticker=ticker)

    return render_template('stocks.html', redirect_uri=redirect_uri)


@app.route('/', methods=['GET', 'POST'])
def home():
    user = login_handler.get_current_user()

    if user:
        return render_template('profile.html')

    action = request.form.get('action')

    if action == 'log-in':
        return redirect(url_for('login'))
    elif action == 'sign-up':
        return redirect(url_for('signup'))
    else:
        return render_template('home.html')


@app.route('/logout/')
@app.route('/logout')
def logout():
    login_handler.user_logout()
    return render_template('home.html'), 200
