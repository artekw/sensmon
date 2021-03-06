<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html xmlns:ng="http://angularjs.org" ng-app="sensmon">
<head>
    <base href="/">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="sensmon - home automation">
    <meta name="author" content="Artur Wronowski">

    <link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/css/styl.css">
    <link rel="stylesheet" href="/static/plugins/owfont/css/owfont-regular.min.css" type="text/css">
    <link rel="stylesheet" href="http://getbootstrap.com/examples/signin/signin.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">

    <title>{% block title %}{% end %} - sensmon</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <!--[if lte IE 8]>
      <script src="http://cdnjs.cloudflare.com/ajax/libs/json3/3.2.4/json3.min.js"></script>
    <![endif]-->
    <script src="/static/js/jquery.min.js" type="text/javascript"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="/static/js/highstock.src.js" type="text/javascript"></script>
    <script src="/static/js/underscore-min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular-animate.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.4.8/angular-route.js" type="text/javascript"></script>
    <script src="/static/js/highcharts-ng.js" type="text/javascript"></script>
    <script src="http://momentjs.com/downloads/moment-with-locales.js" type="text/javascript"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/angular-moment/0.10.3/angular-moment.js" type="text/javascript"></script>
    <script src="/static/js/require.js" type="text/javascript"></script>
    <script src="/static/js/sensmonjs.js" type="text/javascript"></script>
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
					<a class="navbar-brand">sensmon</a>
				</div>
				<div class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
						<li><a target="_self" href="/">Intro</a></li>
						<li><a target="_self" href="dash">Czujniki</a></li>
						<!--<li ng-class="navClass('control')"><a href="/control">Sterowanie</a></li>-->
						<li><a target="_self" href="info">Info</a></li>
					</ul>
					<ul class="nav navbar-nav navbar-right">
						{% if current_user %}
							<li><a target="_self" href="/logout?next={{ url_escape(request.uri) }}">Wyloguj</a></li>
						{% else %}
							<li><a target="_self" href="/login?next={{ url_escape(request.uri) }}">Zaloguj</a></li>
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
    <!--
     <div class="footer">
   		  <div class="container text-center">
    		<p class="text-muted credit">
    			<a title="Source on Github" href="https://github.com/artekw/sensmon" target="_blank"><i class="fa fa-github fa-2x"></i></a>
    		</p>
  		</div>
 	</div>-->
</body>
</html>
