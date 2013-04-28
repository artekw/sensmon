{% extends "base.tpl" %}
{% block title %}Logs{% end %}
{% block content %}
    <h1>Logs</h1>
    <p>
        <div class="row">
            <div class="third"><h3>Źródło</h3></div>
            <div class="third"><h3>Czas</h3></div>
            <div class="third"><h3>Odczyt</h3></div>
        </div>
        <div ng-controller="logsCtrl">
            <div class="row" ng-repeat="i in msg" ng-class-odd="'odd'" ng-class-even="'even'">
                <div class="third" >{{! i['name'] }} -></div>
                <div class="third" >{{! i['timestamp']*1000|date:'dd/MM/yyyy @ H:mm:ss' }}</div>
                <div class="third">{{! i|onlysensors }}</div>
            </div>
        </div>
    </p>
{% end %}
{% block scripts %}
{% end %}