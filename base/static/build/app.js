'use strict';
angular.module('Sportomatics', [])

var next = function($http) {
    return function(isAll) {
        var self = this,
            url = self.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + self.data.count);
        }
        self.loader = true;
        $http.get(url)
            .success(function(data) {
                if (isAll) {
                    self.data = data;
                } else {
                    self.data.next = data.next;
                    self.data.results = self.data.results.concat(data.results);
                }
                self.loader = false;
            });
    };
}

var getCountries = function($http) {
    return function(callback) {
        var self = this,
            url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
                    self.countries = data;
                    if (self.countries.length) { // has countries
                        if (Array.isArray(self.countries_selected) &&
                            self.countries_selected.length === 0) { // array is expected
                            self.countries_selected = [String(self.countries[0].pk)];
                        } else {
                            self.countries_selected = self.countries[0].pk;
                        }
                        if (self.countries[0].league_set.length) { // has leagues
                            if (Array.isArray(self.leagues_selected) &&
                                self.leagues_selected.length === 0) { // array is expected
                                self.leagues_selected = [String(self.countries[0].league_set[0].pk)];
                            } else {
                                self.leagues_selected = self.countries[0].league_set[0].pk;
                            }
                        }
                    }
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
        }
    };
}

var getLeagues = function(countries, countries_selected) {
    var result = [];
    $.each(countries_selected, function() {
        var pk = this;
        $.each(countries, function() {
            if (this.pk == pk) {
                result = result.concat(this.league_set);
            }
        });
    });
    return result;
}
Date.prototype.yyyymmdd = function(delimiter){
    if(delimiter == null) delimiter = '';
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return yyyy + delimiter + (mm[1]?mm:"0"+mm[0]) + delimiter + (dd[1]?dd:"0"+dd[0]);
}
Date.prototype.getWeekNumber = function(){
    var d = new Date(+this);
    d.setHours(0,0,0);
    d.setDate(d.getDate()+4-(d.getDay()||7));
    return Math.ceil((((d-new Date(d.getFullYear(),0,1))/8.64e7)+1)/7);
}
function getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week

    return new Date(y, 0, d);
}
angular.module('Sportomatics')
.value('zoomData', {
    startDate: 'a',
    endDate: 'a'
})
.factory('ChartFactory', ["$q", "$rootScope", "AmChartsFactory", "zoomData", function($q, $rootScope, AmChartsFactory, zoomData){

    return {
        generateSerialChart: function(data, field, graphsCount){
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                // generate some random data first
                var chartData = generateChartData(data, field);

                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = chartData;
                chart.categoryField = "date";
                chart.cursorColor = "#DADADA";
                chart.addClassNames = true;

                // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener("dataUpdated", zoomChart);
                chart.addListener("zoomed", function (chart) {
                    zoomData.startDate = chart.startDate;
                    zoomData.endDate = chart.endDate;
                });
                // AXES
                // category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
                //categoryAxis.minorGridEnabled = true;
                categoryAxis.autoGridCount =  false;
                categoryAxis.gridAlpha = 0.1;
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
                valueAxis1.gridAlpha = 0.1;
                valueAxis1.minimum = -2;
                chart.addValueAxis(valueAxis1);

                // second value axis (on the right)
                var gamesAxis = new AmCharts.ValueAxis();
                gamesAxis.position = "right"; // this line makes the axis to appear on the right
                gamesAxis.axisColor = "#408e3a";
                gamesAxis.gridAlpha = 0;
                gamesAxis.axisThickness = 0;
                gamesAxis.stackType = "regular";
                gamesAxis.maximum = 100;
                chart.addValueAxis(gamesAxis);

                // third value axis (on the left, detached)
                var valueAxis3 = new AmCharts.ValueAxis();
                valueAxis3.offset = 50; // this line makes the axis to appear detached from plot area
                valueAxis3.gridAlpha = 0;
                valueAxis3.axisColor = "#B0DE09";
                valueAxis3.axisThickness = 2;
                chart.addValueAxis(valueAxis3);

                // GRAPHS
                // first graph
                for(var i = 0; i < graphsCount; i ++){
                    var graph = generateGraph(i, data[i]['title'], valueAxis1);
                    chart.addGraph(graph);
                }
                var graph1 = new AmCharts.AmGraph();

                graph1.id = "g2";
                graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                graph1.title = field;
                graph1.valueField = "values";
                graph1.bullet = "round";
                graph1.hideBulletsCount = 30;
                graph1.bulletBorderThickness = 1;
                graph1.lineColor = "#408e3a";
                graph1.lineThickness = 4;
                graph1.animationPlayed = true;
                chart.addGraph(graph1);
                // second graph
                var gamesGraph = new AmCharts.AmGraph();
                gamesGraph.valueField = "count";
                gamesGraph.title = "games";
                gamesGraph.type = "step";
                gamesGraph.fillAlphas = 0;
                gamesGraph.lineColor = "#408e3a";
                gamesGraph.alphaField = "alpha";
                gamesGraph.lineThickness = 0;
                gamesGraph.lineAlpha = 0.3;
                gamesGraph.newStack = true;
                gamesGraph.stackable = true;
                gamesGraph.balloonText = '';
                gamesGraph.visibleInLegend = false;
                //if(field !== 'count')
                //chart.addGraph(gamesGraph);

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
                chartCursor.cursorAlpha = 1;
                //chartCursor.fullWidth = true;
                chartCursor.cursorColor = "#8ebd5d";
                chart.addChartCursor(chartCursor);

                // SCROLLBAR
                var chartScrollbar = new AmCharts.ChartScrollbar();
                if(field !== 'count')
                chartScrollbar.graph = gamesGraph;
                chartScrollbar.autoGridCount = true;
                chartScrollbar.color = "#000000";
                chart.addChartScrollbar(chartScrollbar);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);

                deferred.resolve(chart);
            });
            return deferred.promise; //метод возвращает промис и ждет когда выполнится resolve, а он выполнится после полного создания графика
        }
    }
}])
var colors = ["#26A65B", "#CF000F", "#663399", "#F9690E"];
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
            values: values[i]//,
           // count: count[i]
        });
    }
    return chartData;
}
// this method is called when chart is first inited as we listen for "dataUpdated" event
function zoomChart() {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    //chart.zoomToIndexes(10, 20);
}
function generateGraph(i, title, axis){
        var graph = new AmCharts.AmGraph();
        graph.valueAxis = axis; // we have to indicate which value axis should be used
        graph.title = title;
        graph.valueField = 'value'+i;
        graph.bullet = "round";
        graph.hideBulletsCount = 30;
        graph.bulletBorderThickness = 1;
        graph.lineColor = colors[i]; //TODO: add more colors
        graph.lineThickness = 4;
        return graph;
}
function saveZoomParams(endDate, endIndex, endValue, startDate){

}
angular.module('Sportomatics')
    .factory('LocaleFactory', ["$rootScope", function($rootScope){
        return {
            getFieldName: function(field, locale){
                var fieldNames = {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Плюс/Минус'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру'
                    },
                    change_time__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру'
                    }
                };
                var fieldNamesEn = {
                    count: {
                        shortName: 'GP',
                        fullName: 'Games played'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game'
                    },
                    change_time__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game'
                    }
                };
                return (locale === 'en') ? fieldNamesEn[field]['fullName'] : fieldNames[field]['fullName'];
            }
        }

    }])
