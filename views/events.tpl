{% extends "base.tpl" %}
{% block title %}Zdarzenia{% end %}
{% block content %}
    <h1 class="page-header">Czujniki <small>Odczyty z czujników</small></h1>
    <div ng-controller="dashCtrl">
    <!-- Wiersz -->
    <div class="row">
      <div ng-repeat="(k,v) in array">
      <div class="col-sm-4">
        <div class="panel panel-primary">
          <div class="panel-heading">{{! v.title}}</div>
            <div class="panel-body">
            <!-- Table -->
              <table class="table">
              <th ng-repeat="(i,j) in v.sensors|nodate"><h5>{{! j.desc}}</h5></th>
                <tr>
                <td ng-repeat="(i,j) in v.sensors|nodate" ng-mouseover="hoverIn()" ng-mouseleave="hoverOut()"
                    ng-class="{danger: i=='batvol' && j.raw<3.5 || i=='temp' && j.raw<-10, warning: i=='temp' && j.raw<0 || i=='power' && j.raw>1000 || i=='temp' && j.raw<20, success: i=='temp' && j.raw>23}">
                    <h4 animate-on-change='j.raw'>{{! j.raw }} {{! j.unit}}</h4>
                    <div class="menu">
                      <span ng-show="hoverEdit">
                        <a href="/graphs/{{! k}}/{{! i}}/day"><i class="fa fa-bar-chart"></i></a>
                      </span>
                    </div>
                </td>
                </tr>
            </table>
            <!-- Table -->
            </div>
          <div class="panel-footer panel-primary">{{! v.sensors.timestamp.raw|parsedate }}</div>
        </div>
      </div>
    </div>
    </div>
    </div>
{% end %}
