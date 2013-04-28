#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
import time
import simplejson as json

import common
import logging
import config
import logging

"""
Redis DB szablon:
- hash initv: dane chwilowe z czujek
- kanał nodes(domyślnie) - pubsub
- hash status: dane chwilowe przekaźników
"""

class Store():
    """Aktualne odczyty"""
    def __init__(self, debug=False):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes' ):
        #data = decoder.Decoder.decode(self)
        if data:
            dataj = json.loads(data)
            self.rdb.hset("initv", dataj['name'], data) # hash, field, data
            self.rdb.publish(channel, data)
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def setStatus(self, msg):
        """{"name": "relaynode", "status": 0, "cmd": 1}"""
        jmsg = json.loads(msg)
        self.rdb.hset('status', jmsg['name']+"_"+jmsg['cmd'], str(msg))

    def getStatus(self, nodename):
        return self.rdb.hget("status", nodename)
