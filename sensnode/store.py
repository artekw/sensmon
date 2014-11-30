#!/usr/bin/python2
# -*- coding: utf-8 -*-

import redis
# https://plyvel.readthedocs.org
import plyvel as leveldb
import time
import simplejson as json
import hashlib
import random

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

    """Dane chwilowe"""
    def __init__(self, debug=True):
        self.initdb()
        self.debug = debug

    def initdb(self, host="localhost", port=6379):
        self.rdb = redis.Redis(host, port)

    def pubsub(self, data, channel='nodes'):
        if data:
            data_str = json.dumps(data)
            self.rdb.hset("initv", data['name'], data_str)  # hash, field, data
            self.rdb.publish(channel, data_str)
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
	
	"""Dane historyczne"""
	def __init__(self, path, dbname, create_db):
		self.path = path
		self.dbname = dbname
		self.create_db = create_db
		self.lvldb = leveldb.DB("%s/%s" % (self.path, 
										self.dbname), 
										create_if_missing=self.create_db)
		self.dbconnected = True
		
	def is_connected(self):
		return self.dbconnected

	def get(self, nodename, timerange):
		''' 
		pewnie to trafi do pliku json, aby 
		zakresy były wspolne dla Js i Pythona
		'''
		
		ranges = {'1h' : 3600,
				'2h' : 7200,
				'day' : 86400,
				'week' : 604800,
				'month' : 2419200} 

		if self.dbconnected:
			data = []
			ts = int(time.time())
			start_key = '%s-%s' % (nodename, ts-ranges[timerange])
			stop_key = '%s-%s' % (nodename, ts)

			#print ('Data for last %s') % (timerange)
			for key, value in self.lvldb.iterator(
								start=(start_key).encode('ascii'), 
								stop=(stop_key).encode('ascii'),
								include_start=True,
								include_stop=True):
				data.append(value) # lista ?
			return data

	def put(self, key, value):
		if self.dbconnected:
			self.lvldb.put(key, value)
			
	def select(self, sensor, nodename, timerange='1h'):
		data = self.get(nodename, timerange)
		for i in data:
			line = i
			print line['temp']

		
