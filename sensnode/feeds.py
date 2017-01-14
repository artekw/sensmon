#!/usr/bin/python2
# -*- coding: utf-8 -*-

import feedparser

feeds = ['http://s.stooq.pl/rss/pl/mol.rss', 
        'http://rss.dziennik.pl/Dziennik-PL/',
        'http://www.tvn24.pl/najnowsze.xml',
        'http://wiadomosci.wp.pl/ver,rss,rss.xml']


def getFeeds():
    """Parse selected RSS and Atom feeds"""
    news = []
    for feed in feeds:
        data = feedparser.parse(feed)
        for n in range(2):
            news.append("<span class='label label-info'>%s</span> <a href=%s target='_BLANK'>%s</a>" % (data.feed.title, data.entries[n].link, data.entries[n].title))
    return news