{% extends "base.tpl" %}
{% block title %}Logs{% end %}
{% block content %}
    <h1 class="page-header">Logi <small>Logowanie</small></h1>
        <div class="row">
            <div class="col-md-4"><h4>Źródło</h4></div>
            <div class="col-md-4"><h4>Czas</h4></div>
            <div class="col-md-4"><h4>Odczyt</h4></div>
        </div>
        <div ng-controller="logsCtrl">
            <div class="row" style="margin-bottom:0" ng-repeat="i in msg" ng-class-odd="'odd'" ng-class-even="'even'">
				<div class="col-md-4">{{! i['name'] }} -></div>
                   <div class="col-md-4">{{! i['timestamp']*1000|date:'dd/MM/yyyy @ H:mm:ss' }}</div>
                   <div class="col-md-4">{{! i|onlysensors }}</div>
            </div>
        </div>
{% end %}
{% block scripts %}
{% end %}
