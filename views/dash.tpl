{% extends "base.tpl" %}
{% block title %}Dash{% end %}
{% block content %}
    <h1>Dash</h1>
    <div class="kafelki" ng-controller="dashCtrl">
        <tab-Kafelki></tab-Kafelki>
        Ostatnia aktualizacja: {{! lastupd|date:'dd/MM/yyyy @ H:mm:ss' }} z {{! updfrom }}
    </div>
{% end %}
{% block scripts %}
<script>
    var initv = {{ init }}
</script>
{% end %}