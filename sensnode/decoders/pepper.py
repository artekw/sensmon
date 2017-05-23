#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import inspect

# OK 20 0 0 0 0 0 0 0 0 41 14 227 38

def pepper(data):

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

    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) # czas unixa

    template = ({
        'name':name,
        'batvol':str(int.from_bytes([j,i], byteorder='big')),
        'soil':str(int.from_bytes([l,k], byteorder='big')),
        'timestamp':timestamp
    })

    return template
