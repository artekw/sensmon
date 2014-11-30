{% extends "base.tpl" %}
{% block title %}Graphs{% end %}

{% block content %}
    <h1 class="page-header">Wykresy <small>Wykresy odczytów</small></h1>
    <div id="graph" ng-controller="graphsCtrl">
        <div id="graph-forms">
            <form class="forms columnar">
                <fieldset>
                    <legend>Ustawienia wykresu</legend>
                    <ul>
                        <li>
                            <label class="bold">Zakres:</label>
                            <select ng-model="limit" ng-options="l.title for l in limits"></select>
                        </li>
                        <li>
                            <label class="bold">Punkt:</label>
                            <select ng-model="node" ng-options="n.name for n in nodes"></select>
                        </li>
                        <li>
                            <label class="bold">Czujnik:</label>
                            <select ng-model="sensor" ng-options="s.title for s in sensors"></select>
                        </li>
                        <li class="push">
                            <input type="submit" class="btn" value="Rysuj wykres" ng-click="drawPlot()" />
                        </li>
                    </ul>
                </fieldset>
            </form>
            <form class="forms columnar">
                <fieldset>
                    <legend>Statystyka</legend>
                    <ul>
                        <li>
                            <label class="bold">Minimalna:</label>{{! minimum }}
                        </li>
                        <li>
                            <label class="bold">Maksymalna:</label>{{! maximum }}
                        </li>
                        <li>
                            <label class="bold">Średnia: </label>{{! average }}
                        </li>
                        <li>
                            <label class="bold">Pomiarów:</label>{{! points}}
                        </li>
                    </ul>
                </fieldset>
        </div>
        <div id="graph-chart" style="height: 530px; width: 65%"></div>
        <div style="clear:both;"></div>
    </div>
{% end %}

<script>
</script>
