{% extends "base.tpl" %}
{% block title %}Przełączniki{% end %}

{% block content %}
    <div ng-controller="relayCtrl">
    <h1 class="page-header">Przełączniki</h1>
      <div class="row">
        <div ng-repeat="(k,v) in array">
          <div class="clearfix" ng-if="$index % 3 == 0"></div>
          <div class="col-sm-4">
            <div class="panel panel-default">
              <div class="panel-heading"><b>{{! v.title}}</b></div>
              <div class="panel-body">
                <span>
                  <!-- switches -->
                  <!-- http://ziscloud.github.io/angular-bootstrap-toggle/ -->
                  <span ng-repeat="(i,j) in v.input.relay">
                    <div class="half">{{! j.desc }}</div>
                      <div class="half">
                        <span ng-init="j.cmd= j.state" class="btn-group" data-toggle="buttons">
                          <button class="btn" buttons-radio="" ng-model="j.cmd" ng-change='change(j.cmd, name=i, cmd=j.cmd)' value="1">Wł</button>
                          <button class="btn" buttons-radio="" ng-model="j.cmd" ng-change='change(j.cmd, name=i, cmd=j.cmd)' value="0">Wył</button>
                        </span>
                      </div>
                  </span>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
{% end %}
