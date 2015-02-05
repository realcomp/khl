angular.module('Sportomatics')
.controller('PlayerCardIndicatorsController', ['$http', '$scope','$timeout','AmChartsFactory', function($http, $scope, $timeout, AmChartsFactory) {
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
    this.indicators_type = 'graph';
    this.field = 'goals';
    this.club = null;
    this.coach = null;
    this.groupBy = 'month';
    this.data = {};
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
        this.indicators_type = type;
    };

    this.setField = function(field) {
        this.field = field;
        this.list();
    }

    this.setClub = function(club) {
        this.club = club;
        this.list();
    }

    this.setCoach = function(coach) {
        this.coach = coach;
        this.list();
    }
    this.setGraphResults = function(results) {

    }
    //var chart = null;
    $scope.loadChart = function (url, unload) {
        if(unload != null) {
            var toUnload = unload
            console.log(unload);
        }
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

            })
    };
    $scope.setGroupBy = function(groupby){
        self.groupBy = groupby;
        self.list();
    };
    $scope.unload = function(){

    };
    this.list = function(order_by) {
        var params = 'group_by=' + self.groupBy;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data, status, headers) {
                self.locale = headers()['content-language'];
                self.data = data;
                self.loader = false;
                var chart;
                var chartData = [];
                AmChartsFactory.ready().then(function () {
                    // generate some random data first
                    generateChartData();

                    // SERIAL CHART
                    chart = new AmCharts.AmSerialChart();
                    chart.pathToImages = "http://www.amcharts.com/lib/images/";
                    chart.dataProvider = chartData;
                    chart.categoryField = "date";
                    chart.cursorColor = "#DADADA";

                    // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                    chart.addListener("dataUpdated", zoomChart);

                    // AXES
                    // category
                    var categoryAxis = chart.categoryAxis;
                    categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                    categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
                    categoryAxis.minorGridEnabled = true;
                    categoryAxis.axisColor = "#DADADA";
                    categoryAxis.twoLineMode = true;
                    categoryAxis.dateFormats = [{
                        period: 'fff',
                        format: 'JJ:NN:SS'
                    }, {
                        period: 'ss',
                        format: 'JJ:NN:SS'
                    }, {
                        period: 'mm',
                        format: 'JJ:NN'
                    }, {
                        period: 'hh',
                        format: 'JJ:NN'
                    }, {
                        period: 'DD',
                        format: 'DD'
                    }, {
                        period: 'WW',
                        format: 'DD'
                    }, {
                        period: 'MM',
                        format: 'MMM'
                    }, {
                        period: 'YYYY',
                        format: 'YYYY'
                    }];

                    // first value axis (on the left)
                    var valueAxis1 = new AmCharts.ValueAxis();
                    valueAxis1.axisColor = "#408e3a";
                    valueAxis1.axisThickness = 1;
                    valueAxis1.gridAlpha = 0;
                    chart.addValueAxis(valueAxis1);

                    // second value axis (on the right)
                    var valueAxis2 = new AmCharts.ValueAxis();
                    valueAxis2.position = "right"; // this line makes the axis to appear on the right
                    valueAxis2.axisColor = "#FCD202";
                    valueAxis2.gridAlpha = 0;
                    valueAxis2.axisThickness = 2;
                    chart.addValueAxis(valueAxis2);

                    // third value axis (on the left, detached)
                    var valueAxis3 = new AmCharts.ValueAxis();
                    valueAxis3.offset = 50; // this line makes the axis to appear detached from plot area
                    valueAxis3.gridAlpha = 0;
                    valueAxis3.axisColor = "#B0DE09";
                    valueAxis3.axisThickness = 2;
                    chart.addValueAxis(valueAxis3);

                    // GRAPHS
                    // first graph
                    var graph1 = new AmCharts.AmGraph();
                    graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                    graph1.title = self.field;
                    graph1.valueField = "values";
                    graph1.bullet = "round";
                    graph1.hideBulletsCount = 30;
                    graph1.bulletBorderThickness = 1;
                    graph1.lineColor = "#408e3a";
                    graph1.lineThickness = 4;
                    chart.addGraph(graph1);
                    // second graph
                    var graph2 = new AmCharts.AmGraph();
                    graph2.valueAxis = valueAxis2; // we have to indicate which value axis should be used
                    graph2.title = self.field;
                    graph2.valueField = "hits";
                    graph2.bullet = "square";
                    graph2.hideBulletsCount = 30;
                    graph2.bulletBorderThickness = 1;
                    //chart.addGraph(graph2);

                    // third graph
                    var graph3 = new AmCharts.AmGraph();
                    graph3.valueAxis = valueAxis3; // we have to indicate which value axis should be used
                    graph3.valueField = "views";
                    graph3.title = "green line";
                    graph3.bullet = "triangleUp";
                    graph3.hideBulletsCount = 30;
                    graph3.bulletBorderThickness = 1;
                    //chart.addGraph(graph3);

                    // CURSOR
                    var chartCursor = new AmCharts.ChartCursor();
                    chartCursor.cursorAlpha = 0.1;
                    chartCursor.fullWidth = true;
                    chartCursor.cursorColor = "#8ebd5d";
                    chart.addChartCursor(chartCursor);

                    // SCROLLBAR
                    var chartScrollbar = new AmCharts.ChartScrollbar();
                    chart.addChartScrollbar(chartScrollbar);

                    // LEGEND
                    var legend = new AmCharts.AmLegend();
                    legend.marginLeft = 110;
                    legend.useGraphSettings = true;
                    chart.addLegend(legend);

                    // WRITE
                    chart.write("chartdiv");
                    console.log('applied')
                });

                // generate some random data, quite different range

                var dates = self.data.results.map(function(e){
                    if(e['date'] == null){
                        return new Date(e['season']['start_date'].substr(0,4));
                    }
                    return new Date(e['date']);
                });
                var values = self.data.results.map(function(e){ return e[self.field]});
                function generateChartData() {
                    for(var i = 0; i< dates.length; i++){
                        console.log(dates[i])
                        chartData.push({
                            date: dates[i],
                            values: values[i]
                        });
                    }
                }
                // this method is called when chart is first inited as we listen for "dataUpdated" event
                function zoomChart() {
                    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
                    //chart.zoomToIndexes(10, 20);
                }
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