#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'Artur Wronowski'
__version__ = '0.5-dev'
__appname__ = 'sensnode-core'
__license__ = 'MIT'
__email__ = 'arteqw@gmail.com'

# TODO:
# - testy, testy
# - wysyłanie do sesnbase- OOK (On-Off-Keyring)


import socket
import redis
import time
import datetime
import calendar
import sys
import simplejson
import logging
import platform
import os

debug = False
c = ""

logging.basicConfig(
        format='%(asctime)-25s %(threadName)-15s %(levelname)-10s %(message)s',
        level=logging.DEBUG,
        datefmt='%d/%m/%Y %H:%M:%S')


with open('settings.json') as settings_file:
	settings_cfg = simplejson.load(settings_file)
with open('static/nodes.json') as nodes_file:
	nodes_cfg = simplejson.load(nodes_file)
with open('static/nodemap.json') as nodemap_file:
	nodemap_cfg = simplejson.load(nodemap_file)

#########################################################

def get_version():
		return __version__

def get_author():
		return __author__

def get_license():
		return __license__

def get_email():
		return __email__

########################################################

def this_system():
	return platform.system()

def this_mach():
	return platform.machine()

def loadavg():
	return os.getloadavg()

########################################################

class Config(object):
	"""Zarzadzanie konfiguracja w json"""
	def __init__(self, debug=False):
		self.nodes_cfg = nodes_cfg
		self.nodemap_cfg = nodemap_cfg
		self.settings_cfg = settings_cfg
		self.debug = debug

	def getNodeMap(self):
		"""Tworzy slownik nodeMap"""
		return dict(zip(self.nodemap_cfg['nodemap'].viewkeys(), self.nodemap_cfg['nodemap'].values()))
	def getCurrentSensors(self, name):
		return self.nodes_cfg[name].keys()
	def getCurrentNodes(self):
		return self.nodes_cfg.keys()
	def getScale(self, name):
		"""Tworzy slownik sensor : skala"""
		# TODO: pomijanie wprowadzania skali
		scales = [self.nodes_cfg[name][str(x)]['scale'] for x in self.getCurrentSensors(name)]
		return dict(zip(self.nodes_cfg[name].viewkeys(), scales))

########################################################

class Reader(object):
	"""Odczyt danych z punktow"""
	def __init__(self, debug=False):
		self.settings_cfg = settings_cfg
		self.debug = debug
		self.connected = False

		try:
			host = self.settings_cfg['settings']['daemon']['host']
			port = self.settings_cfg['settings']['daemon']['port']
			if self.debug:
				logging.debug('Trying connect to %s:%s' % (host, str(port)))
		except:
			print "Can't read from config."
			sys.exit(3)

		try:
			self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.soc.connect((host, port))
			if self.debug:
				logging.debug('Connected to %s:%s' % (host, str(port)))
			self.connected = True

		except socket.error:
			logging.warning("Can't connect to %s:%s" % (host, str(port)))
			self.connected = False
			sys.exit(3)

	def is_connected(self):
		return self.connected

	def serialread(self):
		"""Czyta z konsoli szeregowej"""
		line = ''
		if self.connected:
			while True:
				c = self.soc.recv(1)
				if c == '\n' or c == '':
					break
				else:
					line += c
			return line

	def __del__(self):
		self.soc.close()

########################################################

