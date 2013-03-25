<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html ng-app="myapp">
<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="senscms">
    <meta name="author" content="arteq">

    <link <link rel="stylesheet/less" type="text/css" href="static/less/kube.less" />
    <title>{% block title %}{% end %} - sensmon v0.2</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <script src="static/js/jquery.min.js"  type="text/javascript">></script>
    <script src="static/js/underscore-min.js" type="text/javascript"></script>
    <script src="static/js/angular.min.js" type="text/javascript"></script>
    <script src="static/js/app.js" type="text/javascript"></script>
    <script src="static/js/less-1.3.3.min.js" type="text/javascript"></script>
    {% end %}
</head>
<body>
    <div id="wrapper">
        <div id="top" class="group">
            {% block top %}
            <h3>sensmon</h3>
            <nav>
                <ul>
                    <li><a href="/">Home</a></li>
                    <li><a href="/dash">Dash</a></li>
                    <li><a href="/logs">Logs</a></li>
                    <li><a href="/info">Info</a></li>
                </ul>
            </nav>
            {% end %}
        </div>
        <div id="content">{% block content %}{% end %}</div>
        </div>
    </div>
    {% block scripts %}
    {% end %}
</body>