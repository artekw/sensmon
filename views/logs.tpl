{% extends "base.tpl" %}
{% block title %}Logs{% end %}
{% block content %}
    <h1>Logs</h1>
    <h3>Wiadomości z czujnków:</h3>
    <div ng-controller="infoCtrl">
        <div class="row" ng-repeat="i in msg" ng-class-odd="'odd'" ng-class-even="'even'">
            <div class="fifth" >{{! i['name'] }} -></div>
            <div class="fifth" >{{! i['timestamp']*1000|date:'dd/MM/yyyy @ H:mm:ss' }}</div>
            <div class="threefifth">{{! i|onlysensors }}</div>
    </div>
{% end %}
{% block scripts %}
{% end %}