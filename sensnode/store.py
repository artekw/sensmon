#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import ast
import time
from itertools import islice
import simplejson as json
import redis
import logging
from sensnode.config import config


class redisdb():

    """Baza danych tymczasowych"""
    def __init__(self, host="localhost", debug=True):
        self.debug = debug
        self.host = host
        self.initdb(self.host)

    def initdb(self, host="localhost", port=6379):
        """Init redis"""
        self.rdb = redis.Redis(host, port)
        # init data - inf not exist get data from nodescfg
        if not self.rdb.exists('relays_status'):
            self.rdb.set('relays_status', json.dumps(config().getConfig('nodes')))

    def websocket_channel(self, data, channel='nodes'):
        """
        Set initv: dane czujników
        Kanał nodes(domyślnie) - kanał do wymiany danych po Websocket(przeglądarka-nody)
        """
        if data:
            self.rdb.set("initv", data)  # name, value
            self.rdb.publish(channel, data)  # channel, value
            if self.debug:
                logging.debug('Data publish on channel')
                logging.debug('Submit init values')

    def get_initv(self):
        """Return initv"""
        return self.rdb.get("initv")

    def append_key(self, list, string):
        """Add to list"""
        self.rdb.lpush(list, string)
        # trim list to 2 items
        self.rdb.ltrim(list, 0, 2)

    def pop_key(self, list, string):
        """Pop item from list"""
        self.rdb.lpush(list, string)
        # trim list to 2 items
        self.rdb.ltrim(list, 0, 2)

    def alarm_channel(self, string, channel='alarm'):
        """Set string in base with timeout"""
        self.rdb.publish(channel, string)

    def setStatus(self, msg):
        """
        Hash status: dane statusów przekaźników
        {"node_id": 19, "node_name": "lab', relay_name": "lamp", "state": 1, "cmd": 01}
        """
        # json format
        incoming_statuses = json.loads(msg)
        # jsontree format
        prevoius_statuses = json.loads(self.rdb.get('relays_status'))
        prevoius_statuses = jsontree.clone(prevoius_statuses)

        # update statuses of realys and add to redis(set)
        if prevoius_statuses[incoming_statuses['node_name']].input.relay[incoming_statuses["relay_name"]].has_key:
            for k, v in prevoius_statuses[incoming_statuses['node_name']].input.relay.iteritems():
                prevoius_statuses[incoming_statuses['node_name']].input.relay[incoming_statuses["relay_name"]].state = incoming_statuses["state"]
        else:
            return

        self.rdb.set('relays_status', jsontree.dumps(prevoius_statuses))


class history():

    """Baza danych historycznych"""
    def __init__(self, path, dbname):
        import lmdb

        self.path = path
        self.dbname = dbname

        dirname = self.path + "/" + self.dbname

        if not os.path.exists(dirname):
            os.makedirs(dirname)

        self.env = lmdb.open("%s/%s/history.lmdb" % (self.path, self.dbname), map_size=51200000)
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

            with self.env.begin() as txn:
                cursor = txn.cursor()
                cursor.set_range(start_key.encode('ascii'))

                data = [value for key, value in cursor if nodename in key]

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
            with self.env.begin(write=True) as txn:
                txn.put(key, value)

    def get_toJSON(self, nodename, sensor, timerange='1h'):
        """Pobierz zakres danych w formacie JSON"""
        data = []
        if self.dbconnected:
            values = self.get(nodename, timerange)
            # milliseconds for JavaScript
            data = [[ast.literal_eval(v)['timestamp'] * 1000, ast.literal_eval(v)[sensor]] for v in values]
            return data
