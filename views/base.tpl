<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html xmlns:ng="http://angularjs.org" id="ng-app" ng-app="sensmon">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="sensmon">
    <meta name="author" content="arteq">

    <link rel="stylesheet/less" type="text/css" href="static/less/kube.less" media="all"/>
    <title>{% block title %}{% end %} - sensmon v0.3</title>
    <link href='http://fonts.googleapis.com/css?family=Dosis:400,500,600,700|Lato:400,700,900,400italic|Monda:400,700&subset=latin,latin-ext' rel='stylesheet' type='text/css'>
    <!--[if lte IE 8]>
      <script src="http://cdnjs.cloudflare.com/ajax/libs/json3/3.2.4/json3.min.js"></script>
    <![endif]-->
    <script src="static/js/jquery.min.js" type="text/javascript"></script>
    <script src="static/js/flotr2.min.js" type="text/javascript"></script>

    <script src="static/js/underscore-min.js" type="text/javascript"></script>
    <script src="static/js/less-1.3.3.min.js" type="text/javascript"></script>
    <script src="static/js/kube.buttons.js" type="text/javascript"></script>
    <script src="static/js/angular.min.js" type="text/javascript"></script>
    <script src="static/js/angular-mobile.js" type="text/javascript"></script>
    <script src="static/js/angular-resource.js" type="text/javascript"></script>
    <script src="static/js/require.js" type="text/javascript"></script>
    <script src="static/js/sensmonjs.js" type="text/javascript"></script>
<!--
    <script src="static/js/pouchdb-nightly.js"></script>
-->
    <script src="http://download.pouchdb.com/pouchdb-nightly.min.js"></script>
<!--
    <script src="/couchdb/_utils/script/couch.js"></script>
    <script src="http://www.eddelbuettel.net/html5/angular-cornercouch.js"></script>
-->

</head>
<body>
    <div id="wrapper">
        <div id="top" class="group">
            <span class="title"><a href="/">sensmon v0.3<sup> alfa</sup></a></span>
            <nav>
                <ul>
                    <li><a href="/">Dash</a></li>
                    <li><a href="/graphs">Graphs</a></li>
                    <li><a href="/control">Control</a></li>
                    <li><a href="/logs">Logs</a></li>
                    <li><a href="/info">Info</a></li>
                </ul>
            </nav>
        </div>
        <div id="content">
            <div class="row">{% block content %}{% end %}</div>
        </div>
        <div id="footer">
            <a href="/m">Mobilna</a> | <a href="https://github.com/artekw/sensmon">Kod</a>
                <div style="float: right">
                    {% if current_user %}
                        <a href="/logout?next={{ url_escape(request.uri) }}">wyloguj</a>
                    {% else %}
                        <a href="/login?next={{ url_escape(request.uri) }}">zaloguj</a>
                    {% end %}
            </div>
        </div>
    </div>
    {% block scripts %}
    {% end %}
</body>
</html>