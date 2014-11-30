{% extends "base.tpl" %}
{% block title %}Login{% end %}
{% block content %}
        <form class="form-signin" role="form" action="/login" method="post">
			<h2 class="form-signin-heading">Logowanie</h2>
                <input type="username" class="form-control" name="name" placeholder="Login" required autofocus>
                <input type="password" class="form-control" name="pass" placeholder="Haslo" required>
                <button type="submit" class="btn btn-lg btn-primary btn-block">Zaloguj</button>
                {% if resp %}
                    <div class="error big zero">
                        {{ resp['msg'] }}
                    </div>
                {% end %}
        </form>

{% end %}
