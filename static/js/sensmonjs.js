var sensmon = angular.module('sensmon', []);
/*
TODO:
- port websocket z konfiguracji
*/

/*
http://plnkr.co/edit/FFBhPIRuT0NA2DZhtoAD?p=preview
http://vxtindia.com/blog/8-tips-for-angular-js-beginners/
*/

sensmon.run(function($rootScope, $http) {
    $rootScope.hello = function() {
        $http.get('/static/conf/settings.json').success(function(result) {
            return result;
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
            '<td class="{{boxescolor[$index]}}-head"><h1 class="kafelki">Nazwa</h1><h3 class="kafelki">{{nodescfg|showkeys:$index}}</h3></td>' +
            '<td class="{{boxescolor[$parent.$index]}}" ng-repeat="a in n"><h1 class="kafelki">{{a.desc}}</h1><h3 class="kafelki">{{array[$parent.$index][$index]|isdate}} {{a.unit}}</h3></td>' +
            '</tr>' +
            '</tbody>' +
            '</table>',
        replace: true,
        link: function (scope, element, attrs) {}
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

/* filters */

sensmon.filter('showkeys', function() {
    return function(input, onekey) {
        var out = [];
        out = Object.keys(input);
        out = out.sort()
        onekey = onekey || 0;
        out = out[onekey];
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

function logsCtrl($scope) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8081/websocket");
    msg = []
    $scope.hello();
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

    $scope.boxescolor  = ['bluebox', 'orangebox', 'concretebox', 'greenbox', 'amethystbox']

    $http.get('/static/conf/nodes.json').success(function(result) {
        console.log('Generuje tabele');
        $scope.nodescfg = result;
        nodes = _.keys(result).sort();
        $scope.init(); // init values
    });
}