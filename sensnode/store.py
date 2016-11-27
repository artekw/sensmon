#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
# https://plyvel.readthedocs.org
import plyvel as leveldb
import os
import ast
import time
from itertools import islice
import simplejson as json

import common
import logging
import config


class redisdb():

    """Baza danych tymczasowych"""
    def __init__(self, debug=True):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        """
        Hash initv: dane chwilowe z czujników
        Kanał nodes(domyślnie) - kanał do wymiany danych po Websocket(przeglądarka-nody)
        """
        if data:
            data_str = json.dumps(data)
            self.rdb.set("initv", data)  # name, value
            self.rdb.publish(channel, data)  # channel, value
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def setStatus(self, msg):
        """
        Hash status: dane chwilowe przekaźników
        {"name": "relaynode", "status": 0, "cmd": 1}
        """
        jmsg = json.loads(msg)
        self.rdb.hset('status', jmsg['name'] + "_" + jmsg['cmd'], str(msg))

    def getStatus(self, nodename):
        """Spwardzanie statusu przekaźnika"""
        return self.rdb.hget("status", nodename)


class history():

    """Baza danych historycznych"""
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
        """Czy jest połączenie z bazą?"""
        return self.dbconnected

    def get(self, nodename, timerange):
        """Pobierz zakresy danych"""

        # zakresy
        ranges = {'1h' : 3600,
                'day' : 86400,
                '2d': 172800,
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
            iterator.close()

            """
            roblad

            if (ts - ranges[timerange]) > (ts - 604900):
                #print 'week'
                return data
            elif(ts - ranges[timerange]) < (ts - 604900) and (ts - ranges[timerange]) > (ts - 2593000):
                data_filtered = [value for value in (islice(data,0,len(data), 10))]
                #print 'month - 3month'
                return data_filtered
            elif (ts - ranges[timerange]) < (ts - 2593000):
                #print 'above 3month'
                data_filtered = [value for value in (islice(data,0,len(data), 100))]
                return data_filtered
            """
            return data

    def put(self, key, value):
        """Wstawianie danych"""
        if self.dbconnected:
            self.lvldb.put(key, value)

    def get_toJSON(self, nodename, sensor, timerange='1h'):
        """Pobierz zakres danych w formacie JSON"""
        data = []
        if self.dbconnected:
            values = self.get(nodename, timerange)
            # milliseconds for JavaScript
            data = [[ast.literal_eval(v)['timestamp'] * 1000, ast.literal_eval(v)[sensor]] for v in values]
            return data
