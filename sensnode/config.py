#!/usr/bin/python2
# -*- coding: utf-8 -*-

import simplejson as json
import common

class Config(object):
    """Zarzadzanie konfiguracja w json"""
    def __init__(self, debug=False):
        self.nodes_cfg = common.nodes_cfg
        self.nodemap_cfg = common.nodemap_cfg
        self.settings_cfg = common.settings_cfg
        self.debug = debug

    def getNodeMap(self):
        """Tworzy slownik nodemap"""
        return dict(zip(self.nodemap_cfg['nodemap'].viewkeys(), self.nodemap_cfg['nodemap'].values()))

    def getCurrentSensors(self, name):
        tmp = self.nodes_cfg[name].keys()
        return tmp

    def getCurrentNodes(self):
        return self.nodes_cfg.keys()

    def getScale(self, name):
        """Tworzy slownik sensor : skala

        TODO: pomijanie wprowadzania skali"""
        scales = [self.nodes_cfg[name][str(x)]['scale'] for x in self.getCurrentSensors(name)]
        return dict(zip(self.nodes_cfg[name].viewkeys(), scales))