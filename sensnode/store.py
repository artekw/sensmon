#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
import os
import time
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
    def __init__(self, host='127.0.0.1:8080'):
        self.tsdb = Client(host)
        self.adminkey = self.getAdminKey()

    def createNode(self, node_id, interval, public=False):
        """Utwórz node"""

        array = {
                'interval': interval,
                'decimation': [20, 6, 6, 4, 7],
                'metrics': [ {
                            'pad_mode' : 0,
                            'downsample_mode' : 0
                            } ]
                }

        try:
            self.tsdb.create_node(node_id, array, key = self.adminkey)
            node_created = True
        except TimestoreException as e:
            node_created = False
            if e.status == 403:
                print "Node exist?"
                try:
                    print "Try to erase %s node..." % (node_id)
                    self.tsdb.delete_node(node_id, key = self.adminkey)
                    print "Deleted, try to new one"
                except TimestoreException as e:
                    if e.status == 403:
                        print "Admin key rejected!"
                        raise
            else:
                raise
        if node_created and not public:
            self.setRWKeys(node_id)

    def getAdminKey(self, path='/var/lib/timestore'):
        """Pobierz klucz admina z pliku"""

        if os.path.isfile('%s/%s' % (path, 'adminkey.txt')):
            with open('%s/%s' % (path, 'adminkey.txt'), 'r') as adminkey_file:
                adminkey = adminkey_file.readline().rstrip()
                return adminkey
        else:
            logging.warning('Uruchom bazę timestore, brak pliku z kluczem admina!')
            pass

    def setRWKeys(self, node_id):
        "Wygeneruj klucz do zapisu i odczytu dla punktów prywatych"

        m = hashlib.md5()
        m.update(str(random.random()))
        readkey = m.hexdigest()

        m.update(str(random.random()))
        writekey = m.hexdigest()

        self.tsdb.set_key(node_id, 'read', readkey, key = self.adminkey)
        self.tsdb.set_key(node_id, 'write', writekey, key = self.adminkey)
        print 'Read key: %s' % (readkey)
        print 'Write key: %s' % (writekey)
        # return readkey, writekey
        print 'Keys generated!'