class Decoder(Reader, Config):
	"""Dekodowanie pakietów i formatowanie"""
	def __init__(self, debug=False):
		self.debug = debug
		Reader.__init__(self, debug)
		Config.__init__(self, debug)

	def artekroom(self, data, name, fields):
		"""Punkt pogodowy"""

		a = int(data[2])
		b = int(data[3])
		c = int(data[4])
		d = int(data[5])
		e = int(data[6])
		f = int(data[7])
		g = int(data[8])
		h = int(data[9])
		i = int(data[10])
		j = int(data[11])
		k = int(data[12])

		#nodeid = str(data[1])
		timestamp = int(time.time()) #unix time

		light = str((256 * b) + a)
		humi = str((256 * d) + c)
		temp = str(((256 * (f&3) + e) ^ 512) - 512)
		press = str((256 * h) + g)
		lobat = str(i)
		batvol = str((256 * k) + j)

		if self.debug:
			logging.debug('Received data from %s' % (name) )

		fields.append('name')
		fields.append('timestamp') # dodajemy pozostałe pola

		template = ({
			'name':name,
			'light':self.scaleValue(light, name, 'light'),
			'humi':self.scaleValue(humi, name, 'humi'),
			'temp':self.scaleValue(temp, name, 'temp'),
			'press':self.scaleValue(press, name, 'press'),
			'lobat':self.scaleValue(lobat, name, 'lobat'),
			'batvol':self.scaleValue(batvol, name, 'batvol'),
			'timestamp':timestamp
			})

		result = dict((k,v) for (k,v) in template.iteritems() if k in fields)

		return simplejson.dumps(result)

	def outnode(self, data, name, fields):
		"""Punkt pogodowy"""

		a = int(data[2])
		b = int(data[3])
		c = int(data[4])
		d = int(data[5])
		e = int(data[6])
		f = int(data[7])
		g = int(data[8])
		h = int(data[9])
		i = int(data[10])
		j = int(data[11])
		k = int(data[12])

		#nodeid = str(data[1])
		timestamp = int(time.time()) #unix time

		light = str((256 * b) + a)
		humi = str((256 * d) + c)
		temp = str(((256 * (f&3) + e) ^ 512) - 512) # ujemne
		press = str((256 * h) + g)
		lobat = str(i)
		batvol = str((256 * k) + j)

		if self.debug:
			logging.debug('Received data from %s' % (name) )

		fields.append('name')
		fields.append('timestamp') # dodajemy pozostałe pola

		template = ({
			'name':name,
			'light':self.scaleValue(light, name, 'light'),
			'humi':self.scaleValue(humi, name, 'humi'),
			'temp':self.scaleValue(temp, name, 'temp'),
			'press':self.scaleValue(press, name, 'press'),
			'lobat':self.scaleValue(lobat, name, 'lobat'),
			'batvol':self.scaleValue(batvol, name, 'batvol'),
			'timestamp':timestamp
			})

		result = dict((k,v) for (k,v) in template.iteritems() if k in fields)

		return simplejson.dumps(result)

	def powernode(self, data, name, fields):
		"""Punkt mierzący pobór mocy"""

		a = int(data[2])
		b = int(data[3])
		c = int(data[4])
		d = int(data[5])
		e = int(data[6])
		f = int(data[7])
		g = int(data[8])
		h = int(data[9])
		i = int(data[10])
		j = int(data[11])

		#nodeid = str(data[1])
		timestamp  = int(time.time())

		power = str(((((256 * b&3) + a) ^ 512) - 512) + ((((256 * d&3) + c) ^ 512) - 512) + ((((256 * f&3) + e) ^ 512) - 512))
		vrms = str((256 * j) + i)

		if self.debug:
			logging.debug('Received data from %s' % (name) )

		fields.append('name')
		fields.append('timestamp') # dodajemy pozostałe pola

		template = ({
			'name':name,
			'power':self.scaleValue(power, name, 'power'),
			'vrms':self.scaleValue(vrms, name, 'vrms'),
			'timestamp':timestamp
			})

		result = dict((k,v) for (k,v) in template.iteritems() if k in fields)

		return simplejson.dumps(result)

	def pt1000Node(self, data, name, fields):
		"""Punkt testowy"""

		a = int(data[2])
		b = int(data[3])
		c = int(data[4])
		d = int(data[5])
		e = int(data[6])
		f = int(data[7])

		#nodeid = str(data[1])
		timestamp  = int(time.time())

		count = d << 24 | c << 16 | b << 8 | a #long int
		temp = str((256 * f) + e)

		if self.debug:
			logging.debug('Received data from %s' % (name) )

		fields.append('name')
		fields.append('timestamp') # dodajemy pozostałe pola

		template = ({
			'name':name,
			'count':self.scaleValue(count, name, 'count'),
			'temp':self.scaleValue(temp, name, 'temp'),
			'timestamp':timestamp
			})

		result = dict((k,v) for (k,v) in template.iteritems() if k in fields)

		return simplejson.dumps(result)

	def testnode(self, data, name, fields):
		"""Punkt testowy"""

		a = int(data[2])
		b = int(data[3])
		c = int(data[4])
		d = int(data[5])
		e = int(data[6])
		f = int(data[7])

		#nodeid = str(data[1])
		timestamp  = int(time.time())

		count = d << 24 | c << 16 | b << 8 | a #long int
		batvol = str((256 * f) + e)

		if self.debug:
			logging.debug('Received data from %s' % (name) )

		fields.append('name')
		fields.append('timestamp') # dodajemy pozostałe pola

		template = ({
			'name':name,
			'count':self.scaleValue(count, name, 'count'),
			'batvol':self.scaleValue(batvol, name, 'batvol'),
			'timestamp':timestamp
			})

		result = dict((k,v) for (k,v) in template.iteritems() if k in fields)

		return simplejson.dumps(result)

	def decode(self):
		line = Reader.serialread(self)

		if line.startswith("OK"):
			data = line.split(" ")

		if data:
			nodemap = Config.getNodeMap(self)
			nid = data[1] # nodeid
			if nid in nodemap:
				decoder = nodemap.get(nid)
				fields = Config.getCurrentSensors(self, decoder)

				if decoder == 'artekroom':
					return self.artekroom(data, decoder, fields)
				if decoder == 'outnode':
					return self.outnode(data, decoder, fields)
				if decoder == 'powernode':
					return self.powernode(data, decoder, fields)
				if decoder == 'pt1000Node':
					return self.pt1000Node(data, decoder, fields)
				if decoder == 'testnode':
					return self.testnode(data, decoder, fields)
			else:
				if self.debug:
					logging.debug('Received data from unknown node!')
					logging.debug('Data: %s' % (data))
		else:
			return

	def scaleValue(self, value, name, sensor):

		scales = Config.getScale(self, name)
		value = float(value)

		if sensor in scales.keys():
			if scales[sensor] < 0:
				return # do przemyślenia
			elif scales[sensor] >= 0:
				value /= pow(10, scales[sensor])
			return value
		return



########################################################

class Store(Decoder):
	"""Aktualne odczyty"""
	def __init__(self, debug=False):
		Decoder.__init__(self, debug)
		self.initdb()

	def initdb(self, host="localhost", port=6379):
		self.rdb = redis.Redis(host, port)

	def pubsub(self, channel='sensnode'):
		data = Decoder.decode(self)
		if data:
			json = simplejson.loads(data)
			self.rdb.hset("vals", json['name'],  data) # hash, field, data
			self.rdb.publish(channel, data)
			if self.debug:
				logging.debug('Data publish on channel')
				logging.debug('Submit init values')
