var myapp = angular.module('myapp', []);

/*

http://plnkr.co/edit/FFBhPIRuT0NA2DZhtoAD?p=preview

*/

/* directives */

myapp.directive('tabKafelki', function($compile) {
    return {
        restrict: 'E',
        template:
            '<table class="boxes" width="100%">' +
            '<tbody>' +
            '<tr ng-repeat="n in nodescfg">' +
            '<td class="{{boxescolor[$index]}}-head"><h1>Nazwa</h1><h3>{{nodescfg|showkeys:$index}}</h3></td>' +
            '<td class="{{boxescolor[$parent.$index]}}" ng-repeat="a in n"><h1>{{a.desc}}</h1><h3>{{array[$parent.$index][$index]}} {{a.unit}}</h3></td>' +
            '</tr>' +
            '</tbody>' +
            '</table>',
        replace: true,
        link: function (scope, element, attrs) {}
    };
});

/* filters */

myapp.filter('showkeys', function() {
    return function(input, onekey) {
        var out = [];
        out = Object.keys(input);
        out = out.sort()
        onekey = onekey || 0;
        out = out[onekey];
        return out;
    }
});

myapp.filter('onlysensors', function() {
    return function(input) {
        return _.omit(input, 'name', 'timestamp');
    }
});


/* controllers */
function infoCtrl($scope) {
    var ws = new WebSocket("ws://"+document.location.hostname+":8080/websocket");
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

function tabCtrl($scope, $http) {
    $http.get('/static/nodes.json').success(function(result) {
        console.log('Generuje tabele');
        $scope.nodescfg = result;
        nodes = _.keys(result).sort();
        $scope.init(); // init values
    });

    var ws = new WebSocket("ws://"+document.location.hostname+":8080/websocket");

    var data = [];
    var nodes = [];

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
                    this[_.indexOf(nodes, v)] = _.values(_.omit(sortedJSONObj, 'name', 'timestamp'));
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

    $scope.init = function() {
        angular.forEach(initv, function(v) {
            $scope.parseObj(v)
        })
        console.log('Ładuje wartosci wstępne z Redis')

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
}