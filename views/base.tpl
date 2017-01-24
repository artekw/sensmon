<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html xmlns:ng="http://angularjs.org" ng-app="sensmon">
<head>
    <base href="/">
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="sensmon - home automation">
    <meta name="author" content="Artur Wronowski">

    <!--<link rel="stylesheet" href="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">-->
    <!-- https://www.bootstrapcdn.com/bootswatch/ -->
    <link href="https://maxcdn.bootstrapcdn.com/bootswatch/3.3.7/united/bootstrap.min.css" rel="stylesheet" integrity="sha384-pVJelSCJ58Og1XDc2E95RVYHZDPb9AVyXsI8NoVpB2xmtxoZKJePbMfE4mlXw7BJ" crossorigin="anonymous">
    <link rel="stylesheet" href="/static/plugins/owfont/css/owfont-regular.min.css" type="text/css">
    <link rel="stylesheet" href="/static/plugins/weathericons/css/weather-icons.min.css" type="text/css">
    <link rel="stylesheet" href="http://getbootstrap.com/examples/signin/signin.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/font-awesome/4.5.0/css/font-awesome.min.css">
    <link rel="stylesheet" href="/static/css/angular-toggle-switch-bootstrap-3.css">
    <link rel="stylesheet" href="/static/css/styl.css">

    <title>{% block title %}{% end %} - sensmon</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <!--[if lte IE 8]>
      <script src="http://cdnjs.cloudflare.com/ajax/libs/json3/3.2.4/json3.min.js"></script>
    <![endif]-->
    <script src="/static/js/jquery.min.js" type="text/javascript"></script>
    <script src="//maxcdn.bootstrapcdn.com/bootstrap/3.2.0/js/bootstrap.min.js" type="text/javascript"></script>
    <script src="/static/js/highstock.src.js" type="text/javascript"></script>
    <script src="/static/js/underscore-min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.5.0/angular.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.5.0/angular-animate.min.js" type="text/javascript"></script>
    <script src="https://code.angularjs.org/1.5.0/angular-route.js" type="text/javascript"></script>
    <!-- https://libraries.io/bower/angular-bootstrap-toggle-switch -->
    <script src="/static/js/angular-toggle-switch.min.js" type="text/javascript"></script>
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
				<div class="navbar-collapse collapse" ng-controller="HeaderController">
					<ul class="nav navbar-nav">
						<li ng-class="{ active: isActive('/')}"><a target="_self" href="/"><i class="fa fa-home fa-fw" aria-hidden="true"></i>&nbsp;Intro</a></li>
                        <li ng-class="{ active: isActive('/weather')}"><a target="_self" href="/weather"><i class="fa fa-sun-o fa-fw" aria-hidden="true"></i>&nbsp;Weather</a></li>
						<li ng-class="{ active: isActive('/dash')}"><a target="_self" href="dash"><i class="fa fa-tachometer fa-fw" aria-hidden="true"></i>&nbsp;Sensors</a></li>
                        <li ng-class="{ active: isActive('/switches')}"><a target="_self" href="switches"><i class="fa fa-flash fa-fw" aria-hidden="true"></i>&nbsp;Switches</a></li>
						<li ng-class="{ active: isActive('/info')}"><a target="_self" href="info"><i class="fa fa-info fa-fw" aria-hidden="true"></i>&nbsp;Info</a></li>
					</ul>
					<ul class="nav navbar-nav navbar-right">
						{% if current_user %}
							<li ng-class="{ active: isActive('/logout?next={{ url_escape(request.uri) }}')}"><a target="_self" href="/logout?next={{ url_escape(request.uri) }}"><i class="fa fa-sign-in fa-fw" aria-hidden="true"></i>&nbsp;Logout</a></li>
						{% else %}
							<li ng-class="{ active: isActive('/login?next={{ url_escape(request.uri) }}')}"><a target="_self" href="/login?next={{ url_escape(request.uri) }}"><i class="fa fa-sign-out fa-fw" aria-hidden="true"></i>&nbsp;Login</a></li>
						{% end %}
					</ul>
				</div>
        <div ng-view></div>
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
