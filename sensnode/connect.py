#!/usr/bin/python2
# -*- coding: utf-8 -*-

import socket
import sys
import common
import multiprocessing
import logging
import simplejson as json
from config import config


class Connect(multiprocessing.Process):

    """Czytanie danych z nodów"""
    def __init__(self, taskQ, resultQ, debug=False):
        self._logger = logging.getLogger(__name__)
        multiprocessing.Process.__init__(self)
        self.taskQ = taskQ
        self.resultQ = resultQ
        self.debug = debug
        self.connected = False

        try:
            host = config().get("app", ['serial', 'host'])
            port = config().get("app", ['serial', 'port'])

            if self.debug:
                self._logger.debug('Próba połączenia z %s:%s' % (host, str(port)))
        except:
            self._logger.warning("Problem z odczytem ustawień")
            sys.exit(3)

        try:
            self.soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.soc.connect((host, port))
            self.connected = True

            if self.debug:
                self._logger.debug('Połączono z %s:%s' % (host, str(port)))

        except socket.error:
            self.connected = False

            self._logger.warning("Nie można połączyć z %s:%s" % (host, str(port)))
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
            self._logger.warning("Not connected!")

    def serialread(self):
        """Odczyt z konsoli ser2net"""
        line = ''
        while True:
            c = self.soc.recv(1)
            if c == '\n' or c == '':
                break
            else:
                line += c
        return line
