#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

appid = '19355ee6d1cab3099dfb45e308ce7e8b'
url = 'http://api.openweathermap.org/data/2.5/forecast/daily?q='


def getWeather(city, units='metric', lang='pl',
               appid=appid):
    """
    :params city srt: city name
    """
    jsonWeather = requests.get(url + city + '&units=' + units + '&lang=' + lang + '&appid=' + appid + '&cnt=6&mode=json')
    return jsonWeather.json()
