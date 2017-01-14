{% extends "base.tpl" %}
{% block title %}Intro{% end %}

{% block content %}
  <div class="intro" ng-controller="introCtrl">
    <div class="row">
          <div class="clock">{{! clock | date:'HH:mm:ss'}}</div>
          <div class="date">Dziś jest {{! today(clock) }}</div>
        </div>

    <div class="row">
      <div class="col-sm-6">
      <div class="panel panel-info">
        <div class="panel-heading"><i class="fa fa-clock-o" aria-hidden="true"></i> Zdarzenia</div>
        <div class="panel-body">
          <div class="alert alert-warning" role="alert"><span class="badge">19:25</span> Temperatura w Pokój Artura spadła</div>
          <div class="alert alert-success" role="alert"><span class="badge">19:20</span> Cisnienie w Lab podniosło się</div>
        </div>
      </div>
      </div>
      <div class="col-sm-6">
        <div class="panel panel-danger">
          <div class="panel-heading"><i class="fa fa-exclamation-triangle" aria-hidden="true"></i> Alarmy</div>
          <div class="panel-body">
          <div class="alert alert-danger" role="alert"><span class="badge">19:25</span> Temperatura w <b>Pokój Kamila</b> przekroczyła maksymalną wartość!</div>
          <div class="alert alert-danger" role="alert"><span class="badge">19:20</span> Temperatura w <b>Na zewnątrz</b> przekroczyła minimalną wartość!</div>
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
