{% extends "base.tpl" %}
{% block title %}Info{% end %}
{% block content %}
  <h1 class="page-header">System</h1>
    <div class="panel panel-primary">
      <div class="panel-heading">About system</div>
      <div class="panel-body">
        <ul class="list-group">
          <li class="list-group-item"><b>System:</b> {{ system }}</li>
          <li class="list-group-item"><b>Architecture:</b> {{ arch }}</li>
          <li class="list-group-item"><b>Device:</b> {{ machine }}</li>
          <li class="list-group-item"><b>System Load:</b> {{ lavg }}</li>
          <li class="list-group-item"><b>Uptime:</b> {{ uptime }}</li>
          <!-- <li class="list-group-item"><b>Temperatura CPU:</b> {{ cpu_temp }} *C</li>-->
        </ul>
      </div>
    </div>
{% end %}
