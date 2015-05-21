#!/usr/bin/env python
import ssl
import sys
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.wsgi import WSGIContainer

from server import app

port = 443
if len(sys.argv) > 1:
    port = int(sys.argv[1])

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app), ssl_options={
        "certfile": 'config/ssl/stockinterest.io.crt',
        "keyfile": 'config/ssl/stockinterest.io.key',
        "ssl_version": ssl.PROTOCOL_TLSv1
    })
    http_server.listen(port)
    IOLoop.instance().start()