#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import sys

#import config
import common

class Reader(object):
    """Odczyt danych z punktow"""
    def __init__(self, debug=False):
        self.settings_cfg = common.settings_cfg
        self.debug = debug
        self.connected = False

        try:
            host = self.settings_cfg['settings']['daemon']['host']
            port = self.settings_cfg['settings']['daemon']['port']
            if self.debug:
                logging.debug('Trying connect to %s:%s' % (host, str(port)))
        except:
            print "Can't read from config."
            sys.exit(3)

        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((host, port))
            if self.debug:
                logging.debug('Connected to %s:%s' % (host, str(port)))
            self.connected = True

        except socket.error:
            logging.warning("Can't connect to %s:%s" % (host, str(port)))
            self.connected = False
            sys.exit(3)

    def is_connected(self):
        return self.connected

    def serialread(self):
        """Czyta z konsoli szeregowej"""
        line = ''
        if self.connected:
            while True:
                c = self.soc.recv(1)
                if c == '\n' or c == '':
                    break
                else:
                    line += c
            return line

    def __del__(self):
        self.soc.close()