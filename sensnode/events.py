#!/usr/bin/python2
# -*- coding: utf-8 -*-

from jsondiff import diff
import simplejson as json
import jsontree

class Events(object):
    '''
    Events handler. Check for changes in reported data and report it.
    Monitor whitch data break min and max values.
    '''
    def __init__(self, store, debug=False):
        self.store = store
        self.debug = debug

    def changes(self, data):
        """Return difference beetwen two json object"""
        return diff(data, self.store.get_initv(), load=True)

    def alarm(self, data):
        """Alarm"""
        # convert to Python obj and then clone as jsontree obj
        tclone = jsontree.clone(json.loads(data))

        for key in tclone.keys():
            for sensor in tclone[key].output.sensors.keys():
                # check for 'max' key
                if tclone[key].output.sensors[sensor].has_key('max'):
                    if self.debug:
                        print "MAX \n%s" % tclone[key].output.sensors[sensor]
                    if tclone[key].output.sensors[sensor].raw >= tclone[key].output.sensors[sensor].max:
                        print "Warning, %s maximum reached!" % key
                # check for 'min' key
                if tclone[key].output.sensors[sensor].has_key('min'):
                    if self.debug:
                        print "MIN \n%s" % tclone[key].output.sensors[sensor]
                    if tclone[key].output.sensors[sensor].raw <= tclone[key].output.sensors[sensor].min:
                        print "Warning, %s minimum reached!" % key

