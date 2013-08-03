{% extends "base.tpl" %}
{% block title %}Logs{% end %}
{% block content %}
    <h1>Logs</h1>
        <div class="units-row">
            <div class="unit-20"><h3>Źródło</h3></div>
            <div class="unit-30"><h3>Czas</h3></div>
            <div class="unit-50"><h3>Odczyt</h3></div>
        </div>
        <div ng-controller="logsCtrl">
            <div class="units-row" style="margin-bottom:0" ng-repeat="i in msg" ng-class-odd="'odd'" ng-class-even="'even'">
                    <div class="unit-20" >{{! i['name'] }} -></div>
                    <div class="unit-30" >{{! i['timestamp']*1000|date:'dd/MM/yyyy @ H:mm:ss' }}</div>
                    <div class="unit-50">{{! i|onlysensors }}</div>

            </div>
        </div>
{% end %}
{% block scripts %}
{% end %}