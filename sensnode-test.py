#!/usr/bin/python2
# -*- coding: utf-8 -*-

db_name = '_db'

import sensnode.store

d = sensnode.store.history(".", "_db", False)
#d.get('artekroom', '2h')
d.select('a', 'artekroom','2h')
