{% extends "base.tpl" %}
{% block title %}Intro{% end %}

{% block content %}

  <div class="intro" ng-controller="introCtrl">
    <div class="row">
          <div class="clock">{{! clock | date:'HH:mm:ss'}}</div>
          <div class="date">Today is {{! today(clock) }}</div>
        </div>

    <div class="row">
      <div class="col-sm-6">
      <div class="panel panel-info">
        <div class="panel-heading"><i class="fa fa-clock-o" aria-hidden="true"></i> Zdarzenia</div>
        <div class="panel-body">
          <div class="alert alert-warning" role="alert">Brak</div>
        </div>
      </div>
      </div>
      <div class="col-sm-6">
        <div class="panel panel-danger">
          <div class="panel-heading"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Alarmy</div>
          <div class="panel-body">
          {% if alarm != 'null' %}
            {% if 'max' in alarm %}
                <div class="alert alert-danger" role="alert">{{alarm['desc'] }} w <b>{{alarm['name'] }}</b> przekroczyła {{alarm['max'] }}{{alarm['unit'] }}!</div>
            {% end %}
            {% if 'min' in alarm %}
                <div class="alert alert-success" role="alert">{{alarm['desc'] }} w <b>{{alarm['name'] }}</b> spadła {{alarm['min'] }}{{alarm['unit'] }}!</div>
            {% end %}
          {% else %}
            <div class="alert alert-info" role="alert">Brak</div>
          {% end %}
          </div>
        </div>
      </div>
    </div>

    <div class="panel panel-default">
      <div class="panel-heading"><i class="fa fa-newspaper-o" aria-hidden="true"></i> Wiadomości</div>
      <div class="panel-body">
        {% for news in f %}
          <h5>{% raw news %}</h5>
          {% end %}
      </div>
    </div>
  </div>
{% end %}
