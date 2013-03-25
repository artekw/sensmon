#!/usr/bin/python2
# -*- coding: utf-8 -*-

from datetime import datetime
from fabric.api import run, env, put, local, hide
from fabric.colors import green, red

env.hosts = ['artek@192.168.88.245']

def cleanup():
    local('rm -rf *.pyc')
    run('rm -rf /home/artek/code/pycode/senscms2/*')

def backup():
    dt = datetime.now()
    dt = dt.strftime("%H-%M_%d%m%y")
    local('tar -zcvf ./backup/senscms2_'+ dt +'.tar.gz --exclude=backup .')

def copy():
    run('mkdir -p /home/artek/code/pycode/senscms2')
    put('.', '/home/artek/code/pycode/senscms2/')

def run_redis():
    pass


def deploy():
    with hide('running', 'stdout', 'stderr'):
        print(green('############'))
        print(green('## DEPLOY ##'))
        print(green('############'))
        print(red("cleanup..."))
        cleanup()
        print(green("backup..."))
        backup()
        print(green("copy..."))
        copy()