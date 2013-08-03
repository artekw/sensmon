#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
import time
import corduroy
import simplejson as json
import hashlib
import random
from timestore import Client, TimestoreException

import common
import logging
import config

"""
Redis DB szablon:
- hash initv: dane chwilowe z czujek
- kanał nodes(domyślnie) - pubsub
- hash status: dane chwilowe przekaźników
"""


class redisdb():

    """Bazy Redis dla danych chwilowych"""
    def __init__(self, debug=False):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        if data:
            dataj = json.loads(data)
            self.rdb.hset("initv", dataj['name'], data)  # hash, field, data
            self.rdb.publish(channel, data)
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def setStatus(self, msg):
        """{"name": "relaynode", "status": 0, "cmd": 1}"""
        jmsg = json.loads(msg)
        self.rdb.hset('status', jmsg['name'] + "_" + jmsg['cmd'], str(msg))

    def getStatus(self, nodename):
        return self.rdb.hget("status", nodename)


class History():

    """
    Baza Timestore
    http://www.mike-stirling.com/redmine/projects/timestore
    """
    def __init__(self, host='127.0.0.1'):
        tsdb = Client(host)

    def createNode():
        """Utwórz node"""
        pass

    def setAdminKey(self, node, path='/var/lib/timestore'):
        """Ustaw klucz admina"""
        rand = random.random()

        ts.set_key()
        pass

    def setRWKeys(self, tskey):
        "Wygeneruj klucz do zapisu i odczytu"
        pass
