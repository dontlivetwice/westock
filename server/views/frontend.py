import time
import urlparse

from flask import flash
from flask import redirect
from flask import request
from flask import render_template
from werkzeug.security import gen_salt

from server import app
from server import csrf
from server.helpers import login

# Get the running version at startup for the /v/ endpoint
try:
    with open('version.txt') as version_file:
        VERSION = version_file.read()
except IOError:
    VERSION = "0"

@app.context_processor
def add_jinja_utils():
    return dict(get_current_user=login.get_current_user)

@csrf.error_handler
def csrf_error(reason):
    flash("CSRF error.", "danger")
    return redirect('/')


@app.route('/v/', methods=['GET'])
def version():
    return VERSION


@app.route('/', methods=('GET', 'POST'))
def home():
    redirect_uri = '/'
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        #user = model.User.manager().get(username, password)
        redirect_uri = request.form.get('redirect_uri', '/')
        if _is_absolute_url(redirect_uri):
            redirect_uri = '/'
            '''
        if user:
            login.login_user(user.username)
            return redirect(redirect_uri)
        flash('Invalid login.', 'danger')
    user = login.get_current_user()
    if user:
        return render_template('home.html')'''
    return render_template('login.html', redirect_uri=redirect_uri)


@app.route('/logout/')
def logout():
    #login.user_logout()
    return redirect('/')
