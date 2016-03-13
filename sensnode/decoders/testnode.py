#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import datetime
import simplejson as json

def testnode(data, name):
    """Pomiar:
    - swiatła,
    - wlgotności
    - temperatury
    - ciśnienia
    - stanu baterii
    - napięcia beterii

    >> a = "OK 2 0 0 70 1 242 0 201 38 0 15 17"
    >> raw = a.split(" ")
    >> weathernode(raw, "weathernode")
    '{"name": "weathernode", "temp": "242", "lobat": "0", "humi": "326", "timestamp": 1364553092, "light": "0", "press": "9929", "batvol": "4367"}'
    """

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
    l = int(data[13])

    #nodeid = str(data[1])
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) #unix time

    template = ({
        'name':name,
        'temp': str(((256 * (f&3) + e) ^ 512) - 512),
        'batvol':str((256 * j) + i),
        'air':str((256 * l) + k),
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())
