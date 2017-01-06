#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import logging

# https://github.com/leporo/tornado-redis
import tornadoredis
import paho.mqtt.publish as mqtt

import simplejson as json
# http://pymotw.com/2/multiprocessing
import multiprocessing

import tornado.ioloop
import tornado.web
import tornado.template
import tornado.websocket
import tornado.gen
import tornado.httpserver
import tornado.escape
import tornado.autoreload
from tornado.options import define, options

# sesnode engine
import sensnode.decoder
import sensnode.connect
import sensnode.common
import sensnode.store
# import sensnode.logs as logs
from sensnode.config import config
from sensnode.weather import getWeather


# dev mode
debug = False
version = '0.45-dev'

# inicjalizacja menadżera konfiguracji
ci = config(init=True)

# ------------------------webapp settings--------------------#
# app
define("webapp_port", default=config().get("app", ['webapp', 'port']),
                      help="Run on the given port", type=int)
define("webapp_host", default=sensnode.common.get_ip_address(),
                      help="Run on the given hostname")

# lmdb
define("lmdb_enable",default=config().get("app", ['lmdb', 'enable']),
		help="LevelDB enabled")
define("lmdb_dbname",default=config().get("app", ['lmdb', 'dbname']),
		help="LevelDB database name")
define("lmdb_path",default=config().get("app", ['lmdb', 'path']),
		help="LevelDB path do database")
define("lmdb_forgot",default=config().get("app", ['lmdb', 'forgot']),
        help="Forgot nodes data")

# MQTT
define("mqtt_enable",default=config().get("app", ['mqtt', 'enable']),
		help="MQTT enabled")
define("mqtt_broker",default=config().get("app", ['mqtt', 'broker']),
		help="MQTT broker IP")
define("mqtt_port",default=config().get("app", ['mqtt', 'port']),
		help="MQTT broker port")

#OpenWeatherMap
define("city_name", default=config().get("app", ['weather', 'city']),
                  help="City name", type=int)
define("appid", default=config().get("app", ['weather', 'appid']),
                help="APPID to OpenWeatherMap")
# ----------------------end webapp settings------------------#


# klient Redis
c = tornadoredis.Client()
c.connect()
clients = []

if options.lmdb_enable:
    history = sensnode.store.history(options.lmdb_path, options.lmdb_dbname)


# --------------------------webapp code-----------------------#


class BaseHandler(tornado.web.RequestHandler):

    def get_current_user(self):
        return self.get_secure_cookie("user")


# Wylogowywanie
class LogoutHandler(BaseHandler):

    def get(self):
        self.clear_cookie("user")
        # self.redirect("/")
        self.redirect(self.get_argument("next", "/"))


# Logowanie
class LoginHandler(BaseHandler):

    def get(self):
        self.render("login.tpl", resp=None)

    def post(self):
        username = self.get_argument('name', '')
        password = self.get_argument('pass', '')
        print username, password

        settings_pass = config().get("app", ['webapp', 'password'])

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


# zakładka Home
class HomeHandler(BaseHandler):

    def get(self):
        self.render("home.tpl")


# panel administatora
class AdminHandler(BaseHandler):

    @tornado.web.authenticated
    def get(self):
        self.render("admin.tpl")


# zakładka Wykresy
class GraphsHandler(BaseHandler):

    def get(self, node, sensor, timerange):
        self.render("graphs.tpl")


# zakładka Dashboard
class DashHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render("dash.tpl")


