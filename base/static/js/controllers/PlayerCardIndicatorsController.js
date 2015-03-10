    angular.module('Sportomatics')
        .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q) {
            //http://www.amcharts.com/lib/images/
            var self = this,
                url = $('#IndicatorsLink').attr('href');
            this.url = $('#IndicatorsLink').attr('href');
            this.indicatorsType = 'graph';
            this.field = $location.search()['field'] || 'count';
            this.fieldName = LocaleFactory.getFieldName(this.field);
            this.club = parseInt($location.search()['club']) || null;
            this.coach = parseInt($location.search()['coach']) || null;
            this.groupBy = 'season';
            this.data = [];
            this.graphData = {};
            this.chartsCount = 0;
            $scope.activeSeason = -1;

            this.setIndicatorsType = function(type) {
                this.indicatorsType = type;
                if(type === 'graph') {
                    $timeout(function(){
                        //self.list();
                    }, 100);
                }
                else {
                    this.data = (this.groupBy === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
                }
            };

            this.setField = function(field) {
                this.field = field;
                this.fieldName = LocaleFactory.getFieldName(field, self.locale);
                $location.search('field', field);
                this.list(true);
            };

            this.setClub = function(club) {
                this.club = club;
                $location.search('club', club);
                $scope.getClubData(true);
            };

            this.setCoach = function(coach) {
                this.coach = coach;
                $location.search('coach', coach);
                $scope.getCoachData(true);
            };
            this.setGraphResults = function(results) {

            };
            $scope.animateAgain = function(){
                $scope.chart.animateAgain();
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
            $scope.isDisabled = function(season){
                return (self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 );
            };
            $scope.setGroupBy = function(groupby){
                self.groupBy = groupby;
                self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
                $scope.onSeason = false;
                self.list();
                $scope.activeSeason = -1;
                $timeout(function(){}, 500);
            };
            $scope.moveToSeason = function(season, index){
                if((self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
                zoomData.startDate = season.start_date;
                zoomData.endDate = season.end_date;
                $scope.onSeason = true;
                self.groupBy = 'month';
                self.data = $scope.dataByMonth;
                self.list(true);
                $scope.activeSeason = index;
            };
            this.list = function(switched) {
                var data;
                data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var datesArray = (self.groupBy === 'month') ? data.results.map(function(e){ return new Date(e['date']) }) : data.results.map(function(e){ return new Date(e['season']['end_date']) });
                var min = Math.min.apply(null, datesArray);
                var max = Math.max.apply(null, datesArray);
                if(switched){
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                $scope.chartData = generateChartData(data.results, self.field, self.groupBy);
                ChartFactory.generateSerialChart(self.field, $scope.chartData, $scope.localeObject).then(function(chart){
                    $scope.chart = chart;
                    // WRITE
                    if(self.coach){
                        $scope.chart.guides = [];
                        _.each($scope.coachData.results, function(result){
                            var seasonEnd = new Date(result.season.end_date);
                            var prevSeasonEndString = (parseInt(result.season.end_date.substr(0,4))-1).toString() + result.season.end_date.substr(4);
                            var prevSeasonEnd = new Date(prevSeasonEndString);
                            $scope.chart.guides.push({
                                "fillAlpha" : 0.3,
                                "date" : (prevSeasonEnd.getTime() >= min) ? prevSeasonEnd : new Date(min),
                                "toDate": seasonEnd,
                                "fillColor" : "#3498db",
                                "lineThickness": 0
                            });
                        })
                    }
                    if(self.club){
                        $scope.chart.guides = [];
                        _.each($scope.clubData.results, function(result){
                            var seasonEnd = new Date(result.season.end_date);
                            var prevSeasonEndString = (parseInt(result.season.end_date.substr(0,4))-1).toString() + result.season.end_date.substr(4);
                            var prevSeasonEnd = new Date(prevSeasonEndString);
                            $scope.chart.guides.push({
                                "fillAlpha" : 0.3,
                                "date" : (prevSeasonEnd.getTime() >= min) ? prevSeasonEnd : new Date(min),
                                "toDate": seasonEnd,
                                "fillColor" : "#3498db"
                            });
                        })

                    }
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';
                    $scope.chart.write("chartdiv");
                    //$scope.chart.addClassNames = false;
                    if(switched){
                        $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
            };
            $scope.getPlayerData = function(){
                var group = 'month';
                var params = 'group_by=' + group;
                self.loader = true;
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        self.locale = headers()['content-language'];
                        $scope.localeObject = LocaleFactory['locale_'+self.locale];
                        self.fieldName = $scope.localeObject.fieldNames[self.field].fullName;
                        $scope.dataByMonth = data;
                        group = 'season';
                        params = 'group_by=' + group;
                        $http.get(url + '?' + params)
                            .success(function(data, status, headers) {
                                $scope.dataBySeason = data;
                                self.data = data; //for table view
                                self.loader = false;
                            }).then(function(){
                                self.list();
                                console.log($scope.dataByMonth);
                                console.log($scope.dataBySeason);
                            })
                    })
            };
            $scope.getCoachData = function(){
                var group = 'season';
                var params = 'group_by=' + group;
                if (self.coach !== null) {
                    params += '&coach=' + self.coach;
                    $http.get(url + '?' + params)
                        .success(function(data, status, headers) {
                            $scope.coachData = data;
                        }).then(function(){
                            self.list();
                        })
                }
            };
            $scope.getClubData = function(toList){
                var group = 'season';
                var params = 'group_by=' + group;
                if (self.club !== null) {
                    params += '&club=' + self.club;
                    $http.get(url + '?' + params)
                        .success(function(data, status, headers) {
                            $scope.clubData = data;
                        }).then(function(){
                            self.list();
                        })
                }
            };

            $scope.getPlayerData();
            $scope.getCoachData();
            $scope.getClubData();

        })
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
        .run(function (AmChartsFactory) {});

    Array.prototype.contains = function(obj) {
        var i = this.length;
        while (i--) {
            if (this[i] === obj) {
                return true;
            }
        }
        return false;
    };
    function generateChartData(data, field, groupBy) {
        var chartData = {};
        chartData.groupBy = groupBy;
        chartData.data = [];
        var dates = data.map(function(e){
            if(e['date'] == null){
                return new Date(e['season']['end_date']);
            }
            return new Date(e['date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        for(var i = 0; i< dates.length; i++){
            if(!((field === 'shots' || field === 'pis__avg' || field === 'shots__avg' || field === 'faceoff' || field === 'winfaceoff' || field === 'winfaceoff_p__avg' || field === 'gamingtime__avg' || field === 'change_count__avg')
                && (dates[i].getFullYear() <= 2008)))
                chartData.data.push({
                    date: dates[i],
                    values: values[i],
                    count: count[i],
                    percentage: (field === 'count') ? undefined : (count[i] === 0) ? undefined : Math.round(parseFloat(values[i]/realCount[i])*1000)/1000
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
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
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