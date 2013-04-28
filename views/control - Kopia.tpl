{% extends "base.tpl" %}
{% block title %}Control{% end %}
{% block content %}
    <h1>Control</h1>
    <p>Szkic!</p>

    <div class="control" ng-controller="controlCtrl">
        <div class="container row"><!-- poczatek wiersza-->
            <div class="third">
                <fieldset>
                    <legend>relayNode01</legend>
                    <div class ="containter row">
                        <div class="half">Relay 00</div>
                        <div class="half">
                            <form>
                                <input type="radio" ng-model="rn1_00" ng-change='change(rn1_00, name="rn1", cmd="00")' value="1">Wł
                                <input type="radio" ng-model="rn1_00" ng-change='change(rn1_00, name="rn1", cmd="00")' value="0">Wył
                            </form>
                        </div>
                    </div>
                    <div class ="containter row">
                        <div class="half">Relay 01</div>
                        <div class="half">
                            <form>
                                <input type="radio" ng-model="rn1_01" ng-change='change(rn1_01, name="rn1", cmd="01")' value="1">Wł
                                <input type="radio" ng-model="rn1_01" ng-change='change(rn1_01, name="rn1", cmd="01")' value="0">Wył
                            </form>
                        </div>
                    </div>
                    <div class ="containter row">
                        <div class="half">Relay 02</div>
                        <div class="half">
                            <form>
                                <input type="radio" ng-model="rn1_02" ng-change='change(rn1_02, name="rn1", cmd="02")' value="1">Wł
                                <input type="radio" ng-model="rn1_02" ng-change='change(rn1_02, name="rn1", cmd="02")' value="0">Wył
                            </form>
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