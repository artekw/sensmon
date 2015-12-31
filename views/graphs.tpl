{% extends "base.tpl" %}
{% block title %}Graphs{% end %}

{% block content %}
    <h1 class="page-header">Wykresy <small>Wykresy odczytów</small></h1>
    <div id="graph" ng-controller="graphsCtrl">
    <div class="row">
        <div class="col-md-2">
            <form>
                <fieldset>
                    <legend>Ustawienia wykresu</legend>
                    <div class="form-group">
                        <label class="bold">Zakres:</label>
                        <select ng-model="limit" ng-options="l.title for l in limits"></select>
                        </div>
                        <div class="form-group">
                        <label class="bold">Punkt:</label>
                        <select ng-model="node" ng-options="n.name for n in nodes"></select>
                        </div>
                        <div class="form-group">
                        <label class="bold">Czujnik:</label>
                        <select ng-model="sensor" ng-options="s.title for s in sensors"></select>
                        </div>
                        <button type="submit" class="btn btn-default" ng-click="drawPlot()" />Rysuj wykres</button>
                </fieldset>
            </form>
            <br>
            <form>
                <fieldset>
                    <legend>Statystyka</legend>
                    <div class="form-group">
                            <label class="bold">Minimalna:</label> {{! minimum }}
                            </div>
                            <div class="form-group">
                            <label class="bold">Maksymalna:</label> {{! maximum }}
                            </div>
                            <div class="form-group">
                            <label class="bold">Średnia:</label> {{! average }}
                            </div>
                            <div class="form-group">
                            <label class="bold">Pomiarów:</label> {{! points}}
                            </div>
                </fieldset>
                </form>
        </div>
        <div class="col-md-10">
            <div id="graph-chart" style="height: 530px; width: 100%; border-width: 1px; border-style: solid"></div>
        </div>
        <div style="clear:both;"></div>
    </div>
    </div>
{% end %}
