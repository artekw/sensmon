/*
TODO:
- port websocket z konfiguracji
- wczytywanie wykresu
- przyciski zakresów
*/

/*
Linki:
http://plnkr.co/edit/FFBhPIRuT0NA2DZhtoAD?p=preview
http://vxtindia.com/blog/8-tips-for-angular-js-beginners/
http://andru.co/building-a-simple-single-page-application-using-angularjs
https://github.com/ankane/chartkick.js
*/


var sensmon = angular.module('sensmon', ['ngRoute', 'ngAnimate', 'highcharts-ng']);

/* directives */

sensmon.directive('animateOnChange', function($timeout) {
  return function(scope, element, attr) {
    scope.$watch(attr.animateOnChange, function(nv,ov) {
      if (nv!=ov) {
        element.addClass('changed');
        $timeout(function() {
          element.removeClass('changed');
        }, 1000);
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


/* drop timestamp from array */
sensmon.filter('nodate', function() {
    return function(input) {
        return _.omit(input, 'timestamp');
            }
});


/* drop timestamp from array */
sensmon.filter('nobatvol', function() {
    return function(input) {
        return _.omit(input, 'batvol');
            }
});


sensmon.filter('dayOfweekPL', function() {
    return function(input) {
        return moment(input*1000).locale('pl').format('dddd');
            }
});


sensmon.filter('capitalize', function() {
  return function(token) {
      return token.charAt(0).toUpperCase() + token.slice(1);
   }
});


//Inputs a number and outputs an array with that length.
//(3 | array) => [0,1,2]
sensmon.filter('group', function() {
    return function(arrayLength) {
        arrayLength = Math.ceil(arrayLength);
        var arr = new Array(arrayLength), i = 0;
        for (; i < arrayLength; i++) {
            arr[i] = i;
        }
        return arr;
    };
})


/* controllers */
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


sensmon.controller('introCtrl', function ($scope, $interval, $http) {
  $interval(function(){
    $scope.clock = new Date();
  },500);

  $scope.today = function(date) {
      return moment(date).locale('pl').format('dddd, DD MMMM YYYY');
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
dashboard page
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
            console.log($scope.array);
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


sensmon.config(function ($routeProvider, $locationProvider) {
    // configure the routing rules here
    $routeProvider.when('/graphs/:nodename/:sensor/:timerange', {
        controller: 'graphsCtrl'
    });

    // enable HTML5mode to disable hashbang urls
    $locationProvider.html5Mode(true);
});


/*
https://github.com/pablojim/highcharts-ng
TODO:
  * informację o ładowaniu danych: http://stackoverflow.com/questions/12148276/highcharts-how-to-show-loading-animation-at-set-data
  * przyciski z zakresami danych: godzina, dzień, miesiąc itd
*/
sensmon.controller('graphsCtrl', function ($route, $routeParams, $scope, $http, $timeout) {

  // punkty wykresu
  var chartData = [];

  // potrzebujemy 20ms opóźnienie
  $timeout(function(){
    var nodename = $routeParams.nodename; // nodename
    var sensor = $routeParams.sensor; // sensor
    var timerange = $routeParams.timerange; //timerage
    // stwórz adres url
    // /history/<nodename>/<sensor>/<timerange>
    url = '/history/' + nodename + '/' + sensor + '/' + timerange;
    // pobieram ustawienia nodów aby uzyskać dodatkowe informacje na ich temat
    var getPlotInfo = $http.get('/static/conf/nodemap.json').success(function(data) {
      console.log('Pobrano nodemap.json');
      // format JSON
      $scope.plotinfo = {
          title: data[nodename]['title'],
          sensor: data[nodename]['sensors'][sensor]['desc'],
          timerange: timerange
      };
    });
    // pobieramy nodemap i rysujemy wykres
    // https://groups.google.com/forum/#!topic/angular/l47fnafQzlY
    getPlotInfo.then(function () {
      plot($scope.plotinfo);
    })
  }, 20);


  /* funkcja rysująca wykres
  // params - informacje o wykresie: title, sensor, timerage
  */
  function plot(params) {
    // pobieram dane wykresu wg szablonu /history/<nodename>/<sensor>/<timerange>
    $http.get(url).success(function(data) {
      console.log('Rysuje wykres dla ' + params.title);
      // punkty wykresu
      chartData = data.data;
      // ustawienia wykresu
      Highcharts.setOptions({
        global : {
          useUTC : false
        },
        lang: {
          // polskie tłumaczenie
          // http://stackoverflow.com/questions/7419358/highcharts-datetime-localization
          loading: 'Ładowanie...',
          months: ['Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec', 'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'],
          weekdays: ['Niedziela', 'Poniedziałek', 'Wtorek', 'Środa', 'Czwartek', 'Piątek', 'Sobota'],
          shortMonths: ['Sty', 'Lut', 'Mar', 'Kwi', 'Maj', 'Cze', 'Lip', 'Sie', 'Wrz', 'Paź','Lis', 'Gru'],
          exportButtonTitle: "Export",
          printButtonTitle: "Drukowanie",
          rangeSelectorFrom: "Od",
          rangeSelectorTo: "Do",
          rangeSelectorZoom: "Przybliżenie",
          downloadPNG: 'Pobierz obraz PNG',
          downloadJPEG: 'Pobierz obraz JPEG',
          downloadPDF: 'Pobierz dokument PDF',
          downloadSVG: 'Pobierz obraz SVG',
          thousandsSep: " ",
          decimalPoint: ','
          // resetZoom: "Reset",
          // resetZoomTitle: "Reset,
        }
      });
      $scope.chartConfig = {
        options: {
          chart: {
            zoomType: 'x',
            backgroundColor: 'rgb(238, 238, 238)' // szary
          },
          rangeSelector: {
            enabled: true,
            buttons: [{
              type: 'hour',
              count: 1,
              text: '1h'
            },{
              type: 'day',
              count: 1,
            	text: '1D'
            }, {
              type: 'day',
              count: 2,
            	text: '2D'
            }, {
            	type: 'day',
            	count: 7,
            	text: '1W'
            }, {
            	type: 'month',
            	count: 1,
            	text: '1M'
            }, {
            	type: 'year',
            	count: 1,
            	text: '1Y'
            }, {
            	type: 'all',
            	text: 'All'
            }],
            selected: 4,
            inputEnabled : false
          },
          scrollbar: {
            enabled: true
          },
          navigator: {
            enabled: true
          }
        },
        loading: false, // można uzyć do ładowania danych - poszukać!
        credits: {
          enabled: false
        },
        size: {
          height :"550"
        },
        series: [],
        title: {
          text: params.title
        },
        yAxis: {
          title: {
            text: params.sensor,
            opposite: false,
            //gridLineColor: '#197F07',
            minorTickInterval: 'auto'
          }
        },
        //xAxis: {
          //ridLineWidth: 1,
          //gridZIndex: 4,
          //gridLineColor: '#eee',
        //},
        useHighStocks: true
      }
      // dodajemy dane do wykresu
      // FIXME: ustawienia serii danych odzielnie
      $scope.chartConfig.series.push({
        type: 'area',
        //marginRight: 130,
        //marginBottom: 25,
        lineWidth: 2,
        data: chartData,
        threshold: 0,
        color: 'green',
        negativeColor: 'blue',
        name: "Odczyt",
        tooltip: {
          valueDecimals: 2
        }
      });
    });
  };
});


sensmon.controller('HeaderController', function ($scope, $location)
{
    $scope.navClass = function (page) {
        var currentRoute = $location.path().substring(1) || '/';
        return page === currentRoute ? 'active' : '';
    };
});
