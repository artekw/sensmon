#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import sys
import common
import multiprocessing
import logging
import simplejson as json


class Connect(multiprocessing.Process):

    """Odczyt danych z punktow"""
    def __init__(self, taskQ, resultQ, debug=False):
        self._logger = logging.getLogger(__name__)
        multiprocessing.Process.__init__(self)
        self.settings_cfg = common.settings_cfg
        self.taskQ = taskQ
        self.resultQ = resultQ
        self.debug = debug
        self.connected = False

        try:
            host = self.settings_cfg['settings']['remserial']['host']
            port = self.settings_cfg['settings']['remserial']['port']

            if self.debug:
                self._logger.debug('Trying connect to %s:%s' % (host, str(port)))
        except:
            print "Can't read from config."
            sys.exit(3)

        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((host, port))
            self.connected = True

            if self.debug:
                self._logger.debug('Connected to %s:%s' % (host, str(port)))

        except socket.error:
            self.connected = False

            self._logger.warning("Can't connect to %s:%s" % (host, str(port)))
            sys.exit(3)

    def is_connected(self):
        return self.connected

    def close(self):
        self.soc.close()

    def parseInput(self, line):
        msg = json.loads(line)
        node = msg['name']
        node = node.split('rn')[1]
        if int(node) < 9:
            node = "0%s" % (node)

        cmd = msg['cmd']
        state = msg['state']

        output = "%s%s%s" % (node, cmd, state)
        return output

    def run(self):
        line = ''
        if self.connected:
            while True:
                # wysyłanie
                if not self.taskQ.empty():
                    task = self.parseInput(self.taskQ.get())
                    self.soc.sendall(task)
                    if self.debug:
                        self._logger.info("Put task in queue: %s" % task)
                # odbiór
                self.resultQ.put(self.serialread())
            if self.debug:
                self._logger.info("Put result in queue: %s" % line)
        else:
            print "not connected!"

    def serialread(self):
        """Czyta z konsoli szeregowej"""
        line = ''
        while True:
            c = self.soc.recv(1)
            if c == '\n' or c == '':
                break
            else:
                line += c
        return line
