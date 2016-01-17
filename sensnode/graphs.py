#!/usr/bin/python2
# -*- coding: utf-8 -*-

import store
import logging
import logs
import jsontree
from datetime import datetime
from config import config
import numpy as np
from bokeh.plotting import *
from bokeh.embed import components

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
        "height": 400
        }


class Graphs(object):
    """Generate graph image for selected nodes"""
    def __init__(self, history, debug=False):
        self._logger = logging.getLogger(__name__)
        self.debug = False
        self.history = history
        self.nodescfg = jsontree.clone(config().getConfig('nodes'))


    def generate_graph(self, nodename, sensor, timerange='1h'):
        """Generate graphs for selected node, sensor and time range"""

        _data = self.history.select(nodename, sensor, timerange)
        _title = self.nodescfg[nodename].title
        _desc = self.nodescfg[nodename].sensors[sensor].desc

        graph_data = ColumnDataSource(
            data=dict(
                sensor_timstamps=[datetime.fromtimestamp(int(d[0])) for d in _data],
                sensor_data=[d[1] for d in _data],
                )
        )

        graph = figure(width=default_graph_config['width'],
                        height=default_graph_config['height'],
                        x_axis_type = "datetime",
                        title=_title,
                        tools="",
                        toolbar_location=None
        )
        graph.xaxis.axis_label = "Czas"
        graph.yaxis.axis_label = _desc
        graph.ygrid.minor_grid_line_color = 'navy'
        graph.ygrid.minor_grid_line_alpha = 0.1
        graph.background_fill_color = "#eee"
        graph.background_fill_alpha = 0.5

        graph.line("sensor_timstamps", "sensor_data",
                        source=graph_data,
                        color='red',
                        alpha=0.5,
                        line_width=2.5
        )

        script, div = components(graph)
        return (script, div)
