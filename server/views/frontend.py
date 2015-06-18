from flask import flash
from flask import redirect
from flask import url_for
from flask import request
from flask import render_template

from server import app
from server import csrf
from server.handlers import login_handler
from server.handlers import stocks_handler

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
    return dict(get_current_user=login_handler.get_current_user, get_stocks_list=stocks_handler.get_stocks_list)

@csrf.error_handler
def csrf_error(reason):
    flash("CSRF error.", "danger")
    return redirect('/')


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
        base.managers.user_manager.add_one(user)

        if user:
            login_handler.login_user(user.get('id'), user.get('username'))
            return redirect('/')
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


@app.route('/', methods=['GET', 'POST'])
def home():
    redirect_uri = '/'
    user = login_handler.get_current_user()

    if user:
        return render_template('profile.html')

    action = request.form.get('action')

    if action == 'log-in':
        return redirect(url_for('login'))
    elif action == 'sign-up':
        return redirect(url_for('signup'))
    else:
        redirect_uri = '/'
        return render_template('home.html')



@app.route('/logout/')
def logout():
    login_handler.user_logout()
    return redirect('/')
