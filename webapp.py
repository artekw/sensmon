#!/usr/bin/python2
# -*- coding: utf-8 -*-

'''
TODO:
- rozdziałka strony - na 1600 nie wyglada dobrze
- RDW na telefony, tablety
'''
import signal
import time
import os
import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import tornado.gen
import logging
import tornadoredis # https://github.com/leporo/tornado-redis
import simplejson as json

import sensnode.common


HERE = os.path.abspath(os.path.dirname(__file__))

def on_get(result):
    log.debug("get result: %s" % result)

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.tpl")

class DashHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'vals')
        self.render("dash.tpl", init=[json.loads(x) for x in res])

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload.tpl")

class ControlHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("control.tpl")

class LogsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("logs.tpl")

class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("info.tpl", arch=sensnode.common.this_mach(), system=sensnode.common.this_system(), lavg=sensnode.common.loadavg())

class Websocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(Websocket, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'nodes')
        self.client.listen(self.on_message)

    def allow_draft76(self):
        # for WebOS
        return True

    def open(self):
        print "WebSocket opened"

    def on_message(self, result):
        self.write_message(str(result.body))

    def on_close(self):
        print "WebSocket closed"
        self.client.unsubscribe('nodes')
        self.client.disconnect()

application = tornado.web.Application([
    (r"/", HomeHandler),
    (r"/dash", DashHandler),
    (r"/upload", UploadHandler),
    (r"/control", ControlHandler),
    (r"/logs", LogsHandler),
    (r"/info", InfoHandler),
    (r"/websocket", Websocket),
    (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")})],
    template_path = os.path.join(os.path.dirname(__file__), "views"),
    static_path = os.path.join(os.path.dirname(__file__), "static"),
    debug=True)

if __name__ == "__main__":
    print('Start sensmon webapp')
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()