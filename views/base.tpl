<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html xmlns:ng="http://angularjs.org" ng-app="sensmon">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="sensmon">
    <meta name="author" content="Artur Wronowski">

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="static/css/styl.css">
    <!--<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap-theme.min.css">-->
    <link rel="stylesheet" href="http://getbootstrap.com/examples/signin/signin.css">

    <title>{% block title %}{% end %} - sensmon v0.4</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <!--[if lte IE 8]>
      <script src="http://cdnjs.cloudflare.com/ajax/libs/json3/3.2.4/json3.min.js"></script>
    <![endif]-->
    <script src="static/js/jquery.min.js" type="text/javascript"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="static/js/flotr2.min.js" type="text/javascript"></script>
    <script src="static/js/underscore-min.js" type="text/javascript"></script>
	<script src="https://code.angularjs.org/1.3.9/angular.min.js" type="text/javascript"></script>

    <script src="https://code.angularjs.org/1.3.9/angular-touch.min.js" type="text/javascript"></script>

    <script src="static/js/require.js" type="text/javascript"></script>
    <script src="static/js/sensmonjs.js" type="text/javascript"></script>

</head>
<body>
    <div id="wrapper">
        <div class="navbar navbar-inverse navbar-fixed-top" role="navigation">
			<div class="container-fluid">
				<div class="navbar-header">
					<button type="button" class="navbar-toggle" data-toggle="collapse" data-target=".navbar-collapse">
						<span class="sr-only">Toggle navigation</span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
						<span class="icon-bar"></span>
					</button>
					<a class="navbar-brand">sensmon v0.4</a>
				</div>
				<div class="navbar-collapse collapse" ng-controller="HeaderController">
					<ul class="nav navbar-nav">
						<li ng-class="navClass('home')"><a href="/">Czujniki</a></li>
						<li ng-class="navClass('graphs')"><a href="/graphs">Wykresy</a></li>
						<li ng-class="navClass('control')"><a href="/control">Sterowanie</a></li>
						<li ng-class="navClass('logs')"><a href="/logs">Logi</a></li>
						<li ng-class="navClass('info')"><a href="/info">System</a></li>
					</ul>
					<ul class="nav navbar-nav navbar-right">
						{% if current_user %}
							<li><a href="/logout?next={{ url_escape(request.uri) }}">Wyloguj</a></li>
						{% else %}
							<li><a href="/login?next={{ url_escape(request.uri) }}">Zaloguj</a></li>
						{% end %}
					</ul>
				</div>
			</div>
        </div>
        
        <div id="content">
			<div class="container-fluid">
				{% block content %}{% end %}
			</div>
        </div>
	</div>
    {% block scripts %}
    {% end %}
</body>
</html>
