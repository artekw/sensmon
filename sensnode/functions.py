#!/usr/bin/python2
# -*- coding: utf-8 -*-

import smtplib

import common
import logging

class Alarms(object):
    def __init__(self, receivers, debug=False):
        self.debug = debug
        self.receivers = []
        self.receivers = receivers

    def onAlarm(self, **kwargs):
        # args: { 'cricital': 10, 'safe': 2, 'now': 1 }
        if kwargs['now'] == kwargs['safe']:
            sendMail(kwargs['now'])
        elif kwargs['now'] => kwargs['cricital']:
            sendMail(kwargs['now'], important=True)

    def sendMail(self, value, important=False):
        sender = 'sensmon@localhost.net'

        message = """From: From Person <from@fromdomain.com>
        To: To Person <to@todomain.com>
        Subject: SMTP e-mail test

        This is a test e-mail message.
        """

        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, self.receivers, message)
            print "Successfully send mail"
        except SMTPException:
            print "Error: unable to send mail"
