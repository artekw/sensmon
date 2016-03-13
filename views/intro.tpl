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
      <div class="panel-heading ">Jakość powietrza</div>
      <div class="panel-body">
        <h1 class="text-primary">{% raw aqi['title'] %}</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Ciśnienie</div>
      <div class="panel-body">
        <h1 class="text-primary">None</h1>
      </div>
    </div>
  </div>
  <div class="col-sm-4">
    <div class="panel panel-primary">
      <div class="panel-heading">Wilgotość</div>
      <div class="panel-body">
        <h1 class="text-primary">None</h1>
      </div>
    </div>
  </div>
  </div>
  <div class="row">
  <div class="weather">
    {% for list in w['list'] %}
    <div class="col-sm-2">
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
