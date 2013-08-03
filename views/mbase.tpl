<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html xmlns:ng="http://angularjs.org" id="ng-app" ng-app="sensmon">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>
    <meta name="apple-mobile-web-app-capable" content="yes" />
    <meta name="format-detection" content="telephone=no" />
    <meta name="description" content="sensmon">
    <meta name="author" content="arteq">
<!--
    <link rel="stylesheet/less" type="text/css" href="static/less/mkube.less" media="all"/>
-->
    <link href="http://www.afk.mk/d/zepto/examples/iphone/iphone.css" media="screen" rel="stylesheet" type="text/css" />
    <title>sensmon v0.2</title>
    <script src="static/js/jquery.min.js" type="text/javascript"></script>
    <script src="static/js/less-1.3.3.min.js" type="text/javascript"></script>
    <script src="static/js/underscore-min.js" type="text/javascript"></script>
    <script src="static/js/angular.min.js" type="text/javascript"></script>
    <script src="static/js/angular-mobile.js" type="text/javascript"></script>
    <script src="static/js/sensmonjs.js" type="text/javascript"></script>
    <script src="static/js/mobile/zepto.js" type="text/javascript"></script>
    <script src="static/js/mobile/touch.js" type="text/javascript"></script>
    <script src="static/js/mobile/ajax.js" type="text/javascript"></script>

</head>
<body>
<div ng-controller="mobileCtrl">
    Test Mobile

    {{! testt }}
      <section id="menu">
        <div class="toolbar">
          <h1>Title</h1>
        </div>
        <ul class="menu">
          <li class="arrow"><a href="#menu_1">Menu 1</a></li>
          <li>Menu 1</li>
          <li>Menu 1</li>
          <li>Menu 1</li>
          <li>Menu 1</li>
        </ul>
      </section>
      <section id="menu_1">
        <div class="toolbar">
          <h1>Menu 1</h1>
        </div>
        <ul class="menu">
          <li>SubMenu 1</li>
          <li>SubMenu 2</li>
        </ul>
      </section>
</div>
      <script>
        $(document).ready(function(){
          var activate = ('createTouch' in document) ? 'touchstart' : 'click'

          $("body > section").first().addClass("current")

          $("a.back").on(activate, function(event) {
            var current = $(this).attr("href")
            $(".current").removeClass("current").addClass("reverse")
            $(current).addClass("current")
          })

          $(".menu a[href]").on(activate, function(event) {
            var link = $(this), section = link.closest('section'),
              prev_element = "#"+(section.removeClass("current").addClass("reverse").attr("id"))
            $(link.attr("href")).addClass("current")
            $(".current .back").remove()
            $(".current .toolbar").prepend("<a href=\""+prev_element+"\" class=\"back\">Back</a>")
          })
        })
      </script>

</body>
</html>