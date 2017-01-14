{% extends "base.tpl" %}
{% block title %}Czujniki{% end %}
{% block content %}
    <h1 class="page-header">Czujniki</h1>
    <div class="table-responsive" ng-controller="dashCtrl">
        <div class="table-responsive">
        <table class="table">
  			<tbody>
            <tr ng-repeat="(k,v) in array">
            	<td class="name-node"><h4>{{! v.title}}</h4><h5><i class="fa fa-refresh"></i> {{! v.sensors.timestamp.raw|parsedate }}</h5></td>
            	<td ng-repeat="(i,j) in v.sensors|nodate" ng-mouseover="hoverIn()" ng-mouseleave="hoverOut()"
                    ng-class="{danger: i=='batvol' && j.raw<3.5 || i=='temp' && j.raw<-10, warning: i=='temp' && j.raw<0 || i=='power' && j.raw>1000 || i=='temp' && j.raw<20, success: i=='temp' && j.raw>23}">
                    <div class="info"><h5><a href="/graphs/{{! k}}/{{! i}}/day" title="Wykres">{{! j.desc}}</a></h5><h4 animate-on-change='j.raw'>{{! j.raw }} {{! j.unit}}</h4></div>
                    <div class="menu">
                    <!--<span ng-show="hoverEdit">
                    <a href="/graphs/{{! k}}/{{! i}}/day"><i class="fa fa-bar-chart"></i></a>
                    <a href="/{{! k}}/{{! i}}/setup"><i class="fa fa-wrench"></i></a>
                    <a href="/{{! k}}/{{! i}}/action"><i class="fa fa-bolt"></i></a>
                </span>-->
                </div>
                </td>
            </tr>
		</table>
        </div>
        </div>
{% end %}
