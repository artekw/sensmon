#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
# https://plyvel.readthedocs.org
import plyvel as leveldb
import os
import ast
import time
import simplejson as json

import common
import logging
import config

"""
Redis DB szablon:
- hash initv: dane chwilowe z czujnikow
- kanał nodes(domyślnie) - pubsub
- hash status: dane chwilowe przekaźników
"""


class redisdb():

    """Temporary data"""
    def __init__(self, debug=True):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        if data:
            data_str = json.dumps(data)
            self.rdb.set("initv", data)  # name, value
            self.rdb.publish(channel, data)  # channel, value
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def setStatus(self, msg):
        """{"name": "relaynode", "status": 0, "cmd": 1}"""
        jmsg = json.loads(msg)
        self.rdb.hset('status', jmsg['name'] + "_" + jmsg['cmd'], str(msg))

    def getStatus(self, nodename):
        return self.rdb.hget("status", nodename)


class history():

    '''Store data in base for future use ie. graphs'''
    def __init__(self, path, dbname):
        self.path = path
        self.dbname = dbname
        #self.create_db = create_db

        dirname = self.path + "/" + self.dbname

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.lvldb = leveldb.DB("%s/%s" % (self.path,
                                        self.dbname),
                                        create_if_missing=True)
        self.dbconnected = True

    def is_connected(self):
        return self.dbconnected

    def get(self, nodename, timerange):

        ranges = {'1h' : 3600,
                'day' : 86400,
                '2days': 172800,
                'week' : 604800,
                'month' : 2592000}

        if self.dbconnected:
            data = []
            ts = int(time.time())
            start_key = '%s-%s' % (nodename, ts-ranges[timerange])
            stop_key = '%s-%s' % (nodename, ts)

            iterator = self.lvldb.iterator(start=(start_key).encode('ascii'),
                                            stop=(stop_key).encode('ascii'),
                                            include_start=True,
                                            include_stop=True)
            data = [value for key, value in iterator]
            return data

    def put(self, key, value):
        if self.dbconnected:
            self.lvldb.put(key, value)

    def select(self, nodename, sensor, timerange='1h'):
        data = []
        if self.dbconnected:
            values = self.get(nodename, timerange)
            data = [[ast.literal_eval(v)['timestamp'], ast.literal_eval(v)[sensor]] for v in values]
            return data
