/*
TODO:
- port websocket z konfiguracji
*/

/*
http://plnkr.co/edit/FFBhPIRuT0NA2DZhtoAD?p=preview
http://vxtindia.com/blog/8-tips-for-angular-js-beginners/
http://andru.co/building-a-simple-single-page-application-using-angularjs
https://github.com/ankane/chartkick.js
*/


var sensmon = angular.module('sensmon', []);

sensmon.run(function($rootScope, $http) {
  $rootScope.nodes = function() {
    $http.get('/static/conf/nodes.json').success(function(result) {
        return result
    })
  }
});

/* directives */
// http://doc.owncloud.org/server/5.0/developer_manual/angular.html#using-angularjs-in-your-project

sensmon.directive('tabKafelki', function($compile) {
    return {
        restrict: 'E',
        template:
            '<table class="boxes">' +
            '<tbody>' +
            '<tr ng-repeat="n in nodescfg">' +
            '<td class="{{boxescolor[$index]}}-head"><h3 class="kafelki">Nazwa</h3><h1 class="kafelki">{{nodescfg|showkeys:$index}}</h1><span class="qrcode" style="display:none" showonhoverparent><img src="static/img/qrcodes/{{nodescfg|showkeys:$index}}.png"></span></td>' +
            '<td class="{{boxescolor[$parent.$index]}}" ng-repeat="a in n"><h3 class="kafelki">{{a.desc}}</h3><h1 class="kafelki">{{array[$parent.$index][$index]|isdate}} {{a.unit}}</h1></td>' +
            '</tr>' +
            '</tbody>' +
            '</table>',
        replace: true,
        link: function (scope, element, attrs) {}
    };
});


