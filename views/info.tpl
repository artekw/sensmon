{% extends "base.tpl" %}
{% block title %}Info{% end %}
{% block content %}
  <h1 class="page-header">System</h1>
    <div class="panel panel-primary">
      <div class="panel-heading">Informacje o systemie</div>
      <div class="panel-body">
        <ul class="list-group">
          <li class="list-group-item"><b>System:</b> {{ system }}</li>
          <li class="list-group-item"><b>Architektura:</b> {{ arch }}</li>
          <li class="list-group-item"><b>Urządzenie:</b> {{ machine }}</li>
          <li class="list-group-item"><b>Obciążenie:</b> {{ lavg }}</li>
          <li class="list-group-item"><b>Czas pracy:</b> {{ uptime }}</li>
          <li class="list-group-item"><b>Temperatura CPU:</b> {{ cpu_temp }} *C</li>
        </ul>
      </div>
    </div>
{% end %}
