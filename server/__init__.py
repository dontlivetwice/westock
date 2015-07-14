import logging

from flask import Flask
from flask_wtf.csrf import CsrfProtect

from settings import prod

log = logging.getLogger(__name__)

app = Flask(__name__)
app.config['DEBUG'] = True
app.debug = True

app.secret_key = prod.SECRET_KEY

app.template_folder = 'templates'
app.static_folder = 'static'

csrf = CsrfProtect(app)


def add_headers(response):
    for header, value in prod.HEADERS.iteritems():
        response.headers.setdefault(header, value)
    if response.mimetype not in ('text/css', 'application/javascript', 'image/png', 'image/jpg'):
        for header, value in prod.CACHE_HEADERS.iteritems():
            response.headers.setdefault(header, value)
    if not prod.DEBUG:
        for header, value in prod.SSL_HEADERS.iteritems():
            response.headers.setdefault(header, value)
    return response

app.after_request(add_headers)

# Include the views
import server.views

assert server  # silence pyflakes