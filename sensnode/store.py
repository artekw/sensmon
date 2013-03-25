#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
import simplejson
import time

import common
import decoder
import config
import logging

class Store(decoder.Decoder):
    """Aktualne odczyty"""
    def __init__(self, debug=False):
        decoder.Decoder.__init__(self, debug)
        self.initdb()

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, channel='sensnode'):
        data = decoder.Decoder.decode(self)
        if data:
            json = simplejson.loads(data)
            self.rdb.hset("vals", json['name'],  data) # hash, field, data
            self.rdb.publish(channel, data)
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')