{% extends "base.tpl" %}
{% block title %}Dash{% end %}
{% block content %}
    <h1 class="page-header">Czujniki <small>Odczyty z czujników</small></h1>
    <div class="table-responsive" ng-controller="dashCtrl">
        <table class="table table-striped">
  			<tbody>
            <tr ng-repeat="(k,v) in array">
            	<td><h5>Nazwa</h5><h4>{{! v.title}}</h4></td>
            	<td ng-repeat="(i,j) in v.sensors"><h5>{{! j.desc}}</h5><h4><span animate-on-change='j.raw'> {{! j.raw|parsedate }} {{! j.unit}}</span></h4></td>
            </tr>
		</table>
    </div>
{% end %}
