#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
TODO:
- RDW na telefony, tablety
- konfiguracja
- baza danych historii
- wykresy
- autoryzacja
- ssl
"""

import signal
import time
import os
import logging
import tornadoredis # https://github.com/leporo/tornado-redis
import simplejson as json
import multiprocessing # http://pymotw.com/2/multiprocessing

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import tornado.gen
import tornado.httpserver
from tornado.escape import json_encode
from tornado.options import define, options

# sensnode
import sensnode.store
import sensnode.decoder
import sensnode.connect
import sensnode.common

c = tornadoredis.Client()
c.connect()

define("port", default=8081, help="Run on the given port", type=int)

clients = []

#--------------------------webapp----------------------------#

class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("home.tpl")

class DashHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'initv')
        self.render("dash.tpl",
            init=[json.loads(x) for x in res]) # sort_keys=True ?

class UploadHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("upload.tpl")

class ControlHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'status')
        self.render("control.tpl",
            init=[json.loads(x) for x in res]) # sort_keys=True ?

class LogsHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("logs.tpl")

class InfoHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("info.tpl",
            arch = sensnode.common.this_mach(),
            system = sensnode.common.this_system(),
            lavg = sensnode.common.loadavg(),
            uptime = sensnode.common.uptime())

class RESTHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, query):
        cl = tornadoredis.Client()
        """Pobieram wszystkie nazwy punktów"""
        nodes = yield tornado.gen.Task(cl.hkeys, 'initv')
        if query not in nodes:
            """Brak punktu - poinformuj"""
            self.write("Brak danych, wybierz inny punkt. Dostępne: %s" % (nodes))
        """Jak istnieje - pobierz"""
        nodevals = yield tornado.gen.Task(cl.hget, 'initv', query)
        self.set_header("Content-Type", "application/json")
        self.write(json_encode(nodevals))
        self.finish()

class Websocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        super(Websocket, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.gen.engine
    def listen(self):
        self.client = tornadoredis.Client()
        self.client.connect()
        yield tornado.gen.Task(self.client.subscribe, 'nodes')
        self.client.listen(self.sendmsg)

    def allow_draft76(self):
        # dla WebOS & iOS
        return True

    def open(self):
        print "WebSocket opened"

    """Wyślij wiadomość do klienta"""
    def sendmsg(self, msg):
        if hasattr(msg, "body"):
            self.write_message(str(msg.body))

    """Odbierz wiadomość od klienta"""
    def on_message(self, msg):
        store = sensnode.store.Store()
        '''FIXME: odczyt aktualnego stanu'''
        store.setStatus(msg) # zapisz status w bazie redis
        # wrzuć w kolejkę
        q = self.application.settings.get('queue')
        q.put(msg)
        self.write_message('{"control":"You send: %s"}' % (json.loads(str(msg))))

    def on_close(self):
        if self.client.subscribed:
            print "WebSocket closed"
            self.client.unsubscribe('nodes')
            self.client.disconnect()

def main():
    # tryb developerski - wyświetlanie dodatkowch komunikatów dla biblioteki sensnode
    debug = False

    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    sp = sensnode.connect.Connect(taskQ, resultQ, debug=debug)
    sp.daemon = True
    sp.start()

    store = sensnode.store.Store(debug=debug)
    decoder = sensnode.decoder.Decoder(debug=debug)

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/", HomeHandler),
        (r"/dash", DashHandler),
        (r"/control", ControlHandler),
        (r"/logs", LogsHandler),
        (r"/info", InfoHandler),
        (r"/websocket", Websocket),
        (r"/rest/([a-z]+)", RESTHandler),
        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")})],
        queue=taskQ,
        template_path = os.path.join(os.path.dirname(__file__), "views"),
        static_path = os.path.join(os.path.dirname(__file__), "static"),
        debug=True)

    httpServer = tornado.httpserver.HTTPServer(application)
    httpServer.listen(options.port)
    print "Nasłuchuje na porcie:", options.port

    def checkResults():
        if not resultQ.empty():
            result = resultQ.get()
            if debug:
                print "Odebrano: %s" % (result)
            decoded = decoder.decode(result)
            store.pubsub(decoded)
            for c in clients:
                c.write_message(result)

    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(checkResults, 500, io_loop = mainLoop)
    scheduler.start()
    mainLoop.start()

if __name__ == "__main__":
    main()