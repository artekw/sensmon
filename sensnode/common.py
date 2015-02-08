#!/usr/bin/python2
# -*- coding: utf-8 -*-

__author__ = 'Artur Wronowski'
__version__ = '0.4-dev'
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
from config import config
# from qrcode import *

'''
logging.basicConfig(
    format='%(asctime)-25s %(threadName)-15s %(levelname)-10s %(message)s',
    level=logging.DEBUG,
    datefmt='%d/%m/%Y %H:%M:%S')
'''

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


def machine_detect():
	if os.path.exists('/sys/class/hwmon/hwmon0/device/temp1_input'):
		machine = "Beaglebone Black"
		temp_path = "/sys/class/hwmon/hwmon0/device/temp1_input"
		scale = 1000
	elif os.path.exists('/sys/class/thermal/thermal_zone0/temp'):
		machine = "Raspberry Pi"
		temp_path = "/sys/class/thermal/thermal_zone0/temp"
		scale = 1000
	else:
		machine = "Unknown"
		temp_path = None
		scale = None
	return [machine, temp_path, scale]
	

def cpu_temp():
	machine_info = machine_detect()
	with open(machine_info[1], 'r') as f:
		if machine_info[1] == None:
			temp = 0
		temp = float(f.readline()) / int(machine_info[2])
	return int(temp)

#


def getDigest(password):
    return hashlib.sha256(password).hexdigest()


def isPassword(password, digest):
    return getDigest(password) == digest

'''
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

for n in config().get("nodes", ['keys']):
    qrcode_gen(n, "http://192.168.88.20/rest")
'''