angular.module('Sportomatics')
.controller('ClubListController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#ClubListForm').attr('action');
    this.data = {};
    this.order_by = '%s_title';
    this.order_by_reversed = false;
    this.loader = false;
    this.countries = {};
    this.countries_selected = [];
    this.leagues_selected = '';

    $scope.setSeason = function(e) {
        // turn missing braces back
        $(e).attr('value', '[' + $(e).val() + ']');
        self.list();
    };

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

    this.setCountry = function() {
        this.leagues_selected = '';
        this.list();
    };

    this.list = function(order_by) {
        var self = this,
            params = $('#ClubListForm').serialize();
        if (order_by) {
            if (self.order_by === order_by) { // same field -> reverse
                self.order_by_reversed = !self.order_by_reversed;
            } else { // other field -> reset
                self.order_by_reversed = false;
            }
            self.order_by = order_by;
        }
        params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by +
        '&league=' + self.leagues_selected;
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.next = next($http);

    this.getCountries();
    this.list();
}])
angular.module('Sportomatics')
.controller('MetricsCompareController', ['$http', '$scope', function($http, $scope) {
    this.graph_type = 'linear';
    this.data = {};
    this.setGraphType = function(type) {
        this.graph_type = type;
    };
}])
angular.module('Sportomatics')
.controller('MetricsPlayersController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#MetricsPlayersForm').attr('action');
    self.data = {};

    this.search = function() {
        var self = this,
            params = $('#MetricsPlayersForm').serialize();
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
            });
    };
    this.search();
}])
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
    $scope.moveToSeason = function(season){
        zoomData.startDate = season.start_date;
        zoomData.endDate = season.end_date;
        self.groupBy = 'month';
        self.list(true);
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
                self.fieldName = LocaleFactory.getFieldName(self.field, self.locale);
                self.loader = false;
                if(switched){
                    var datesArray = data.results.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);

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
.factory('AmChartsFactory', ["$q", "$rootScope", "$document", function ($q, $rootScope, $document) {
    var deferred = $q.defer();

    AmCharts.ready(function(){
        $rootScope.$apply(deferred.resolve);
    });

    return {
        ready: function () {
            return deferred.promise;
        }
    };
}])
    .run(["AmChartsFactory", function (AmChartsFactory) {}])
Array.prototype.contains = function(obj) {
    var i = this.length;
    while (i--) {
        if (this[i] === obj) {
            return true;
        }
    }
    return false;
}
angular.module('Sportomatics')
.controller('PlayersSearchController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#PlayersSearchForm').attr('action'),
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

    this.data = {};
    this.order_by = '[%22%s_lastname%22,%22%s_name%22]';
    this.order_by_reversed = false;
    this.ratedBy = 'clubplayer__season_id__count';
    this.isPlaying = true;

    this.loader = false;
    this.countries_selected = [];
    this.leagues_selected = [];

    $scope.moreClubs = function(e) {
        $(e).closest('td').toggleClass('show-more-clubs')
    };

    $scope.lineCheck = function(e) {
        var defaultValue = '[0,1,2,3]',
            isDefault;
        isDefault = $(e).attr('value') === defaultValue;
        if ($(e).is(':checked')) {
            $('input[name="line"]').each(getUnchecker(isDefault, defaultValue));
        }
    };

    $scope.citizenshipCheck = function(e) {
        var isDefault = $(e).attr('name') === 'citizenship' && $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="citizenship"]').each(getUnchecker(isDefault, ''));
            $('input[name="citizenship_other_active"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.contractCheck = function(e) {
        var isDefault = $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="contract"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.showPopup = function(e) {
        var block = $(e).closest('.player-avatar-block');
        block.children('.player-avatar-block-popup').show();
    };

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

    this.search = function(order_by) {
        var params = $('#PlayersSearchForm').serialize();
        if (order_by) {
            if (self.order_by === order_by) { // same field -> reverse
                self.order_by_reversed = !self.order_by_reversed;
            } else { // other field -> reset
                self.order_by_reversed = false;
            }
            self.order_by = order_by;
        }
        params += '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by +
            '&rated_by=' + self.ratedBy;
        if (self.isPlaying) {
            params += '&is_playing=true';
        }
        $.each(self.leagues_selected, function() {
            params += '&league=' + this;
        });
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.setPlaying = function(isPlaying) {
        if (!this.loader) {
            this.isPlaying = isPlaying;
            this.search();
        }
    }

    this.setRatedBy = function(ratedBy) {
        if (!this.loader) {
            this.ratedBy = ratedBy;
            this.search();
        }
    };

    this.next = next($http);

    this.getCountries(this.search);
}])

