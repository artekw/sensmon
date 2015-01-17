#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import imp
import simplejson as json
from collections import OrderedDict

import common
import logging
from config import config
from plugins import plugins


class Decoder(object):

    """Dekodowanie pakietów"""
    def __init__(self, debug=False):
        #self._logger = logging.getLogger(__name__)
        self.debug = debug

        # inicjalizacja systemu pluginów - dekoderów nodów
        p = plugins(init=True)

    def decode(self, line):
        decoders = []

        if line.startswith("OK"):
            data = line.split(" ")
        else:
            print("WARNING: No data!")
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
                decoded_data = plug(data, nodemap[nid])
                return self.scale(decoded_data)

                '''
                # TODO
                # lista modułów z katalogu 'decoders'
                for f in os.listdir(os.path.abspath("./sensnode/decoders")):
                    module_name, ext = os.path.splitext(f)
                    if ext == ".py" and module_name != "__init__":
                        decoders.append(module_name)

                if decoder in ['artekroom', 'outnode']:
                    tmp = self.filter(weathernode(data, decoder), fields)
                    return self.scale(tmp)
                if decoder == 'powernode':
                    tmp = self.filter(powernode(data, decoder), fields)
                    return self.scale(tmp)
                if decoder == 'pirnode':
                    tmp = self.filter(pirnode(data, decoder), fields)
                    return self.scale(tmp)
                if decoder == 'testnode':
                    tmp = self.filter(testnode(data, decoder), fields)
                    return self.scale(tmp)
                '''
        else:
            return


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

    def filter(self, data, fields):
        return dict((k, v) for (k, v) in data.iteritems() if k in fields)
