{% extends "base.tpl" %}
{% block title %}Home{% end %}
{% block content %}
    <h1>Home</h1>
    <p>Witamy w projekcie sensmon!<p>
    <ul>
        <li><a href="/dash">dash</a> - odczyty przedstawione w tabeli w stylu Metro</li>
        <li><a href="/graphs">graphs</a> - odczyty przedstawione w postaci wykresu (WiP)</li>
        <li><a href="/control">control</a> - kontrola przekaźników</li>
        <li><a href="/logs">logs</a> - aktualne odczyty w postaci prostej tabeli</li>
        <li><a href="/info">info</a> - informacje o systemie</li>
    </ul>
{% end %}
