#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def pirnode(data, name):
    """Czujka ruchu"""

    a = int(data[2])
    b = int(data[3])
    c = int(data[4])
    d = int(data[5])

    #nodeid = str(data[1])
    timestamp  = int(time.time())

    template = ({
        'light': a,
        'motion': b & 1,
        'humi': b >> 1,
        'temp': str(((256 * (d&3) + c) ^ 512) - 512),
        'lowbat': (d >> 2) & 1,
    })

    return dict((k,v) for (k,v) in template.iteritems())