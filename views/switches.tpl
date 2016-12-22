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
                  <span ng-repeat="(i,j) in v.input.relay">
                    <div>{{! j.desc }}</div>
                    <div toggle-switch class="switch-primary"
                                        ng-init="state=j.state"
                                        ng-model="state"
                                        on-label="Wł."
                                        off-label="Wył."
                                        ng-change='changeState(state, i)'>
                                      </div>
                    <br>
                  </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
{% end %}
