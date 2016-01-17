#!/usr/bin/python2
# -*- coding: utf-8 -*-

import store
import logging
import logs
import numpy as np
from bokeh.plotting import *

"""
__TODO__:
- generowanie obrazu png HQ lub kodu HTML+JS
- Schemat nazwy generowanego obrazu:
    * odzielnie na kazdy sensor
        _node_-_sensor_-_period_.png
        np:.
            outnode-temp-day.png
            artekroom-humi-week.png
    * lub grupowo na node:
        _node_-_period_.png
            np:.
            outnode-day.png
            salon-week.png
- cyliczne generowanie statystyk(wykresów) w tle:
    * roczne(year) raz na tydzień
    * miesięczne(mounth) co 24h
    * tygodniowe(week) co 12h
    * dzienne(day) na bieżąco z przeglądarki
    * godzinne(1h) na bieżąco z przeglądarki
- przechowywanie plików w 'static/img/graphs'
- dodanie ignora do githuba dla katalogu z wykresami
- dodać timestamp do generowanego obrazu
- do generowania można wykorzytać 'https://github.com/rholder/retrying'
"""

default_graph_config = {
        "width": 800,
        "height": 400,
        "x_axis_type" = "datetime",
        "grid_line_color" = "navy"
        }


class Graphs(object):
    """Generate graph image for selected nodes"""
    def __init__(self, debug=False):
        self._logger = logging.getLogger(__name__)
        self.debug = False


        def generate_graph(self, node):
            pass
