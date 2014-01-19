#!/usr/bin/python2
# -*- coding: utf-8 -*-

import os
import simplejson as json
import logging

# na podstawie
# https://github.com/foosel/OctoPrint/blob/master/octoprint/settings.py

instance = None

APPNAME = 'sensmon'

def config(init=False,
            debug=False,
            basedir=None,
            app_configfile=None,
            nodes_configfile=None):

    global instance
    if instance is None:
        if init:
            instance = Config(debug, basedir, app_configfile, nodes_configfile)
        else:
            raise ValueError("Ustawienia nie zostały właściwie zainicjowane")
    return instance

# TODO - wykorzystać domyślne ustawienia
default_app_config = {
            "webapp": {"host": "0.0.0.0", "port": "8080", "password": "password"},
            "remserial": {"port": 2000, "host": "localhost"},
            "redis": {"host": "localhost"},
            "leveldb": {"dbname" : "sensmon_db", "path": "/tmp/"}
            }

default_nodes_config ={}


class Config(object):

    """Zarzadzanie konfiguracją w json
    Konfigi:
    - programu - settings.json
    - nodów - nodes.json
    """
    def __init__(self,
                debug=False,
                basedir=None,
                app_configfile=None,
                nodes_configfile=None):

        self.debug = debug
        self._logger = logging.getLogger(__name__)

        self._appconfig = None
        self._nodeconfig = None
        self.settings_dir = None

        if basedir is not None:
            self.settings_dir = basedir
        else:
            appdir = os.path.expanduser(os.path.join('~', APPNAME.lower()))
            # TODO - inny katalog na ustawienia
            self.settings_dir = os.path.join(appdir, 'static/conf')

        # app
        if app_configfile is not None:
            self._app_configfile = app_configfile
        else:
            self._app_configfile = os.path.join(self.settings_dir, "settings.json")

        # nodes
        if nodes_configfile is not None:
            self._nodes_configfile = nodes_configfile
        else:
            self._nodes_configfile = os.path.join(self.settings_dir, "nodemap2.json")

        self.load()


    def load(self):
        # app
        if os.path.exists(self._app_configfile) and os.path.isfile(self._app_configfile):
            with open(self._app_configfile, "r") as f:
                self._appconfig = json.load(f)
        if not self._appconfig:
            self._appconfig = {}

        # nodes
        if os.path.exists(self._nodes_configfile) and os.path.isfile(self._nodes_configfile):
            with open(self._nodes_configfile, "r") as f:
                self._nodeconfig = json.load(f)
        if not self._nodeconfig:
            self._nodeconfig = {}

        self._logger.info(" config loaded")


    def save(self):
        """Zapisywanie pliku konfiguracyjnego"""
        pass


    def set(self):
        """Ustawianie opcji dla wybranego paramatru"""
        pass


    def get(self, type, path):
        """
        Pobieranie z ustawień np:.
        get("app",['webapp','host'])
        get("nodes",['artekroom','press', 'unit'])
        """
        if len(path) == 0:
            return None

        if type == "app":
            config = self._appconfig
        elif type == "nodes":
            config = self._nodeconfig
        else:
            return None

        # FIXME
        if path == ['fkeys']:
            return config.keys()

        while len(path) > 1:
            key = path.pop(0)
            if key in config.keys():
                config = config[key]
            else:
                return None

        k = path.pop(0)
        if not isinstance(k, (list, tuple)):
            keys = [k]
        else:
            keys = k

        results = []

        for key in keys:
            if key in config.keys():
                results.append(config[key])
            else:
                results.append(None)

            if not isinstance(k, (list, tuple)):
                return results.pop()
            else:
                return results


    def getScale(self, name):
        """Tworzy slownik sensor : skala"""
        keys = []
        scales = []
        for (k, v) in self.get("nodes", [name,'sensors']).iteritems():
            if "scale" in v:
                keys.append(k)
                scales.append(v['scale'])
        return dict(zip(keys, scales))


    def getMap(self, type=None):
        """Tworzy słownik {id : name} dla wybranego typu sensora (output lub control)"""
        if type == None:
            type = ['output', 'control']
        ids = [self.get("nodes", [k,'id']) for k in self.get("nodes", ['fkeys']) if self.get("nodes", [k,'type']) in type]
        names = [k for k in self.get("nodes", ['fkeys']) if self.get("nodes", [k,'id' ]) in ids]
        return dict(zip(ids, names))