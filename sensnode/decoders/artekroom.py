#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def artekroom(data, name):
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

    #nodeid = str(data[1])
    timestamp = int(time.time()) #unix time

    template = ({
        'name':name,
        'humi': str((256 * d) + c),
        'temp': str(((256 * (f&3) + e) ^ 512) - 512),
        'press': str((256 * h) + g),
        'batvol':str((256 * k) + j),
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())