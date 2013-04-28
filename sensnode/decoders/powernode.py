#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def powernode(data, name):
    """Punkt mierzący pobór mocy biernej"""

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
    power = power1 + power2 + power3

    template = ({
        'name':name,
        'power': power,
        'vrms': ((256 * j) + i),
        'timestamp':timestamp
        })
    return dict((k,v) for (k,v) in template.iteritems())