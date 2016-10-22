{% extends "base.tpl" %}
{% block title %}Intro{% end %}

{% block content %}
  <div class="intro" ng-controller="introCtrl">
    <div class="row">
      <div class="clock">{{! clock | date:'HH:mm:ss'}}</div>
      <div class="date">Dziś jest {{! today(clock) }}</div>
  </div>
  <div class="row" style="text-align:center;">
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading ">Temperatura</div>
      <div class="panel-body">
        <h1 class="text-primary">{% raw round((w['list'][0]['temp']['max'] + w['list'][0]['temp']['min'])/2, 1) %}°C</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Ciśnienie</div>
      <div class="panel-body">
        <h1 class="text-primary">{% raw w['list'][0]['pressure']%}  hPa</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Wilgotość</div>
      <div class="panel-body">
        <h1 class="text-primary">{% raw w['list'][0]['humidity']%}%</h1>
      </div>
    </div>
  </div>
  </div>
  <div class="row">
  <div class="weather">
    {% for list in w['list'][1:5] %}
    <div class="col-sm-3">
      <div class="panel panel-success">
        <div class="panel-heading">{{! {% raw list['dt'] %}|dayOfweekPL|capitalize}}</div>
          <div class="panel-body">
            {% for weather in list['weather'] %}
              <i class="owf owf-{% raw weather['id'] %} owf-5x"></i>
              <p style="text-transform: capitalize;">{% raw weather['description'] %}</p>
      {% end %}
      {% raw list['temp']['min']%}°C / {% raw list['temp']['max']%}°C
      </div>
    </div>
    </div>
    {% end %}
</div>
</div>
</div>
{% end %}
