#!/usr/bin/python2
# -*- coding: utf-8 -*-

import time
import simplejson as json

def pirnode(data, name):
    """Czujka ruchu"""

    a = int(data[2])

    #nodeid = str(data[1])
    timestamp  = int(time.time())

    template = ({
        'name':name,
        'motion': a & 1,
        'lowbat': (b >> 2) & 1,
        'timestamp':timestamp
    })

    return dict((k,v) for (k,v) in template.iteritems())