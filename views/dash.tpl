{% extends "base.tpl" %}
{% block title %}Dash{% end %}
{% block content %}
    <h1 class="page-header">Czujniki <small>Odczyty z czujników</small></h1>
    <div class="table-responsive" ng-controller="dashCtrl">
        <dynamic-table></dynamic-table>
        <h5>Aktualizacja: {{! lastupd|date:'dd/MM/yyyy, H:mm:ss' }} @ {{! updfrom }}</h5>
    </div>
{% end %}
