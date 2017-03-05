#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import inspect

def kamilroom(data):
    """kamilroom"""

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
    m = int(data[14])

    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) #unix time

    template = ({
        'name':name,
        'temp': str(((256 * (f&3) + e) ^ 512) - 512),
        'press': str((256 * h) + g),
        'batvol':str((256 * k) + j),
        'air':str((256 * m) + l),
        'timestamp':timestamp
    })

    return template
