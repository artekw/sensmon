#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def outnode(data, name):
    """Outnode"""

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
        'temp': str(((256 * (f&3) + e) ^ 512) - 512),
        'batvol':str((256 * k) + j),
        'timestamp':timestamp
         })

    return  dict((k,v) for (k,v) in template.iteritems())