# zakładka Przełaczniki
class SwitchesHandler(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.render("switches.tpl")


# zakłatka Intro
class IntroHandler(BaseHandler):

    def get(self):
        weather = getWeather(city=options.city_name, appid=options.appid)
        self.render("intro.tpl", w=weather)


# zakładka System
class InfoHandler(BaseHandler):

    def get(self):
        self.render("info.tpl",
                    arch=sensnode.common.this_mach(),
                    system=sensnode.common.this_system(),
                    lavg=sensnode.common.loadavg(),
                    uptime=sensnode.common.uptime(),
                    cpu_temp=sensnode.common.cpu_temp(),
                    machine=sensnode.common.machine_detect()[0]
                    )


# RESTful
# history/<node>/<sensor>/<timerange>
class GetHistoryData(BaseHandler):

    def get(self, node, sensor, timerange):
        self.set_header("Content-Type", "application/json")
        response = []

        try:
            response = { 'data' :  history.get_toJSON(node, sensor, timerange) }
            self.write(response)
            self.finish()
        except KeyError, e:
            self.set_status(404)
            self.finish("%s nie znaleziono" % e)


# /initv/
class GetInitData(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header("Content-Type", "application/json")
        _cl = tornadoredis.Client()
        _initv = yield tornado.gen.Task(_cl.get, 'initv')
        data_json = tornado.escape.json_encode(_initv)
        self.write(data_json)
        self.finish()


# /status/
class GetStatus(BaseHandler):

    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        self.set_header("Content-Type", "application/json")
        _cl = tornadoredis.Client()
        status = yield tornado.gen.Task(_cl.get, 'relays_status')
        data_json = tornado.escape.json_encode(status)
        self.write(data_json)
        self.finish()


# Websocket
class Websocket(tornado.websocket.WebSocketHandler):

    def __init__(self, *args, **kwargs):
        super(Websocket, self).__init__(*args, **kwargs)
        self.listen()

    @tornado.web.asynchronous
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

    def on_close(self):
        if self.client.subscribed:
            print "WebSocket closed"
            self.client.unsubscribe('nodes')
            self.client.disconnect()


def publish(jsondata):
	"""
	>> data = {'vrms': 220.39, 'timestamp': 1428338500, 'name': 'powernode', 'power': 246}
	>> publish(data, hostname="localhost" port="1883")
	/powernode/vrms 220.39
	/powernode/power 246
	/powernode/timestamp 1428338500
	"""
	name = jsondata['name']
	for k, v in jsondata.iteritems():
		mqtt.single("/sensmon/%s/%s" % (name, k), v, hostname=options.mqtt_broker, port=options.mqtt_port)


# funkcja główna
def main():
    taskQ = multiprocessing.Queue()
    resultQ = multiprocessing.Queue()

    connect = sensnode.connect.Connect(taskQ, resultQ, debug=debug)
    connect.daemon = True
    connect.start()

    redisdb = sensnode.store.redisdb(debug=debug)
    decoder = sensnode.decoder.Decoder(debug=debug)

    logger = logging.getLogger()

    tornado.options.parse_command_line()
    application = tornado.web.Application([
        (r"/admin", AdminHandler),
        (r"/dash", DashHandler),
        (r"/switches", SwitchesHandler),
        (r"/graphs/(?P<node>[^\/]+)/?(?P<sensor>[^\/]+)?/?(?P<timerange>[^\/]+)?", GraphsHandler),
        (r"/info", InfoHandler),
		(r"/", IntroHandler),
        (r"/login", LoginHandler),
        (r"/logout", LogoutHandler),
        (r"/initv", GetInitData),
        (r"/status", GetStatus),
        (r"/history/(?P<node>[^\/]+)/?(?P<sensor>[^\/]+)?/?(?P<timerange>[^\/]+)?", GetHistoryData),
        (r"/websocket", Websocket),
        (r'/favicon.ico', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.dirname(__file__), "static")})],
        queue=taskQ,
        template_path=os.path.join(os.path.dirname(__file__), "views"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
        login_url="/login",
        # xsrf_cookies=True,
        debug=True)

    httpServer = tornado.httpserver.HTTPServer(application)
    httpServer.listen(options.webapp_port)
    print "sensmon %s started at %s port" % (version, options.webapp_port)
    print "Go to page http://%s:%s" % (options.webapp_host, options.webapp_port)

    @tornado.gen.engine
    def checkResults():
        if not resultQ.empty():
            # RAW data
            result = resultQ.get()
            # Decoded data
            decoded = decoder.decode(result)
            # Update sensors data
            update = decoder.update(decoded)
            #print ("RAW: %s" % (result))
            #print ("JSON %s" % (decoded))
            #print ("JSON Updated %s" % (update))

            # if lmdb enabled store data
            if options.lmdb_enable:
                if decoded['name'] not in options.lmdb_forgot:
                    key = ('%s-%d' %  (decoded['name'],decoded['timestamp'])).encode('ascii')
                    value = ('%s' % decoded).encode('ascii')
                    history.put(key, value)
                    if debug:
                        logger.debug("LevelDB: %s %s" % (key, decoded))
            # If MQTT enabled publish
            if options.mqtt_enable:
                publish(decoded)

            # initv - actual data from sensors store in Redis
            redisdb.pubsub(update)
            for c in clients:
                c.write_message(update)

    mainLoop = tornado.ioloop.IOLoop.instance()
    tornado.autoreload.start(mainLoop)
    scheduler = tornado.ioloop.PeriodicCallback(
        checkResults, 500, io_loop=mainLoop)

    scheduler.start()
    mainLoop.start()


if __name__ == "__main__":
    main()
