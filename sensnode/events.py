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
                    sensor_data = tclone[key].output.sensors[sensor]
                    if self.debug:
                        print "MAX \n%s" % tclone[key].output.sensors[sensor]
                    if sensor_data.raw >= sensor_data.max:
                        # copy timestamp and push to jsontree obj
                        sensor_data.timestamp = tclone[key].output.sensors.timestamp.raw
                        print "Warning, %s maximum reached!" % key
                        # set key in base
                        # eg. max_powernode <data>
                        self.store.set_key_timeout("max" + "_" + key,
                                                   jsontree.dumps(sensor_data),
                                                   60)
                # check for 'min' key
                if tclone[key].output.sensors[sensor].has_key('min'):
                    sensor_data = tclone[key].output.sensors[sensor]
                    if self.debug:
                        print "MIN \n%s" % tclone[key].output.sensors[sensor]
                    if sensor_data.raw <= sensor_data.min:
                        # copy timestamp and push to jsontree obj
                        sensor_data.timestamp = tclone[key].output.sensors.timestamp.raw
                        print "Warning, %s minimum reached!" % key
                        # set key in base
                        # eg. min_powernode <data>
                        self.store.set_key_timeout("min" + "_" + key,
                                                   jsontree.dumps(sensor_data),
                                                   60)

