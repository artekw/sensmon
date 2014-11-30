#!/usr/bin/python2
# -*- coding: utf-8 -*-

import imp
import os
import logging

APPNAME = 'sensmon'

instance = None


def plugins(init=False, basedir=None):
    global instance
    if instance is None:
        if init:
            instance = Plugins(basedir)
        else:
            raise ValueError("Plugins module not initialized correctly.")
    return instance


class Plugins(object):
    def __init__(self, basedir=None):
        self._logger = logging.getLogger(__name__)
        self.plugins_dir = None

        if basedir is not None:
            self.plugins_dir = basedir
        else:
            # FIXME = docelowo plugins
            # FIXME = coś to nie działa ??!!??
            appdir = os.path.expanduser(os.path.join('~', APPNAME.lower()))
            self.plugins_dir = os.path.join(appdir, 'sensnode/decoders')

        self._find_plugins()
        self._load_plugins()


    def _find_plugins(self):
        self.plugins_names = []

        for fn in os.listdir(self.plugins_dir):
            plugin_name, ext = os.path.splitext(fn)
            if ext == ".py" and plugin_name != "__init__":
                self.plugins_names.append(plugin_name)

            self._logger.info("%s plugins was found" % len(self.plugins_names))


    def _load_plugins(self):
        self.plugins = {}

        fp, filenamep, descriptionp = imp.find_module('sensnode/decoders')
        for p in self.plugins_names:
            f, filename, description = imp.find_module(p, [filenamep])
            self.plugins[p] = imp.load_module(p, f, filename, description)

        self._logger.info("%s plugins was loaded" % len(self.plugins))
        print ("%s plugins was loaded" % len(self.plugins))


    def plugin(self, plugin):
        return getattr(self.plugins[plugin], plugin)
