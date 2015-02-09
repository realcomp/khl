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
    this.indicatorsType = 'graph';
    this.field = 'count';
    this.fieldName = LocaleFactory.getFieldName(this.field);
    this.club = null;
    this.coach = null;
    this.groupBy = 'season';
    this.data = [];
    this.graphData = {};
    this.chartsCount = 0;

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
        var params = 'group_by=month';
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        $http.get(url + '?' + params)
            .success(function(data) {
                $scope.dataByMonth = data;
                params = 'group_by=season';
                if (self.club !== null) {
                    params += '&club=' + self.club;
                }
                if (self.coach !== null) {
                    params += '&coach=' + self.coach;
                }
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        $scope.dataBySeason = data;
                        self.loader = false;
                    }).then(function(){
                        var data;
                        data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                        var newChartData = updatedChartData($scope.chart, $scope.chartData, data.results, self.field);
                        $scope.chart.dataProvider = newChartData.chartData;
                        $scope.chart.addGraph(newChartData.newGraph);
                        $scope.chart.validateData();
                    })
            })
    };
    $scope.setGroupBy = function(groupby){
        self.groupBy = groupby;
        $scope.onSeason = false;
        self.list();
    };
    $scope.unload = function(){

    };
    $scope.moveToSeason = function(season){
        zoomData.startDate = season.start_date;
        zoomData.endDate = season.end_date;
        $scope.onSeason = true;
        self.groupBy = 'month';
        self.list(true);
    };
    this.list = function(switched) {
        /*var params = 'group_by=' + self.groupBy;
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
                self.fieldName = LocaleFactory.getFieldName(self.field, self.locale);
                self.loader = false;*/
        var data;
        data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                if(switched){
                    var datesArray = data.results.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                $scope.chartData = generateChartData(data.results, self.field);
                ChartFactory.generateSerialChart(data.results, self.field, $scope.chartData).then(function(chart){
                    $scope.chart = chart;
                    $scope.chart.write("chartdiv");
                    $scope.chart.addClassNames = false;
                    if(switched){
                        $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
            //});
    };
    $scope.getPlayerData = function(){
        var group = 'month';
        var params = 'group_by=' + group;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data, status, headers) {
                self.locale = headers()['content-language'];
                self.fieldName = LocaleFactory.getFieldName(self.field, self.locale);
                $scope.dataByMonth = data;
                group = 'season';
                params = 'group_by=' + group;
                if (self.club !== null) {
                    params += '&club=' + self.club;
                }
                if (self.coach !== null) {
                    params += '&coach=' + self.coach;
                }
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        $scope.dataBySeason = data;
                        self.loader = false;
                    }).then(function(){
                        self.list();
                        console.log($scope.dataByMonth);
                        console.log($scope.dataBySeason);
                    })
            })
    };

    $scope.getPlayerData();

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
function generateChartData(data, field) {
    var chartData = [];
    var dates = data.map(function(e){
        if(e['date'] == null){
            return new Date(e['season']['end_date']);
        }
        return new Date(e['date']);
    });
    var values = data.map(function(e){ return e[field]});
    var count = data.map(function(e){ return e['count']});
    for(var i = 0; i< dates.length; i++){
        chartData.push({
            date: dates[i],
            values: values[i],
            count: count[i]
        });
    }
    return chartData;
}
function updatedChartData(chart, initialData, data, field){

    var chartData = initialData;
    console.log(chartData);
    var dates = data.map(function(e){
        if(e['date'] == null){
            return new Date(e['season']['end_date']);
        }
        return new Date(e['date']);
    });
    var values = data.map(function(e){ return e[field]});
    var count = data.map(function(e){ return e['count']});
    _.each(dates, function(date, index){
        var pushed = false;
        _.each(chartData, function(e){
            if(e['date'] === date){
                e['values1'] = values[index];
                e['count1'] = count[index];
                pushed = true;
            }
        });
        if (!pushed) {
            chartData.push({
                date: date,
                values1: values[index],
                count1: count[index]
            });
        }
    });
    console.log(chartData);
    var graph = new AmCharts.AmGraph();
    graph.valueAxis = chart.valueAxes[0]; // we have to indicate which value axis should be used
    graph.title = '926';
    graph.valueField = 'values'+1;
    graph.bullet = "round";
    graph.hideBulletsCount = 30;
    graph.bulletBorderThickness = 1;
    graph.lineColor = '#000000'; //TODO: add more colors
    graph.lineThickness = 4;
    return {
        chartData: chartData,
        newGraph: graph
    };
}