var next = function($http) {
    return function(isAll) {
        var self = this,
            url = self.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + self.data.count);
        }
        self.loader = true;
        $http.get(url)
            .success(function(data) {
                if (isAll) {
                    self.data = data;
                } else {
                    self.data.next = data.next;
                    self.data.results = self.data.results.concat(data.results);
                }
                self.loader = false;
            });
    };
}

var getCountries = function($http) {
    return function(callback) {
        var self = this,
            url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
                    self.countries = data;
                    if (self.countries.length) { // has countries
                        if (Array.isArray(self.countries_selected) &&
                            self.countries_selected.length === 0) { // array is expected
                            self.countries_selected = [String(self.countries[0].pk)];
                        } else {
                            self.countries_selected = self.countries[0].pk;
                        }
                        if (self.countries[0].league_set.length) { // has leagues
                            if (Array.isArray(self.leagues_selected) &&
                                self.leagues_selected.length === 0) { // array is expected
                                self.leagues_selected = [String(self.countries[0].league_set[0].pk)];
                            } else {
                                self.leagues_selected = self.countries[0].league_set[0].pk;
                            }
                        }
                    }
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
        }
    };
}

var getLeagues = function(countries, countries_selected) {
    var result = [];
    $.each(countries_selected, function() {
        var pk = this;
        $.each(countries, function() {
            if (this.pk == pk) {
                result = result.concat(this.league_set);
            }
        });
    });
    return result;
}

angular.module('Sportomatics')
.controller('ProfileController', ['$http', '$scope', function($http, $scope) {
    var self = this;

    self.user = {};
    self.csrf_token = null;

    $http.get('/en/accounts/api/profile/')
        .success(function(data) {
            self.user = data;
        });

    $scope.setAvatar = function(files, csrf_token) {
        var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': undefined
                },
                'withCredentials': true,
                'transformRequest': angular.identity
            },
            fd = new FormData();
        fd.append('avatar', files[0]);
        $http.patch('/en/accounts/api/profile/', fd, config)
            .success(function(data) {
                $('#id_avatar').attr('src', data.avatar);
                $('.user-avatar-hex2').css(
                    'background-image', 'url(' + data.avatar + ')');
            })
            .error(function(data) {
                // TODO: handle image upload errors
            });
    };

    this.save = function() {
        var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': this.csrf_token
                }
            };
        // TODO: replace url
        $http.patch('/en/accounts/api/profile/', {
            'fio': self.user.fio,
            'email': self.user.email
        }, config)
            .success(function(data) {
                self.user = data;
            });
    };
}])