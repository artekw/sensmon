/*
TODO:
- port websocket z konfiguracji
*/

/*
Linki:
http://plnkr.co/edit/FFBhPIRuT0NA2DZhtoAD?p=preview
http://vxtindia.com/blog/8-tips-for-angular-js-beginners/
http://andru.co/building-a-simple-single-page-application-using-angularjs
https://github.com/ankane/chartkick.js
*/


var sensmon = angular.module('sensmon', ['ngAnimate']);

/* directives */

sensmon.directive('animateOnChange', function($timeout) {
  return function(scope, element, attr) {
    scope.$watch(attr.animateOnChange, function(nv,ov) {
      if (nv!=ov) {
        element.addClass('changed');
        $timeout(function() {
          element.removeClass('changed');
        }, 1000); // Could be enhanced to take duration as a parameter
      }
    });
  };
});


sensmon.directive('buttonsRadio', function() {
    return {
        restrict: 'A',
        require: 'ngModel',
        link: function($scope, element, attr, ctrl) {
            element.bind('click', function() {
                $scope.$apply(function(scope) {
                    ctrl.$setViewValue(attr.value);
                });
            });

            // This should just be added once, but is added for each radio input now?
            $scope.$watch(attr.ngModel, function(newValue, oldValue) {
                element.parent(".btn-group").find('button').removeClass("btn-active");
                element.parent(".btn-group") //.children()
                .find("button[value='" + newValue + "']").addClass('btn-active');
            });
        }
    };
});


// http://jsfiddle.net/kurtteichman/KDYSN/
// http://plnkr.co/edit/8Bo2YD9AWaUwLDXr6IGk?p=preview
sensmon.directive("chart", function() {
  return {
    restrict: "E",
    scope: {
      data: "@",
      options: "@",
      id: "@"
    },
    link: function(scope, elem, attrs) {
            //console.log(val);
            var flot = {};
            flot.id = (attrs.id !== undefined) ? attrs.id : (Math.random().toString().split(".")[1]);

            attrs.$observe("data", function(nv) {
               if (angular.isDefined(nv)) {
                 flot.data = nv;
               }
            });
            attrs.$observe("options", function(nv){
              if(angular.isDefined(nv)){
                flot.options = nv;
              }
              else { flot.options = {};}
            });

            scope.$watch(function(){
              return flot;
            }, function() {
              console.log(flot);
              // this works with no errors but without data/chart
              //Flotr.draw(document.getElementById(attrs.id), [flot.data], flot.options);
              //this results in an error "The target container must be visible"
              //Flotr.draw(elem, [flot.data], flot.options);

              elem.attr("id", flot.id);
              Flotr.draw(document.getElementById(flot.id), [flot.data], flot.options);
            }, true);
    }
  };
});



/* filters */

sensmon.filter('parsedate', function(dateFilter) {
    return function(date) {
        // FIXME!
        var patern = new RegExp("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]");
        if (patern.test(date)) {
            return dateFilter(date * 1000, 'HH:mm:ss | dd/MM')
        }
        else {
            return date
        }
    }
});


sensmon.filter('nodate', function() {
    return function(input) {
        return _.omit(input, 'timestamp');
            }
});



/* controllers */

