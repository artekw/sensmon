#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import simplejson as json
from collections import OrderedDict

import sensnode.common
import logging
from sensnode.config import config
from sensnode.plugins import plugins


class Decoder(object):

    '''Decoders of binary packets from wireless node'''
    def __init__(self, debug=False):
        self._logger = logging.getLogger(__name__)
        self.debug = debug
        self.nodescfg = jsontree.clone(config().getConfig('nodes'))

        # inicjalizacja systemu pluginów - dekoderów nodów
        p = plugins(init=True)


    def decode(self, line):
        '''Decoder'''
        decoders = []

        # data must have OK on front
        if line.startswith("OK"):
            data = line.split(" ")
        else:
            print("WARNING: Bad data!")
            print("Source: %s") % line
            return

        if data:
            # nodeid
            nid = int(data[1])
            # dict id:name
            nodemap = config().getMap()
            # check if node is on the list
            if nid in nodemap.keys():
                # search for proper plugin - decoder
                plug = plugins().plugin(nodemap[nid])
                # return data
                decoded_data = plug(data)

                return self.scale(decoded_data)
            else:
                return
        else:
            return

    def update(self, _new_value):
        '''Copy node config and add to output
        sensors "raw" key with received data'''

        if _new_value != None:
            new_value = jsontree.clone(_new_value)

            if self.nodescfg.has_key(new_value.name):
                for k,v in self.nodescfg[new_value.name].output.sensors.iteritems():
                    self.nodescfg[new_value.name].output.sensors[k].raw = new_value[k]
            else:
                return

            return jsontree.dumps(self.nodescfg)

    def scale(self, data):
        '''Scale data'''
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