sensmon.directive('showonhoverparent',
   function() {
      return {
         link : function(scope, element, attrs) {
            element.parent().bind('mouseenter', function() {
                element.show();
            });
            element.parent().bind('mouseleave', function() {
                 element.hide();
            });
       }
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

sensmon.filter('showkeys', function() {
    return function(input, index) {
        var out = [];
        out = Object.keys(input);
        out = out.sort()
        index = index || 0;
        out = out[index];
        return out;
    }
});

sensmon.filter('onlysensors', function() {
    return function(input) {
        return _.omit(input, 'name', 'timestamp');
    }
});

sensmon.filter('isdate', function(dateFilter) {
    return function(date) {
        // FIXME!
        var patern = new RegExp("[0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]");
        if (patern.test(date)) {
            return dateFilter(date * 1000, 'HH:mm:ss')
        }
        else {
            return date
        }
    }
});




/* controllers */

function mobileCtrl($scope, $rootScope){
    $scope.testt = 'from scope :)'
}

// https://github.com/jcw/housemon/blob/master/client/code/modules/graphs.coffee
// http://www.humblesoftware.com/flotr2/documentation
// http://stackoverflow.com/questions/6064987/using-map-reduce-in-couchdb-to-output-fewer-rows/6066433#6066433
// http://dygraphs.com/#usage
https://github.com/jcw/housemon/blob/develop/client/code/modules/graphs.coffee
// http://jsfiddle.net/KmXTy/14/ - loading
function graphsCtrl($scope){
    // ustawienia
    var timezone_offset = 7200; // +2h - Europe/Warsaw

    $scope.limits = [
        {'title': 'Godzina','offset': 3600},
        {'title': 'Dzień', 'offset': 86400},
        {'title': 'Dwa dni', 'offset': 172800},
        {'title': 'Tydzień', 'offset': 604800},
        {'title': 'Miesiąc', 'offset': 2592000}
    ]
    $scope.limit = $scope.limits[0] // domyślnie pierwsza pozycja

    // FIXME! - pobieranie z pliku json nodes.json
    $scope.nodes = [
        {'name': 'artekroom'},
        {'name': 'outnode'},
        {'name': 'powernode'},
        {'name': 'testnode'}
    ]
    $scope.node = $scope.nodes[0]

    $scope.sensors = [
        {'title': 'Temperatura', 'name': 'temp'},
        {'title': 'Ciśnienie', 'name': 'press'},
        {'title': 'Wilgotność', 'name': 'humi'},
        {'title': 'Napięcie baterii', 'name': 'batvol'},
        {'title': 'Moc bierna', 'name': 'power'},
        {'title': 'Nasłonecznienie', 'name': 'light'}
    ]
    $scope.sensor = $scope.sensors[0];

    $scope.minimum = 0
    $scope.maximum = 0
    $scope.average = 0
    $scope.points = 0

    $scope.drawPlot = function() {
        // zmienne
        var pdb = Pouch('http://192.168.88.20/couchdb/sensmon')
        var flotr_data = [];
        var data_values = [];
        var unix_now = Math.round((new Date()).getTime() / 1000) + timezone_offset;
        var last_day = (unix_now - $scope.limit.offset ) - timezone_offset;

        // debug
        //console.log("now:", unix_now);
        //console.log("last:", last_day);

        // http://192.168.88.20/couchdb/sensmon/_design/node/_view/by_date_name?startkey=[%22artekroom%22,1367586876]&endkey=[%22artekroom%22,1367808365]
        pdb.query('node/by_date_name', {reduce: false, startkey: [$scope.node.name, last_day], endkey: [$scope.node.name, unix_now]}, function(err, response) {

            if (err) {
                console.log('error')
            }

            console.log(response)

            angular.forEach(response.rows, function(v) {
                flotr_data.push([v.key[1]*1000, v.value[$scope.sensor.name]]);
                data_values.push(v.value[$scope.sensor.name])
            });

            $scope.minimum = _.min(data_values)
            $scope.maximum = _.max(data_values)
            $scope.average = Math.round(_.reduce(data_values, function(memo, num){ return memo + num; }, 0) / data_values.length*100)/100;
            $scope.points = data_values.length
            $scope.$apply();

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
        });
    }
}

// format daty na etykiecie
myFormatter = function(obj) {
    var d, t;
    d = new Date(Math.floor(obj.x));
    t = Flotr.Date.format(d, '%b %d, %H:%M:%S', 'local');
    return " " + t + ": " + obj.y + " ";
};

function logsCtrl($scope) {
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
}

function controlCtrl($scope) {
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
}

function dashCtrl($scope, $http) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8081/websocket");

    var data = []; // dane finalne jak tablica
    var nodes = []; // lista punktów w konfiguracji

    function sortObject(o) {
        var sorted = {},
        key, a = [];

        for (key in o) {
            if (o.hasOwnProperty(key)) {
                a.push(key);
            }
        }

        a.sort();

        for (key = 0; key < a.length; key++) {
            sorted[a[key]] = o[a[key]];
        }
        return sorted;
    }

    $scope.parseObj = function (jsonObj) {
        if (_.isEmpty(jsonObj)) {
            return // pustym "obiektom" dziekujemy :)
        }

        sortedJSONObj = sortObject(jsonObj); // sortowanie po kluczu

        $scope.lastupd = sortedJSONObj['timestamp']*1000
        $scope.updfrom = sortedJSONObj['name']

        $scope.safeApply(function() {
            angular.forEach(nodes, function(v) {
                if (v = sortedJSONObj.name) {
                    this[_.indexOf(nodes, v)] = _.values(_.omit(sortedJSONObj, 'name'));
                }
                }, data);

            $scope.array = data;
        });
    }

    // safeApply: https://coderwall.com/p/ngisma
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

    // z redis dane chwilowe
    $scope.init = function() {
        angular.forEach(initv, function(v) {
            $scope.parseObj(v)
        })
        console.log('Wczytuję wartosci wstępne z Redis')

    }

    ws.onmessage = function (evt) {
        jsonObj = JSON.parse(evt.data);
        $scope.parseObj(jsonObj);
    }

    ws.onopen = function() {
        console.log('Sesja websocket rozpoczęta')
    }

    ws.onclose = function() {
        console.log('Narazie :)')
    }
/*
    $scope.mouseoverKaf = function(n, index) {
        var out = [];
        out = Object.keys(n);
        out = out.sort()
        index = index || 0;
        out = out[index];
        console.log ("Mouse Over: " + out)
    }
*/
    $scope.boxescolor  = ['bluebox', 'orangebox', 'concretebox', 'greenbox', 'amethystbox']

    $http.get('/static/conf/nodes.json').success(function(result) {
        console.log('Generuje tabele');
        $scope.nodescfg = result;
        nodes = _.keys(result).sort();
        $scope.init(); // init values
    });
}