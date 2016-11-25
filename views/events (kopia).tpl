{% extends "base.tpl" %}
{% block title %}Zdarzenia{% end %}

{% block content %}
    <div ng-controller="eventsCtrl">
    <h1 class="page-header">Zdarzenia <small>Lista zdarzeń</small></h1>
    <div class="row">
    <!-- Panel -->
    <div class="col-sm-4">
    <div class="panel panel-primary">
     <div class="panel-heading">Termostat P4</div>
     <div class="panel-body">
      <!-- Table -->
      <table class="table">
        <th>Teraz</th><th>Nastawa</th><th>Status</th>
        <tr>
        <td>40</td><td>54</td><td>Włączony</td>
        </tr>
      </table>
      <!-- Koniec Table -->
     </div>
    </div>
    </div>
     <!-- Koniec Panel -->
    </div>
    <div class="row">
    <div class="col-sm-4">
    <div class="panel panel-primary">
    <div class="panel-heading">Pokój Artura</div>
  <div class="panel-body">
         <table class="table">
        <th>Nap. baterii</th><th>Temperatura</th><th>Ciśnienie</th>
        <tr>
        <td>3,900</td><td>23*C</td><td>1000hPa</td>
        </tr>
      </table>
  </div>
  <div class="panel-footer panel-primary">16:32:12 | 20/11</div>
</div>
</div>

<div class="col-sm-4">
    <div class="panel panel-primary">
    <div class="panel-heading"><b>Pokój Artura</b></div>
  <div class="panel-body">
         <table class="table">
        <th>Nap. baterii</th><th>Temperatura</th><th>Ciśnienie</th>
        <tr>
        <td>3,900</td><td>23*C</td><td>1000hPa</td>
        </tr>
      </table>
  </div>
  <div class="panel-footer panel-primary">16:32:12 | 20/11</div>
</div>
</div>

<div class="col-sm-4">
    <div class="panel panel-primary">
    <div class="panel-heading"><b>Pokój Artura</b></div>
  <div class="panel-body">
         <table class="table">
        <th>Nap. baterii</th><th>Temperatura</th><th>Ciśnienie</th><th>Wilgotność</th>
        <tr>
        <td><h5>3,900</h5</td><td><h5>23*C</h5></td><td><h5>1000hPa</h5></td><td><h5>47%</h5></td>
        </tr>
      </table>
  </div>
  <div class="panel-footer panel-primary">16:32:12 | 20/11</div>
</div>  
</div>

</div>
    </div>
{% end %}
