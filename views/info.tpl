{% extends "base.tpl" %}
{% block title %}Info{% end %}
{% block content %}
    <h1>Info</h1>
    <p>Informacje o platformie:<p>
    <ul>
        <li>System: {{ system }}</li>
        <li>Architektura: {{ arch }}</li>
        {% if system == 'Linux' %}
            <li>Obciążenie: {{ lavg }}</li>
        {% end %}
    </ul>
    <br />
    <h1>Powered by:</h1>
    <ul>
        <li><a href="http://www.tornadoweb.org" title="tornadoweb"><img src="static/img/tornado.png"/></a></li>
        <li><a href="http://angularjs.org/" title="angularjs"><img src="static/img/AngularJS-large.png"/></a></li>
    </ul>
{% end %}
