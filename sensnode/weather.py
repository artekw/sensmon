#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q='


def getWeather(city, appid, units='metric', lang='us'):
    """
    :params city srt: city name
    """
    jsonWeather = requests.get(url + city + '&units=' + units + '&lang=' + lang + '&appid=' + appid + '&cnt=6&mode=json')
    return jsonWeather.json()
