{% extends "base.tpl" %}
{% block title %}Dash{% end %}
{% block content %}
    <h1 class="page-header">Czujniki <small>Odczyty z czujników</small></h1>
    <div class="table-responsive" ng-controller="dashCtrl">

        <table class="table">
  			<tbody>
            <tr ng-repeat="(k,v) in array">
            	<td class="inverse"><h4>{{! v.title}}</h4><h5><i class="fa fa-refresh"></i> {{! v.sensors.timestamp.raw|parsedate }}</h5></td>
            	<td ng-repeat="(i,j) in v.sensors|nodate" ng-class="{danger: i=='batvol' && j.raw<3.5, warning: i=='temp' && j.raw<0 || i=='power' && j.raw>1000}"><h5>{{! j.desc}}</h5><h4 animate-on-change='j.raw'> {{! j.raw }} {{! j.unit}}</h4></td>
            	<td><h6></i><a href="#"><i class="fa fa-bar-chart"></a></h6><h6></i><a href="#"><i class="fa fa-wrench"></a></h6><h6></i><a href="#"><i class="fa fa-bolt"></a></h6></td>
            </tr>
		</table>
    </div>
{% end %}
