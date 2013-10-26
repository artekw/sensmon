#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import simplejson as json
from collections import OrderedDict

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
        self._logger = logging.getLogger(__name__)
        self.debug = debug
        config.Config.__init__(self, debug)

    def decode(self, line):
        decoders = []

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

                # TODO
                # lista modułów z katalogu 'decoders'
                for f in os.listdir(os.path.abspath("./sensnode/decoders")):
                    module_name, ext = os.path.splitext(f)
                    if ext == ".py" and module_name != "__init__":
                        decoders.append(module_name)

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
                    self._logger.debug('Received data from unknown node!')
                    self._logger.debug('Data: %s' % (data))
        else:
            return

    def scaleValue(self, data):
        """TODO: napisać to lepiej"""
        scales = config.Config.getScale(self, data['name'])
        scaled_values = []

        for (k, v) in data.iteritems():
            if k in scales.keys():
                if scales[k] > 0:
                    v = float(data[k])
                    v /= pow(10, int(scales[k]))
            scaled_values.append(v)
        new_dict = dict(zip(data.keys(), scaled_values))
        return json.dumps(OrderedDict(sorted(new_dict.items(), key=lambda t: t[0])))

    def filter(self, data, fields):
        return dict((k, v) for (k, v) in data.iteritems() if k in fields)
