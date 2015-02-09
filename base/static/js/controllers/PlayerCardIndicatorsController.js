angular.module('Sportomatics')
.controller('PlayerCardIndicatorsController', ['$http', '$scope','$timeout','AmChartsFactory','ChartFactory','zoomData','LocaleFactory', function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory) {
    //http://www.amcharts.com/lib/images/
    var self = this,
        url = $('#IndicatorsLink').attr('href');
    var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    var monthNamesRu = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
        "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"];
    var localeRu = {
        'season' : 'Сезон'
    };
    var localeEn = {
        'season' : 'Season'
    };
    this.url = $('#IndicatorsLink').attr('href');
        console.log(this.url)
    this.indicatorsType = 'graph';
    this.field = 'count';
    this.fieldName = LocaleFactory.getFieldName(this.field);
    this.club = null;
    this.coach = null;
    this.groupBy = 'season';
    this.data = [];
    this.graphData = {};
    this.chartsCount = 0;
    function ObjectToGenerate() {
        return {
            bindto: '#chart',
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: function (value) {
                            if (self.groupBy === 'month') return monthNames[value.getMonth()] + ' ' + value.getDate() + ', ' + value.getFullYear();
                            if (self.groupBy === 'season') return 'Сезон ' + (value.getFullYear()-1) + '-' + value.getFullYear();
                            return value;
                        }
                    }
                },
                y: {
                    min: -2,
                    label: self.field
                }
            },
            data: {
                xs: {},
                columns: [],
                colors: {
                },
                type: 'line'
            },
            point: {
                show: false
            },
            size: {
                width: 900
            },
            transition: {
            }, zoom: {
                //enabled: true,
                rescale: true
            }

        }
    }
    this.createC3ArrayAndData = function(array, number, field, name){
        var resultArray = _.map(array, function(e){
                if(e['date'] == null){
                    console.log(new Date(e['season']['start_date'].substr(0, 4)).yyyymmdd('-'))
                    return new Date(e['season']['start_date'].substr(0,4)).yyyymmdd('-');
                }
                return new Date(e['date']).yyyymmdd('-');}
        ).sort(function(a,b){
                return new Date(a.substr(0, 4), a.substr(5, 2)-1, a.substr(8, 2)) - new Date(b.substr(0, 4),b.substr(5, 2)-1, b.substr(8, 2));
            });
        resultArray.unshift('x'+number);
        var resultArrayData = array.map(function(e){
            /*if( Object.prototype.toString.call( $scope.fieldMapping[field] ) === '[object Array]' ) {
             var sum = 0;
             _.each($scope.fieldMapping[field], function(fieldEntry){
             sum += e[fieldEntry];
             })
             return sum;
             } else*/ return e[field]; // wait for multiple players comparison
        });
        resultArrayData.unshift(name);
        return {
            array: resultArray,
            data: resultArrayData
        }
    }
    this.createFieldData = function(field, array, chartsCount){
        var result = [];
        var i = 0;
        //TODO: make this method accept multiple players
        var object = self.createC3ArrayAndData(array, chartsCount, field, 'Player ' + chartsCount);
        result.push(object);
        return result;
    };

    this.setIndicatorsType = function(type) {
        this.indicatorsType = type;
    };

    this.setField = function(field) {
        this.field = field;
        this.fieldName = LocaleFactory.getFieldName(field, self.locale);
        this.list(true);
    };

    this.setClub = function(club) {
        this.club = club;
        this.list();
    };

    this.setCoach = function(coach) {
        this.coach = coach;
        this.list();
    };
    this.setGraphResults = function(results) {

    };
    //var chart = null;
    $scope.addGraph = function (url) {
        var params = 'group_by=' + self.groupBy;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                angular.copy();
                ChartFactory.generateSerialChart(self.data.results, self.field).then(function(chart){
                    chart.write("chartdiv");
                    chart.validateData();
                });
            })
    };
    $scope.setGroupBy = function(groupby){
        self.groupBy = groupby;
        self.list();
    };
    $scope.unload = function(){

    };
    this.list = function(switched) {
        var params = 'group_by=' + self.groupBy;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        //self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data, status, headers) {
                self.locale = headers()['content-language'];
                self.data = data;
                self.loader = false;
                if(switched){
                    var zoomStart = zoomData.startDate;
                    var zoomEnd = zoomData.endDate;
                }
                ChartFactory.generateSerialChart(self.data.results, self.field).then(function(chart){
                    chart.write("chartdiv");
                    chart.addClassNames = false;
                    if(switched){
                        chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
                // generate some random data, quite different range

            });
    };

    this.list();

}])
.factory('AmChartsFactory', function ($q, $rootScope, $document) {
    var deferred = $q.defer();

    AmCharts.ready(function(){
        $rootScope.$apply(deferred.resolve);
    });

    return {
        ready: function () {
            return deferred.promise;
        }
    };
})
    .run(function (AmChartsFactory) {})
Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}