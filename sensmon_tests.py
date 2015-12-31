#!/usr/bin/python2
# -*- coding: utf-8 -*-

# sesnode engine
import sensnode.store
import sensnode.decoder
import sensnode.connect
import sensnode.common
import sensnode.logs as logs
from sensnode.config import config


# inicjalizacja menadżera konfiguracji
ci = config(init=True)

history = sensnode.store.history(config().get("app", ['leveldb', 'path']),
                                config().get("app", ['leveldb', 'dbname']))


print history.select('artekroom', 'temp', 'day')