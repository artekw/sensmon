#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def testnode(data, name):
    """Punkt testowy"""

    a = int(data[2])
    b = int(data[3])
    c = int(data[4])
    d = int(data[5])
    e = int(data[6])
    f = int(data[7])

    #nodeid = str(data[1])
    timestamp  = int(time.time())

    template = ({
        'name':name,
        'count': d << 24 | c << 16 | b << 8 | a, # long int
        'batvol': str((256 * f) + e),
        'timestamp':timestamp
        })

    return dict((k,v) for (k,v) in template.iteritems())