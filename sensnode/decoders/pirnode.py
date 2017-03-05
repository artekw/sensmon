#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import datetime
import inspect

def pirnode(data):
    """Czujka ruchu"""

    a = int(data[2])
    b = int(data[3])
    c = int(data[4])
    d = int(data[5])

    name = inspect.stack()[0][3] # z nazwy funcji
    timestamp = int(time.mktime(datetime.datetime.now().timetuple())) #unix time

    template = ({
        'name':name,
        'light': a,
        'motion': b & 1,
        'humi': b >> 1,
        'temp': str(((256 * (d&3) + c) ^ 512) - 512),
        'lowbat': (d >> 2) & 1,
        'timestamp':timestamp
    })

    return template
