{% extends "base.tpl" %}
{% block title %}Login{% end %}
{% block content %}

<div class="units-row">
    <div class="unit-centered unit-40">
        <form class="forms forms-inline" action="/login" method="post">
            <fieldset>
                <legend>Logowanie</legend>
                <input type="text" name="name" placeholder="Login">
                <input type="text" name="pass" placeholder="Haslo">
                <input type="submit" class="btn" value="Logowanie">
                {% if resp %}
                    <div class="error big zero">
                        {{ resp['msg'] }}
                    </div>
                {% end %}
            </fieldset>
        </form>
    </div>
</div>

{% end %}