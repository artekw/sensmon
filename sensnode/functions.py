#!/usr/bin/python2
# -*- coding: utf-8 -*-

# import smtplib

import common
import logging
import config

class alarms(object):
    def __init__(self, debug=False):
        self.settings_cfg = common.settings_cfg
        self.nodes_cfg = common.nodes_cfg
        self.debug = debug
        pass

    def onAlarm():
        pass

    def sendMail():
        pass