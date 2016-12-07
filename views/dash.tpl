{% extends "base.tpl" %}
{% block title %}Zdarzenia{% end %}
{% block content %}
    <h1 class="page-header">Czujniki</h1>
    <div ng-controller="dashCtrl">
    <!-- Wiersz -->
    <div class="row">
      <div ng-repeat="(k,v) in array">
        <div class="clearfix" ng-if="$index % 3 == 0"></div>
      <div class="col-sm-4" >
        <div class="panel panel-primary">
          <div class="panel-heading"><i class="fa fa-tachometer" aria-hidden="true"></i> {{! v.title}}</div>
            <div class="panel-body">
            <!-- Table -->
              <table class="table">
              <th ng-repeat="(i,j) in v.sensors|nodate"><h5><a href="/graphs/{{! k}}/{{! i}}/day" title="Wykres">{{! j.desc}}</a></h5></th>
                <tr>
                <td ng-repeat="(i,j) in v.sensors|nodate"
                    ng-class="{danger: i=='batvol' && j.raw<3.5 || i=='temp' && j.raw<-10, warning: i=='temp' && j.raw<0 || i=='power' && j.raw>1000 || i=='temp' && j.raw<20, success: i=='temp' && j.raw>23}">
                    <h4 animate-on-change='j.raw'>{{! j.raw }} {{! j.unit}}</h4>
                </td>
                </tr>
            </table>
            <!-- Table -->
            </div>
          <div class="panel-footer panel-primary"><i class="fa fa-refresh"></i> <b>{{! v.sensors.timestamp.raw|parsedate }}</b></div>
        </div>
      </div>
    </div>
    </div>
    </div>
{% end %}
