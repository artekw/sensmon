#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import jsontree
import simplejson as json
from collections import OrderedDict

import common
import logging
from config import config
from plugins import plugins


class Decoder(object):

    """Decoders of binary packets from wireless node"""
    def __init__(self, debug=False):
        self._logger = logging.getLogger(__name__)
        self.debug = debug
        self.nodescfg = jsontree.clone(config().getConfig('nodes'))

        # inicjalizacja systemu pluginów - dekoderów nodów
        p = plugins(init=True)


    def decode(self, line):
        """Dekoder"""
        decoders = []

        # zaczyna się o OK
        if line.startswith("OK"):
            data = line.split(" ")
        else:
            print("UWAGA: Brak danych!")
            return

        if data:
            # nodeid z otrzymanych danych
            nid = int(data[1])
            # słownik id:name
            nodemap = config().getMap()
            # sprawdzam czy jest na liście
            if nid in nodemap.keys():
                # szukamy właściwej wtyczki - dekodera
                plug = plugins().plugin(nodemap[nid])
                # zwracamy zdekodowane dane wg szablonu
                decoded_data = plug(data)

                return self.scale(decoded_data)
        else:
            return

    def update(self, _new_value):
        """Add to node config "raw" value with data from wireless nodes"""

        new_value = jsontree.clone(_new_value)

        # FIXME - rozróznianie output i input
        if self.nodescfg.has_key(new_value.name):
            for k,v in self.nodescfg[new_value.name].output.sensors.iteritems():
                self.nodescfg[new_value.name].output.sensors[k].raw = new_value[k]
        else:
            return

        return jsontree.dumps(self.nodescfg)

    def scale(self, data):
        """TODO: napisać to lepiej"""
        scales = config().getScale(data['name'])
        scaled_values = []

        for (k, v) in data.iteritems():
            if k in scales.keys():
                if scales[k] > 0:
                    v = float(data[k])
                    v /= pow(10, int(scales[k]))
            scaled_values.append(v)
        new_dict = dict(zip(data.keys(), scaled_values))
        return json.loads(json.dumps(OrderedDict(sorted(new_dict.items(), key=lambda t: t[0]))))

        #return new_dict.items()

        #return  dict((k,v) for (k,v) in template.iteritems())

#    def filter(self, data, fields):
#        return dict((k, v) for (k, v) in data.iteritems() if k in fields)