// graphs page
sensmon.controller('graphsCtrl', function ($scope, $http) {
    // ustawienia
    var timezone_offset = 7200; // +2h - Europe/Warsaw
    var offset = 86400;

    var response = [];

    $scope.limit = {'title': 'Godzina','offset': 3600};
    $scope.sensor = {'title': 'Temperatura', 'name': 'temp'};
    $scope.node = "test";

    $scope.minimum = 0
    $scope.maximum = 0
    $scope.average = 0
    $scope.points = 0


    $scope.drawPlot = function() {
        // zmienne
        var response = $scope.response;
        var flotr_data = [];
        var data_values = [];
        var unix_now = Math.round((new Date()).getTime() / 1000) + timezone_offset;
        var last_day = (unix_now - offset ) - timezone_offset;


        angular.forEach(response.data, function(v) {
            flotr_data.push([v[0]*1000, v[1]]);
            data_values.push(v[1])
        });
        
        $scope.minimum = _.min(data_values)
        $scope.maximum = _.max(data_values)
        $scope.average = Math.round(_.reduce(data_values, function(memo, num){ return memo + num; }, 0) / data_values.length*100)/100;
        $scope.points = data_values.length
        //$scope.$apply();
        
        // opcje wykresu
        $scope.flotr = {
            data: flotr_data,

                options: {
                    title: $scope.sensor.title + ' dla ' + $scope.node.name + ', ostatnie ' + $scope.limit.offset/3600 + ' h',
                    xaxis : {
                        mode : 'time',
                        title : 'Czas pomiaru',
                        tickDecimals: 0,
                        timeFormat : '%H:%M, %d/%m/%y',
                        timeMode: 'local',
                    },
                    yaxis : {
                        autoscale : true,
                    },
                    mouse: {
                        track: true,
                        sensibility: 10,
                        trackFormatter: myFormatter
                    }
                }
            }
            Flotr.draw(document.getElementById("graph-chart"), [$scope.flotr.data], $scope.flotr.options);
    }

    $http.get('/static/conf/nodemap.json').success(function(data) { 
        console.log('Pobrano mapę punktów(nodów)');
        $scope.nodemap = data;
    });


    $http.get('/history/lab/humi/day').success(function(data) { 
        console.log('Pobrano dane do wykresu');
        $scope.response = data;
        console.log(data);
    });
});

// format daty na etykiecie w wykresie
myFormatter = function(obj) {
    var d, t;
    d = new Date(Math.floor(obj.x));
    t = Flotr.Date.format(d, '%b %d, %H:%M:%S', 'local');
    return " " + t + ": " + obj.y + " ";
};


sensmon.controller('logsCtrl', function ($scope) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8081/websocket");
    msg = []
    ws.onmessage = function (evt) {
        jsonObj = JSON.parse(evt.data);
        if (_.has(jsonObj, 'name')) {
            msg.push(jsonObj)
        }

        $scope.$apply(function() {
            $scope.msg = msg
        });
    }
});


sensmon.controller('controlCtrl', function ($scope) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8081/websocket");

    // załadowanie listy przekaźników
    // TODO


    // filtr
    ws.onmessage = function (evt) {
        jsonObj = JSON.parse(evt.data)
        if (_.has(jsonObj, 'control')){
            console.log(jsonObj.control)
        }
    };

    // http://stackoverflow.com/questions/13077320/angularjs-trigger-when-radio-button-is-selected
    // realcja na zmianę stanu przekaźnika
    $scope.change = function(v, name, cmd) {
        //console.log({"state": v, "name": name, "cmd": cmd})
        ws.send(JSON.stringify({state: v, name: name, cmd: cmd}));
    }

    // z redis dane chwilowe
    $scope.init = function() {
        switches = []
        angular.forEach(initv, function(v) {
            switches.push(v)
        })
        console.log('Wczytuję wartosci wstępne z Redis')
        $scope.switches = switches;

    }
    $scope.init();
});


/* 
dashboard page - data in table 
$scope.array - array with data
*/
sensmon.controller('dashCtrl', function ($scope, $http) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8081/websocket");

    function parseJSON(jsonObj) {
		jsonParsed = JSON.parse(jsonObj);
        if (_.isEmpty(jsonParsed)) {
            return // pustym "obiektom" dziekujemy :)
        }

        $scope.safeApply(function() {
            $scope.array = jsonParsed;
        });
    }


    $scope.safeApply = function(fn) {
        var phase = this.$root.$$phase;
        if(phase == '$apply' || phase == '$digest') {
            if(fn && (typeof(fn) === 'function')) {
                fn();
            }
        } else {
            this.$apply(fn);
        }
    };

    ws.onmessage = function (evt) {
        jsonObj = evt.data;
        parseJSON(jsonObj);
        console.log('Otrzymano nowe dane')
    }

    ws.onopen = function() {
        console.log('Sesja websocket rozpoczęta')
    }

    ws.onclose = function() {
        console.log('Narazie :)')
    }

    // hover
    $scope.hoverIn = function(){
        this.hoverEdit = true;
    };

    $scope.hoverOut = function(){
        this.hoverEdit = false;
    };

	$http.get('/initv').success(function(data) {
		console.log('Pobrano ostatnie wartości');
        parseJSON(data);
	});

});


sensmon.controller('HeaderController', function ($scope, $location) 
{ 
    $scope.navClass = function (page) {
        var currentRoute = $location.path().substring(1) || '/';
        return page === currentRoute ? 'active' : '';
    };    
});
