{% extends "base.tpl" %}
{% block title %}Info{% end %}
{% block content %}
    <h1>Info</h1>
    <p>Informacje o platformie:<p>
    <ul>
        <li><b>System:</b> {{ system }}</li>
        <li><b>Architektura:</b> {{ arch }}</li>
        {% if system == 'Linux' %}
            <li><b>Obciążenie:</b> {{ lavg }}</li>
            <li><b>Czas pracy:</b> {{ uptime }}</li>
            <li><b>Temperatura CPU:</b> {{ cpu_temp }} *C</li>
            <li><b>Dysk:</b></li>
                <pre>{{ disksize }}</pre>
            <li><b>Procesy:</b></li>
                <pre>{{ process }}
        {% end %}
    </ul>
{% end %}
