{% extends "base.tpl" %}
{% block title %}Control{% end %}
{% block content %}
    <h1 class="page-header">Sterowanie <small>Sterowanie przekaźnikami</small></h1>

    <div class="control" ng-controller="controlCtrl">
        <div class="container"><!-- poczatek wiersza-->
            <div class="third">
                <fieldset>
                    <legend>relayNode01</legend>
                    <div ng-repeat="switch in switches">
                    <div class ="containter row">
                        <div class="half">Przekaźnik {{! switch.cmd }}</div>
                        <div class="half">
                            <span ng-init="switch.name_switch.cmd= switch.state" class="btn-group" data-toggle="buttons">
                                <button class="btn" buttons-radio="" ng-model="switch.name_switch.cmd" ng-change='change(switch.name_switch.cmd, name=switch.name, cmd=switch.cmd)' value="1">Wł</button>
                                <button class="btn" buttons-radio="" ng-model="switch.name_switch.cmd" ng-change='change(switch.name_switch.cmd, name=switch.name, cmd=switch.cmd)' value="0">Wył</button>
                            </span>
                        </div>
                    </div>
                    </div>
                </fieldset>
            </div>
        </div><!-- koniec wiersza-->
    </div>
{% end %}
{% block scripts %}
<script>
    var initv = {{ init }}
</script>
{% end %}
