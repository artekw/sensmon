#!/usr/bin/python2
# -*- coding: utf-8 -*-

import datetime
import logging
import platform
import os
import subprocess
import socket
import fcntl
import struct
import simplejson as json
import hashlib
#from config import config
import logs


def this_system():
    return "%s %s" % (platform.linux_distribution()[0].capitalize(), platform.linux_distribution()[1])


def this_mach():
    return platform.machine()


def loadavg():
    return os.getloadavg()


def uptime():
    with open('/proc/uptime', 'r') as f:
        uptime_seconds = float(f.readline().split()[0])
        uptime_string = str(datetime.timedelta(seconds=uptime_seconds))
    return uptime_string


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


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
		temp_path = ""
		scale = 0
	return [machine, temp_path, scale]


def cpu_temp():
    machine_info = machine_detect()
    if machine_info[0] == "Unknown":
        return 0
    with open(machine_info[1], 'r') as f:
        temp = float(f.readline()) / int(machine_info[2])
    return int(temp)


def getDigest(password):
    return hashlib.sha256(password).hexdigest()


def isPassword(password, digest):
    return getDigest(password) == digest
