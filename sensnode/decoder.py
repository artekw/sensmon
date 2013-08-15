#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import simplejson as json

import common
import logging
import config

"""Import dekoderów punktów"""
from decoders.weathernode import weathernode
from decoders.powernode import powernode
from decoders.pirnode import pirnode
from decoders.testnode import testnode


class Decoder(config.Config):

    """Dekodowanie pakietów"""
    def __init__(self, debug=False):
        self.debug = debug
        config.Config.__init__(self, debug)

    def decode(self, line):

        if line.startswith("OK"):
            data = line.split(" ")

        if data:
            nodemap = config.Config.getNodeMap(self)
            nid = data[1]  # nodeid
            if nid in nodemap:
                decoder = nodemap.get(nid)
                fields = config.Config.getCurrentSensors(self, decoder)

                fields.append('name')
                fields.append('timestamp')  # dodajemy pozostałe pola

                if decoder in ['artekroom', 'outnode']:
                    tmp = self.filter(weathernode(data, decoder), fields)
                    return self.scaleValue(tmp)
                if decoder == 'powernode':
                    tmp = self.filter(powernode(data, decoder), fields)
                    return self.scaleValue(tmp)
                if decoder == 'pirnode':
                    tmp = self.filter(pirnode(data, decoder), fields)
                    return self.scaleValue(tmp)
                if decoder == 'testnode':
                    tmp = self.filter(testnode(data, decoder), fields)
                    return self.scaleValue(tmp)
            else:
                if self.debug:
                    logging.debug('Received data from unknown node!')
                    logging.debug('Data: %s' % (data))
        else:
            return

    def scaleValue(self, data):
        """TODO: napisać to lepiej"""
        scales = config.Config.getScale(self, data['name'])
        a = []

        for (k, v) in data.iteritems():
            if k in scales.keys():
                if scales[k] < 0:
                    return  # do przemyślenia
                elif scales[k] >= 0:
                    v = float(data[k])
                    v /= pow(10, int(scales[k]))
            a.append(v)
        return json.dumps(dict(zip(data.keys(), a)))

    def filter(self, data, fields):
        return dict((k, v) for (k, v) in data.iteritems() if k in fields)
