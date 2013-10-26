#!/usr/bin/python2
# -*- coding: utf-8 -*-

import simplejson as json

# na podstwie
# https://github.com/foosel/OctoPrint/blob/master/octoprint/settings.py

instance = None

def config(init=False,
            debug=False,
            basedir=None,
            app_configfile=None,
            nodes_configfile=None):

    global instance
    if instance in None:
        if init:
            instance = Config(debug, basedir, app_configfile, nodes_configfile)
        else:
            raise ValueError("Settings not initialized yet")

class Config():

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
            self.settings_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '/static/conf')

        # app
        if app_configfile is not None:
            self._app_configfile = app_configfile
        else:
            self._app_configfile = os.path.join(self.settings_dir, "settings.json")

        # nodes
        if nodes_configfile is not None:
            self._nodes_configfile = nodes_configfile
        else:
            self._nodes_configfile = os.path.join(self.settings_dir, "nodes.json")

        self.load()

    def load(self):
        # app
        if os.path.exists(self._app_configfile) and os.path.isfile(self._app_configfile):
            with open(self._app_configfile, "r") as f:
                self._appconfig = json.load(self._app_configfile)
                if not self._appconfig:
                    self._appconfig = {}

        # nodes
        if os.path.exists(self._nodeconfig) and os.path.isfile(self._nodeconfig):
            with open(self._nodeconfig, "r") as f:
                self._nodeconfig = json.load(self._nodeconfig)
                if not self._nodeconfig:
                    self._nodeconfig = {}

    def save(self):
        pass

    def set(self):
        pass

    def get(self):
        pass
'''
    def getNodeMap(self):
        """Tworzy slownik nodemap"""
        return dict(zip(self.nodemap_cfg['nodemap'].viewkeys(), self.nodemap_cfg['nodemap'].values()))
'''
    def getCurrentSensors(self, name):
        tmp = self.nodes_cfg[name].keys()
        return tmp

    def getCurrentNodes(self):
        return self.nodes_cfg.keys()

    def getScale(self, name):
        """Tworzy slownik sensor : skala"""
        keys = []
        scales = []
        for (k, v) in self.nodes_cfg[name].iteritems():
            if "scale" in v:
                keys.append(k)
                scales.append(v['scale'])
        return dict(zip(keys, scales))
