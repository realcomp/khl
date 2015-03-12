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
            $scope.playersStats = [];

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
            $scope.addGraph = function(url, local){
                //TODO: make production version
                var players = [
                    {
                        title: 'Горохов Илья',
                        color: "#FF3232",
                        id: '1',
                        link: '/static/json/gorohov'
                    },
                    {
                        title: 'Сергей Соин',
                        color: "#3232FF",
                        id: '2',
                        link: '/static/json/soin'
                    }
                ];
                if(contains($scope.playersStats, 'id', (parseInt(local)+1).toString())){
                    $scope.playersStats = _.without($scope.playersStats, _.findWhere($scope.playersStats, {id: (parseInt(local)+1).toString()}));
                    return $scope.makeChart($scope.activeSeason > -1);
                }
                var playerObject = players[local];
                url = playerObject.link;
                var localUrlMonths = url + '_months.json';
                var localUrlSeasons = url + '_seasons.json';
                    self.loader = true;
                    $http.get(localUrlMonths)
                        .success(function(data){
                            playerObject.dataByMonth = data;
                        }).then(function(){
                            $http.get(localUrlSeasons)
                                .success(function(data){
                                    playerObject.dataBySeason = data;
                                    self.loader = false;
                                }).then(function(){
                                    $scope.playersStats.push(playerObject);
                                    /*var data = (self.groupBy === 'month') ?  playerObject.dataByMonth : playerObject.dataBySeason;
                                    var newChartData = populateChartData($scope.chart, $scope.chartData, data.results, self.field, $scope.localeObject, playerObject);
                                    var newGraph = makeGraph(playerObject.id, playerObject.title, playerObject.color, self.field, $scope.chart.valueAxes[0], $scope.localeObject);
                                    //var newChartDataByMonth = populateChartData($scope.chart, $scope.chartData, newPlayer.dataByMonth.results, self.field, $scope.localeObject, playerObject);
                                    //var newChartDataBySeason = populateChartData($scope.chart, $scope.chartData, newPlayer.dataBySeason.results, self.field, $scope.localeObject, playerObject);
                                    $scope.latestData = newChartData.data;
                                    $scope.chart.dataProvider = newChartData.data;
                                    $scope.chart.addGraph(newGraph);
                                    //$scope.chart.validateData();
                                    $scope.chart.write("chartdiv");*/
                                    $scope.makeChart($scope.activeSeason > -1);
                                })
                        })
            };

            $scope.makeChart = function(switched){

                var initialData = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var initialGraph = makeGraph('', $scope.playerObject.title, $scope.playerObject.color, self.field, null, $scope.localeObject);
                var initialChartData = generateChartData(initialData.results, self.field, self.groupBy);
                var newChartGraphs = [];
                var newChartData = {};
                newChartGraphs.push(initialGraph);

                _.each($scope.playersStats, function(player, index) {
                    var data = (self.groupBy === 'month') ? player.dataByMonth : player.dataBySeason;
                    newChartData = populateChartData($scope.chart, initialChartData, data.results, self.field, $scope.localeObject, player);
                    var newChartGraph = makeGraph(player.id, player.title, player.color, self.field, null, $scope.localeObject);
                    //$scope.latestData = newChartData.chartData.data;
                    newChartGraphs.push(newChartGraph);
                });
                if(!$scope.playersStats.length) newChartData.data = initialData.results;
                var datesArray = newChartData.data.map(function(e){ return new Date(e['date']) });
                var min = Math.min.apply(null, datesArray);
                var max = Math.max.apply(null, datesArray);
                if(switched){
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                if(self.groupBy === 'season'){
                    $scope.seasons = newChartData;
                    console.log($scope.seasons);
                }
                if(!$scope.playersStats.length) newChartData = initialChartData;
                ChartFactory.generateSerialChart(self.field, newChartData, $scope.localeObject, newChartGraphs).then(function(chart){
                    $scope.chart = chart;
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';
                    console.log($scope.chart.dataProvider);
                    $scope.chart.write("chartdiv");
                    //$scope.chart.addClassNames = false;
                    if(switched){
                        $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
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
                var data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
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
                    if ($scope.playersStats.length > 0) return $scope.makeChart(switched);
                    $scope.chart.write("chartdiv");
                    //$scope.chart.addClassNames = false;
                    if(switched){
                        $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
            };
            $scope.getPlayerData = function(){
                $scope.playerObject = {
                    id: $('#player-id').val(),
                    title: 'Player' + $('#player-id').val(),
                    color: "#408e3a"
                };
                var group = 'month';
                var params = 'group_by=' + group;
                self.loader = true;
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        self.locale = headers()['content-language'];
                        $scope.localeObject = LocaleFactory['locale_'+self.locale];
                        self.fieldName = $scope.localeObject.fieldNames[self.field].fullName;
                        $scope.dataByMonth = data;
                        $scope.playerObject.dataByMonth = data;
                        group = 'season';
                        params = 'group_by=' + group;
                        $http.get(url + '?' + params)
                            .success(function(data, status, headers) {
                                $scope.dataBySeason = data;
                                $scope.playerObject.dataBySeason = data;
                                self.data = data; //for table view
                                self.loader = false;
                            }).then(function(){
                                //$scope.playersStats.push(playerObject);
                                self.list();
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
    function populateChartData(chart, initialData, data, field, localeObject, playerObject){
        var chartData = initialData;
        var dates = data.map(function(e){
            if(e['date'] == null){
                return new Date(e['season']['end_date']);
            }
            return new Date(e['date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        _.each(dates, function(date, index){
            if(!((field === 'shots' || field === 'pis__avg' || field === 'shots__avg' || field === 'faceoff' || field === 'winfaceoff' || field === 'winfaceoff_p__avg' || field === 'gamingtime__avg' || field === 'change_count__avg')
                && (date.getFullYear() <= 2008))){
                if(playerObject.id === '1'){
                    chartData.data.push({
                        date: date,
                        values1: values[index],
                        count1: count[index],
                        percentage1: (field === 'count') ? undefined : (count[index] === 0) ? undefined : Math.round(parseFloat(values[index]/realCount[index])*1000)/1000
                    });
                } else if(playerObject.id === '2'){
                    chartData.data.push({
                        date: date,
                        values2: values[index],
                        count2: count[index],
                        percentage2: (field === 'count') ? undefined : (count[index] === 0) ? undefined : Math.round(parseFloat(values[index]/realCount[index])*1000)/1000
                    });
                }
            }
        });
        var a = _.map(_.toArray(_.groupBy(chartData.data, 'date')), function(e){
            var object = {};
            //if(e.length < 2) return null; //в случае если нужно будет сделать только общие сезоны
            _.each(e, function(dateObject){
                object = mergeJSON(object, dateObject);
            });
            object.date = new Date(object.date);
            return object;
        });
        chartData.data = _.without(_.sortBy(_.toArray(a), 'date'), null);

        return chartData;
    }
    function getArrayElementIndex(array, field, value){
        _.each(array, function(element, index){
            if(element[field].toString() === value.toString()){
                return index;
            }
        });
        return null;
    }
    function mergeJSON(source1,source2){
        /*
         * Properties from the Souce1 object will be copied to Source2 Object.
         * Note: This method will return a new merged object, Source1 and Source2 original values will not be replaced.
         * */
        var mergedJSON = source2;// Copying Source2 to a new Object

        for (var attrname in source1) {
            if(mergedJSON.hasOwnProperty(attrname)) {
                if ( source1[attrname]!=null && source1[attrname].constructor==Object ) {
                    /*
                     * Recursive call if the property is an object,
                     * Iterate the object and set all properties of the inner object.
                     */
                    mergedJSON[attrname] = mergeJSON(source1[attrname], mergedJSON[attrname]);
                }
            } else {//else copy the property from source1
                mergedJSON[attrname] = source1[attrname];

            }
        }

        return mergedJSON;
    }
    function makeGraph(id, title, color, field, valueAxis, localeObject){
        console.log(id, title, color, field);
        var graph = new AmCharts.AmGraph();
        graph.id = "gl"+id;
        graph.valueAxis = valueAxis; // we have to indicate which value axis should be used
        graph.title = title + ' ' + field;
        graph.valueField = "values" + id;
        graph.bullet = "none";
        graph.hideBulletsCount = 30;
        graph.bulletBorderThickness = 1;
        graph.lineColor = color;
        graph.fillColors = color;
        graph.fillAlphas = 1;
        graph.lineThickness = 0;
        graph.type = 'column';
        if(field === 'goals' || field === 'assists' || field === 'points' || field === 'plus_minus' || field === 'penalty_time' )
        graph.balloonText = '<span style="text-align: left; float: left">'+localeObject.fieldNames[field].shortName + ': [[values2]]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage2]]</span>';

        return graph;
    }
    function contains(array, field, value){
        for(var i = 0; i < array.length; i++) {
            if (array[i][field] === value) {
                return true;
            }
        }
        return false;
    }