#!/usr/bin/python2
# -*- coding: utf-8 -*-

import simplejson
import time

import common
import reader
import config

class Decoder(reader.Reader, config.Config):
    """Dekodowanie pakietów i formatowanie"""
    def __init__(self, debug=False):
        self.debug = debug
        reader.Reader.__init__(self, debug)
        config.Config.__init__(self, debug)

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

        power1 = ((256 * b) + a)
        power2 = ((256 * d) + c)
        power3 = ((256 * f) + e)

        #print power1
        #print power2
        #print power3
        power = power1 + power2 + power3

        vrms = ((256 * j) + i)

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
        line = reader.Reader.serialread(self)

        if line.startswith("OK"):
            data = line.split(" ")

        if data:
            nodemap = config.Config.getNodeMap(self)
            nid = data[1] # nodeid
            if nid in nodemap:
                decoder = nodemap.get(nid)
                fields = config.Config.getCurrentSensors(self, decoder)

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

        scales = config.Config.getScale(self, name)
        value = float(value)

        if sensor in scales.keys():
            if scales[sensor] < 0:
                return # do przemyślenia
            elif scales[sensor] >= 0:
                value /= pow(10, scales[sensor])
            return value
        return