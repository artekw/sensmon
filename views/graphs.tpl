{% extends "base.tpl" %}
{% block title %}Graphs{% end %}

{% block content %}
    <h1 class="page-header">Wykresy <small>Wykresy odczytów</small></h1>
    <div class="row">
      {% raw content[1] %}
    </div>
{% end %}
{% block scripts %}
  {% raw content[0] %}
{% end %}
