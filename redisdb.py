#!/usr/bin/python2
# -*- coding: utf-8 -*-

import sensnode.store
st = sensnode.store.Store()

while True:
    st.pubsub('nodes');

