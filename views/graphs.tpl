{% extends "base.tpl" %}
{% block title %}Graphs{% end %}

{% block content %}
    <div ng-controller="graphsCtrl">
    <h1 class="page-header">Graphs</h1>
    <div class="row">
      <!--<div class="btn-group" role="group" aria-label="...">
        <button type="button" class="btn btn-default">Godzina</button>
        <button type="button" class="btn btn-default">Dzień</button>
        <button type="button" class="btn btn-default">Miesiąc</button>
      </div>-->
      <highchart id="chart" config="chartConfig" class="span10"></highchart>
    </div>
</div>
{% end %}
