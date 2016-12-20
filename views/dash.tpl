{% extends "base.tpl" %}
{% block title %}Czujniki{% end %}
{% block content %}
    <h1 class="page-header">Czujniki</h1>
    <div ng-controller="dashCtrl">
    <!-- Row -->
    <div class="row">
      <div ng-repeat="(k,v) in array">
        <div class="clearfix" ng-if="$index % 3 == 0"></div>
      <div class="col-sm-4">
        <div class="panel panel-primary">
          <div class="panel-heading"><b>{{! v.title}}</b>
            <!-- battery levels -->
            <span class="pull-right">
            <i ng-class="{'fa fa-plug': v.output.sensors.batvol.raw<=6.0 || v.output.sensors.batvol.raw<=5.0,
                          'fa fa-battery-full': v.output.sensors.batvol.raw<=4.5 || v.output.sensors.batvol.raw<=3.9,
                          'fa fa-battery-half': v.output.sensors.batvol.raw<=3.8 || v.output.sensors.batvol.raw<=3.7,
                          'fa fa-battery-quater': v.output.sensors.batvol.raw<=3.6 || v.output.sensors.batvol.raw<=3.5 ,
                          'fa fa-battery-empty': v.output.sensors.batvol.raw<=3.4 || v.output.sensors.batvol.raw<=3.3}"
                          title="{{! v.output.sensors.batvol.raw }}">
            </i>
            </span>
            <!-- end battery levels -->
          </div>
            <div class="panel-body">
            <!-- Table -->
              <table class="table">
              <th ng-repeat="(i,j) in v.output.sensors|nodate|nobatvol"><h5><a href="/graphs/{{! k}}/{{! i}}/week" target="_self" title="Wykres">{{! j.desc}}</a></h5></th>
                <tr>
                  <!-- cels -->
                <td ng-repeat="(i,j) in v.output.sensors|nodate|nobatvol"
                    ng-class="{danger: i=='temp' && j.raw<-10,
                              warning: i=='temp' && j.raw<0 || i=='power' && j.raw>1000 || i=='temp' && j.raw<20,
                              success: i=='temp' && j.raw>23}">
                    <h4 animate-on-change='j.raw'>{{! j.raw }} {{! j.unit}}</h4>
                </td>
                <!-- end cels -->
                </tr>
            </table>
            <!-- End Table -->
            </div>
          <div class="panel-footer panel-primary">
            <i class="fa fa-refresh fa-spin fa fa-fw"></i> <b>{{! v.output.sensors.timestamp.raw|parsedate }}</b>
          </div>
        </div>
      </div>
    </div>
    </div>
    </div>
{% end %}
