#!/usr/bin/python2
# -*- coding: utf-8 -*-

"""
TODO:
- RDW na telefony, tablety
- konfiguracja
"""

debug = False  # tryb developerski - wyświetlanie dodatkowch komunikatów dla biblioteki sensnode

import os

# https://github.com/leporo/tornado-redis
import tornadoredis

import simplejson as json
# http://pymotw.com/2/multiprocessing
import multiprocessing

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import tornado.gen
import tornado.httpserver
from tornado.options import define, options

# sensnode
import sensnode.store, sensnode.decoder, sensnode.connect, sensnode.common, sensnode.config

# https://code.google.com/p/leveldb-py/
# key-value database from Google :)
import sensnode.leveldb

# ------------------------webapp settings--------------------#

define("webapp_port", default=sensnode.common.settings_cfg['settings'][
       'webapp']['port'], help="Run on the given port", type=int)
define("leveldb_dbname", default=sensnode.common.settings_cfg['settings'][
       'leveldb']['dbname'], help="LevelDB database name")
define("leveldb_path", default=sensnode.common.settings_cfg['settings'][
       'leveldb']['path'], help="LevelDB path do database")

# dane dla tych punktów NIE SĄ umieszczane w bazie histori
filterout = ['powernode']

# ----------------------end webapp settings------------------#

c = tornadoredis.Client()
c.connect()

leveldb = sensnode.leveldb.DB("%s/%s" % (options.leveldb_path, options.leveldb_dbname), create_if_missing=True)

clients = []

# --------------------------webapp code-----------------------#


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        # self.redirect("/")
        self.redirect(self.get_argument("next", "/"))


class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.tpl", resp=None)

    def post(self):
        username = self.get_argument('name', '')
        password = self.get_argument('pass', '')

        settings_pass = settings_cfg['settings']['webapp']['password']

        # logowanie - FIXME
        if not password:
            login_response = {
                'msg': 'Wpisz haslo.'
            }
            self.render("login.tpl", resp=login_response)
        elif not username:
            login_response = {
                'msg': 'Wpisz login.'
            }
            self.render("login.tpl", resp=login_response)
        elif username == 'admin' and password == settings_pass:
            self.set_secure_cookie("user", self.get_argument("name"))
            self.redirect(self.get_argument("next", "/"))
        else:
            login_response = {
                'msg': 'Zły login i hasło!'
            }
            self.render("login.tpl", resp=login_response)


class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.tpl")


class MobileHomeHandler(BaseHandler):

    def get(self):
        self.render("mbase.tpl")


class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.tpl")


class GraphsHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.render("graphs.tpl")


class DashHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'initv')
        self.render("dash.tpl",
                    init=[json.loads(x) for x in res])


class ControlHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    @tornado.web.authenticated
    def get(self):
        c = tornadoredis.Client()
        res = yield tornado.gen.Task(c.hvals, 'status')
        self.render("control.tpl",
                    init=[json.loads(x) for x in res])


class LogsHandler(BaseHandler):

    def get(self):
        self.render("logs.tpl")


class InfoHandler(BaseHandler):

    def get(self):
        self.render("info.tpl",
                    arch=sensnode.common.this_mach(),
                    system=sensnode.common.this_system(),
                    lavg=sensnode.common.loadavg(),
                    uptime=sensnode.common.uptime(),
                    cpu_temp=sensnode.common.cpu_temp(),
                    process=sensnode.common.process(),
                    disksize=sensnode.common.disksize())


class RESTHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self, query):
        self.set_header("Content-Type", "application/json")
        cl = tornadoredis.Client()
        """Pobieram wszystkie nazwy punktów"""
        nodes = yield tornado.gen.Task(cl.hkeys, 'initv')
        if query == 'list':
            """Wypisz liste dostępnch nodów"""
            self.write("%s" % (nodes))
        elif query not in nodes:
            """Brak punktu - poinformuj"""
            self.write(
                "Brak danych, wybierz inny punkt. Dostępne: %s" % (nodes))
        else:
            """Jak istnieje - pobierz"""
            nodevals = yield tornado.gen.Task(cl.hget, 'initv', query)
            self.write(nodevals)
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
        rdb = sensnode.store.redisdb()
        # zapisz status w bazie redis
        rdb.setStatus(msg)
        # wrzuć w kolejkę
        q = self.application.settings.get('queue')
        q.put(msg)
        self.write_message('{"control":"You send: %s"}' % (
            json.loads(str(msg))))

    def on_close(self):
        if self.client.subscribed:
            print "WebSocket closed"
            self.client.unsubscribe('nodes')
            self.client.disconnect()


class MiniDashHandler(BaseHandler):

    def get(self):
        self.write(".")


def main():
    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    connect = sensnode.connect.Connect(taskQ, resultQ, debug=debug)
    connect.daemon = True
    connect.start()

    redisdb = sensnode.store.redisdb(debug=debug)
    decoder = sensnode.decoder.Decoder(debug=debug)

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/admin", AdminHandler),
        (r"/control", ControlHandler),
        (r"/", DashHandler),
        (r"/graphs", GraphsHandler),
        (r"/m", MobileHomeHandler),
        (r"/minidash", MiniDashHandler),
        (r"/info", InfoHandler),
        (r"/logs", LogsHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/rest/([a-z]+)", RESTHandler),
        (r"/websocket", Websocket),
        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")})],
        queue=taskQ,
        template_path=os.path.join(os.path.dirname(__file__), "views"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/login",
        debug=True)

    httpServer = tornado.httpserver.HTTPServer(application)
    httpServer.listen(options.webapp_port)
    print "Nasluchuje na porcie:", options.webapp_port

    @tornado.gen.engine
    def checkResults():
        if not resultQ.empty():
            result = resultQ.get()
            if debug:
                print "BINARY: %s" % (result)
            decoded = decoder.decode(result)
            # filtr - FIXME
            decodedj = json.loads(decoded)
            if debug:
                print "JSON: %s" % (decoded)
            if decodedj['name'] not in filterout:
                leveldb.put("%s-%s" % (decodedj['name'], decodedj['timestamp']), decoded)
                if debug:
                    print "LevelDB: %s-%s %s" % (decodedj['name'], decodedj['timestamp'], decoded)
            # koniec
            redisdb.pubsub(decoded)
            for c in clients:
                c.write_message(result)

    mainLoop = tornado.ioloop.IOLoop.instance()
    scheduler = tornado.ioloop.PeriodicCallback(
        checkResults, 500, io_loop=mainLoop)
    scheduler.start()
    mainLoop.start()

if __name__ == "__main__":
    main()
