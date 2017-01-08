{% extends "base.tpl" %}
{% block title %}Przełączniki{% end %}

{% block content %}
    <div ng-controller="relayCtrl">
    <h1 class="page-header">Przełączniki</h1>
      <div class="row">
        <div ng-repeat="(k,v) in array">
          <div class="clearfix" ng-if="$index % 2 == 0"></div>
          <div class="col-sm-3">
            <div class="panel panel-primary">
              <div class="panel-heading"><b>{{! v.title}}</b></div>
              <div class="panel-body">
                  <span ng-repeat="(i,j) in v.input.relay">
                    <div form class="form-inline">
                      <label><h5><b>{{! j.desc }}</b></h5></label>
                      <div class="pull-right">
                          <toggle-switch class="switch-primary"
                                        ng-init="state=j.state"
                                        ng-model="state"
                                        on-label="Wł."
                                        off-label="Wył."
                                        ng-change='changeState(state, i, j.cmd, v.node_name, v.id)'>
                          </toggle-switch>
                      </div>
                    </div>
                  </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
{% end %}
