#!/usr/bin/python2
# -*- coding: utf-8 -*-

# http://throwingfire.com/storing-passwords-securely/

__author__ = 'Artur Wronowski'
__version__ = '0.5-dev'
__appname__ = 'sensnode-core'
__license__ = 'MIT'
__email__ = 'arteqw@gmail.com'

import datetime
import logging
import platform
import os
import subprocess
import simplejson as json
import hashlib
from qrcode import *
from collections import OrderedDict

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

#


def get_version():
        return __version__


def get_author():
        return __author__


def get_license():
        return __license__


def get_email():
        return __email__

#


def this_system():
    return platform.system()


def this_mach():
    return platform.machine()


def loadavg():
    return os.getloadavg()


def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
    return uptime_string


def disksize():
    disk = subprocess.Popen(['df', '-H'], stdout=subprocess.PIPE)
    grep = subprocess.Popen(
        ['grep', 'root'], stdin=disk.stdout, stdout=subprocess.PIPE)
    disk.stdout.close()
    out = grep.communicate()[0]
    return out


def process():
    ps = subprocess.Popen(['ps', 'x1'], stdout=subprocess.PIPE)
    out, err = ps.communicate()
    return out


# only for raspberrypi
def cpu_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = float(f.readline()) / 1000
    return round(temp, 1)

#


def getDigest(password):
    return hashlib.sha256(password).hexdigest()


def isPassword(password, digest):
    return getDigest(password) == digest


def qrcode_gen(node, url, out='static/img/qrcodes', replace=False):
    if not os.path.isdir(out):
        os.makedirs(out)

    if not os.path.isfile('%s/%s.png' % (out, node)):
        qr = QRCode(version=4,
                    error_correction=constants.ERROR_CORRECT_M,
                    box_size=5,
                    border=1,
                            )
        qr.add_data('%s/%s.png' % (url, node))
        qr.make(fit=True)

        img = qr.make_image()
        img.save('%s/%s.png' % (out, node))

for n in nodes_cfg.keys():
    qrcode_gen(n, "http://192.168.88.20/rest")


def dict2list_values(d):
    dict_sorted = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
    del dict_sorted['timestamp']
    del dict_sorted['name']

    return [v for k,v in dict_sorted.items()]

def dict2list_keys(d):
    dict_sorted = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
    del dict_sorted['timestamp']
    del dict_sorted['name']

    return [k for k,v in dict_sorted.items()]