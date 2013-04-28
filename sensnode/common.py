#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'Artur Wronowski'
__version__ = '0.5-dev'
__appname__ = 'sensnode-core'
__license__ = 'MIT'
__email__ = 'arteqw@gmail.com'

import time
import datetime
import calendar
import sys
import logging
import platform
import os
import simplejson as json

debug = False

logging.basicConfig(
        format='%(asctime)-25s %(threadName)-15s %(levelname)-10s %(message)s',
        level=logging.DEBUG,
        datefmt='%d/%m/%Y %H:%M:%S')


with open('static/conf/settings.json') as settings_file:
    settings_cfg = json.load(settings_file)
with open('static/conf/nodes.json') as nodes_file:
    nodes_cfg = json.load(nodes_file)
with open('static/conf/nodemap.json') as nodemap_file:
    nodemap_cfg = json.load(nodemap_file)


#########################################################

def get_version():
        return __version__

def get_author():
        return __author__

def get_license():
        return __license__

def get_email():
        return __email__

########################################################

def this_system():
    return platform.system()

def this_mach():
    return platform.machine()

def loadavg():
    return os.getloadavg()

def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(datetime.timedelta(seconds = uptime_seconds))
    return uptime_string

########################################################