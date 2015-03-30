    angular.module('Sportomatics')
        .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q) {
            //http://www.amcharts.com/lib/images/
            var self = this,
                url = $('#IndicatorsLink').attr('href');
            this.indicatorsType = 'graph';
            this.field = $location.search()['field'] || 'count';
            this.fieldName = LocaleFactory.getFieldName(this.field);
            this.club = parseInt($location.search()['club']) || null;
            this.coach = parseInt($location.search()['coach']) || null;
            this.compare_to = parseInt($location.search()['compare_to']) || null;
            this.groupBy = 'season';
            this.data = [];
            this.graphData = {};
            this.chartsCount = 0;
            this.playerUrl = '';
            this.playerId = document.getElementById('player-id').value;
            this.playerName = document.getElementById('player-name').value;
            $scope.apiPlayersUrl = document.getElementById('api-players-url').value;
            $scope.limited = false; //
            $scope.activeSeason = -1; // all seasons selected by default
            $scope.playersStats = [];
            $scope.radarPlayers = [self.playerId]; // array of players to compare in radar chart
            $scope.playerToCompare = { // last found player to compare with
                id: this.compare_to
            };
            $scope.dataType = 'graph-serial'; // we'll be on serial chart tab by default

            $scope.setDataType = function(type){
                $scope.dataType = type;
                if(type === 'graph-radar'){
                    if($scope.playerToCompare.id){
                        $http.get($scope.apiPlayersUrl+$scope.playerToCompare.id)
                            .success(function(data){
                                $timeout(function(){
                                    $scope.playerToCompare.photo = data.photo;
                                    $scope.playerToCompare.name = data.name + ' ' + data.lastname + ' ( ' + data.club.title + ' )';
                                    $scope.playerToCompare.club = data.club;
                                }, 100)
                            })
                    }
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason).then(function(){});
                }
            };
            $scope.addRadarGraph = function(id){
                if(_.contains($scope.radarPlayers, id)) return;
                $scope.radarPlayers.push(id);
                $scope.createRadar($scope.radarPlayers, $scope.lastSeason).then(function(){});
            };

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

            $scope.removeGraph = function(player){
                if(contains($scope.playersStats, 'id', (parseInt(player.id)).toString())){
                    $scope.playersStats = _.without($scope.playersStats, _.findWhere($scope.playersStats, {id: (parseInt(player.id)).toString()}));
                    $scope.makeChart($scope.activeSeason > -1);
                }
            };
            $scope.$watch('playerToCompare.id', function(newval){
                if(newval){
                    $http.get($scope.apiPlayersUrl+newval)
                        .success(function(data){
                            console.log(data);
                            $scope.playerToCompare.photo = data.photo;
                            $scope.playerToCompare.name = data.name + ' ' + data.lastname + ' ( ' + data.club.title + ' )';
                            $scope.playerToCompare.club = data.club;
                        })
                } else {
                    $scope.playerToCompare = {};
                    $location.search('compare_to', null);
                }
            });
            $scope.addGraph = function(id){
                //$('#chartdiv').empty();
                if(!id) return;
                $location.search('compare_to', id);
                $http.get($scope.apiPlayersUrl+id)
                    .success(function(data){

                        $scope.playerToCompare.photo = data.photo;
                        $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                        $scope.playerToCompare.club = data.club;
                        /*if(contains($scope.playersStats, 'id', (parseInt(id)).toString())){
                         $scope.playersStats = _.without($scope.playersStats, _.findWhere($scope.playersStats, {id: (parseInt(id)).toString()}));
                         return $scope.makeChart($scope.activeSeason > -1);
                         }*/
                        var playerObject = {
                            title: $scope.playerToCompare.name || id,
                            color: $scope.playerToCompare.club.main_color || getRandomColor(),
                            id: id,
                            link: $scope.apiPlayersUrl + id + '/indicators/'
                        };
                        url = playerObject.link;
                        var localUrlMonths = url + '?group_by=month';
                        var localUrlSeasons = url + '?group_by=season';
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
                                        $scope.makeChart($scope.activeSeason > -1);
                                    })
                            })
                    })
            };

            $scope.makeChart = function(switched){ // make column chart from multiple players
                var initialData = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var initialGraph = makeGraph('', $scope.playerObject.title, $scope.playerObject.color, self.field, null, $scope.localeObject);
                var initialChartData = generateChartData(initialData.results, self.field, self.groupBy);
                var newChartGraphs = [initialGraph];
                var newChartData = {};
                _.each($scope.playersStats, function(player, index) {
                    var data = (self.groupBy === 'month') ? player.dataByMonth : player.dataBySeason;
                    newChartData = populateChartData($scope.chart, initialChartData, data.results, self.field, $scope.localeObject, player);
                    var newChartGraph = makeGraph(player.id, player.title, player.color, self.field, null, $scope.localeObject);
                    newChartGraphs.push(newChartGraph);
                });
                if(switched){
                    if(!$scope.playersStats.length) newChartData.data = initialData.results;
                    var datesArray = newChartData.data.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                if(!$scope.playersStats.length) newChartData = initialChartData;
                ChartFactory.generateSerialChart(self.field, newChartData, $scope.localeObject, newChartGraphs).then(function(chart){
                    $scope.chart = chart;
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
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
                        _.each($scope.chart.dataProvider, function(data){
                            _.each($scope.coachData.results, function(coachData){
                                if(new Date(data.date).getFullYear() === new Date(coachData.end_date).getFullYear()){
                                    data.lineColor = "#3498db"
                                }
                            })
                        });
                    }
                    if(self.club){
                        _.each($scope.chart.dataProvider, function(data){
                            _.each($scope.clubData.results, function(clubData){
                                if(new Date(data.date).getFullYear() === new Date(clubData.end_date).getFullYear()){
                                    data.lineColor = "#3498db"
                                }
                            })
                        });
                    }
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';

                    if ($scope.playersStats.length > 0) return $scope.makeChart(switched); //player comparison
                    if ($scope.limited) { //not registered users
                        $scope.chart.chartCursor = null;
                        $scope.chart.chartScrollbar = null;
                        $scope.chart.startDuration = null;
                        for(var i = 0; i < $scope.chart.graphs.length; i ++){
                            $scope.chart.graphs[i].balloonText = '';
                            $scope.chart.graphs[i].visibleInLegend = false;
                        }
                        delete $scope.chart.exportConfig

                    }
                    $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
                    $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); })
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    //if(self.compare_to)  $scope.addGraph(self.compare_to);
                });
            };

            $scope.$watch('lastSeason', function(newval){
                if(newval)
                $scope.createRadar($scope.radarPlayers, newval)
            });

            $scope.getPlayerData = function(){
                $scope.playerObject = {
                    id: self.playerId,
                    title: self.playerName,
                    color: "#408e3a"
                };
                self.loader = true;
                $http.get(url + '?group_by=month')
                    .success(function(data, status, headers) {
                        if(data.is_limited) $scope.limited = true;
                        self.locale = headers()['content-language']; // determine language locale
                        $scope.localeObject = LocaleFactory['locale_'+self.locale]; // set locale object to use in js
                        self.fieldName = $scope.localeObject.fieldNames[self.field].fullName;
                        $scope.dataByMonth = data;
                        $scope.playerObject.dataByMonth = data;
                        $http.get(url + '?group_by=season')
                            .success(function(data, status, headers) {
                                $scope.dataBySeason = data;
                                $scope.playerObject.dataBySeason = data;
                                self.data = data; //for table view
                                self.loader = false;
                            }).then(function(){
                                //$scope.playersStats.push(playerObject);
                                if(self.coach){
                                    $scope.getCoachData();
                                }
                                else if(self.club) {
                                    $scope.getClubData();
                                }
                                else {
                                    self.list();
                                }
                            })
                    })
            };

            $scope.getCoachData = function(){
                if(self.coach == null) return;
                var params = '?group_by=season&coach=' + self.coach;
                self.loader = true;
                $http.get(url + '?' + params)
                .success(function(data) {
                    $scope.coachData = data;
                    self.loader = false;
                    self.list();
                })
            };

            $scope.getClubData = function(){
                if(self.club == null) return;
                var params = '?group_by=season&club=' + self.club;
                self.loader = true;
                $http.get(url + '?' + params)
                    .success(function(data) {
                        $scope.clubData = data;
                        self.loader = false;
                        self.list();
                    })
            };

            $scope.selectedRadarFields = [{ // default radar fields we use
                field: "goals"
            }, {
                field: "points"
            }, {
                field: "assists"
            }, {
                field: "plus_minus"
            }];
            $scope.availableFields = _.toArray(LocaleFactory.locale_ru.fieldNames); // generate available fields
            _.each($scope.availableFields, function(object){
                object.ticked = !!(object.field === 'points' || object.field === 'goals' || object.field === 'assists' || object.field === 'plus_minus');
            });

            $scope.$watch('selectedRadarFields', function(newval){
                if(newval && $scope.lastSeason){
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason)
                }
            }, true);

            $scope.createRadar = function(players, season, sum){ // function to create radar chart for one or multiple players
                $scope.playersInRadarChart = [];
                $scope.playersRadarChartData = [];
                _.each($scope.selectedRadarFields, function(field){
                    $scope.playersRadarChartData.push({
                        field: field.field
                    })
                });
                $scope.playersRadarChartGraphs = [];
                var deferred = $q.defer();
                if(players.length > 0) { // multiple players
                    if (sum) {
                        var playersRequestArray = [];
                        _.each(players, function (player) {
                            var url = $scope.apiPlayersUrl + player + '/indicators/?group_by=season';
                            playersRequestArray.push($http.get(url));
                        });
                        $q.all(playersRequestArray).then(function (results) { // we should request all players data
                            $scope.lastSeason = Math.max.apply(Math, $scope.dataBySeason.results.map(function (o) {
                                return parseInt(o.season.end_date.substr(0, 4));
                            })).toString();
                            $scope.playerSeasons = $scope.dataBySeason.results.map(function (e) {
                                return e.season.end_date.substr(0, 4);
                            });

                            _.each(results, function (result) {
                                var playerSeasonsDataResults = result.data.results;
                                var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                    return e.season.end_date.substr(0, 4);
                                });
                                $scope.playerSeasons = $scope.playerSeasons.concat(playerSeasons).unique().sort();

                                var playerDataInSeason = _.filter(playerSeasonsDataResults, function (e) {
                                    return e.season.end_date.indexOf(season) > -1;
                                })[0];
                                _.each($scope.playersRadarChartData, function (radarChartDataCategory, index) {
                                    if (playerDataInSeason) {
                                        if (radarChartDataCategory['value']) {
                                            radarChartDataCategory['value'] += playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                        }
                                        else {
                                            radarChartDataCategory['value'] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                        }
                                    } else {
                                        radarChartDataCategory['value'] = 0;
                                    }
                                });
                                $scope.playersInRadarChart.push({
                                    player: player,
                                    playerData: playerDataInSeason
                                });
                            });
                            _.each($scope.playersRadarChartData, function (radarChartDataCategory, index) {
                                radarChartDataCategory['value'] = radarChartDataCategory['value'] / $scope.playersInRadarChart.length;
                            });
                            var graph = new AmCharts.AmGraph();
                            graph.valueField = "value";
                            graph.bullet = "round";
                            graph.balloonText = "team [[value]]";
                            $scope.playersRadarChartGraphs.push(graph);
                            ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function (chart) {
                                $scope.chartRadar = chart;
                                $scope.chartRadar.write('chartdiv2');
                                deferred.resolve(true);
                            })
                        });
                    } else if (players.length > 1) {
                        _.each(players, function (player) {
                            var url = $scope.apiPlayersUrl + player + '/indicators/?group_by=season';
                            //$http.get(player)
                            $http.get(url)
                                .success(function (playerSeasonsData) {
                                    var playerSeasonsDataResults = playerSeasonsData.results;
                                    var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                        return e.season.end_date.substr(0, 4);
                                    });
                                    $scope.playerSeasons = $scope.playerSeasons.concat(playerSeasons).unique().sort();

                                    var playerDataInSeason = _.filter(playerSeasonsDataResults, function (e) {
                                        return e.season.end_date.indexOf(season) > -1;
                                    })[0];
                                    _.each($scope.playersRadarChartData, function (radarChartDataCategory, index) {
                                        if (playerDataInSeason && playerDataInSeason['count']) {
                                            radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                            if(radarChartDataCategory.field === 'shots')
                                                radarChartDataCategory['value' + player] /= 10;
                                        } else {
                                            radarChartDataCategory['value' + player] = 0;
                                        }
                                    });
                                    $http.get($scope.apiPlayersUrl+player)
                                        .success(function(playerInfo){
                                            var playerName = playerInfo.name + ' ' + playerInfo.lastname;
                                            var graph = new AmCharts.AmGraph();
                                            graph.valueField = "value" + player;
                                            graph.bullet = "round";
                                            graph.balloonText = playerName + " [[value]]";
                                            graph.title = playerName;
                                            graph.balloonFunction = function(a,b){
                                                var value = a.values.value;
                                                var title = b.title;
                                                if(a.category === 'shots' || a.category === 'shots__avg') value *= 10;
                                                return title + ', ' + $scope.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                                            };
                                            $scope.playersInRadarChart.push({
                                                player: player,
                                                playerData: playerDataInSeason
                                            });
                                            $scope.playersRadarChartGraphs.push(graph);
                                        }).then(function () {
                                            ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function (chart) {
                                                $scope.chartRadar = chart;
                                                $scope.chartRadar.write('chartdiv2');
                                                deferred.resolve(true);
                                            })
                                        });
                                })
                        })
                    }
                    else { // 1 player
                        var player = players[0];
                        var playerSeasonsData = $scope.dataBySeason;
                        var playerSeasonsDataResults = playerSeasonsData.results;
                        var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                        var maximums = [];
                        var data = $scope.playersRadarChartData;
                        var balloonValues = [];
                        _.each($scope.playersRadarChartData, function(radarChartDataCategory){
                            if(playerDataInSeason && playerDataInSeason['count']){
                                radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field];
                                if(radarChartDataCategory.field !== 'shots__avg') radarChartDataCategory['value' + player] /= playerDataInSeason['count'] ;
                                if(radarChartDataCategory.field === 'shots' || radarChartDataCategory.field === 'shots__avg')
                                    radarChartDataCategory['value' + player] /= 10;
                            } else {
                                radarChartDataCategory['value' + player] = 0;
                            }
                        });
                        for(var field in data[0]){
                            maximums.push(Math.max.apply(Math, data.map(function(o){return o[field];})))
                        }
                        var max = Math.max.apply(null, _.filter(maximums, function(value){ return value >= 0;}));
                        var graph = new AmCharts.AmGraph();
                        graph.valueField = "value" + player;
                        graph.bullet = "round";
                        graph.balloonText = self.playerName + " [[value]]";
                        graph.title = self.playerName;
                        graph.balloonFunction = function(a,b){
                            var value = a.values.value;
                            var title = b.title;
                            if(a.category === 'shots' || a.category === 'shots__avg') value *= 10;
                            return title + ', ' + $scope.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                        };
                        $scope.playersInRadarChart.push({
                            player: player,
                            playerData: playerDataInSeason
                        });
                        $scope.playersRadarChartGraphs.push(graph);
                        console.log($scope.playersRadarChartData);
                        ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                            $timeout(function(){
                                $scope.chartRadar = chart;
                                $scope.chartRadar.write('chartdiv2');
                            }, 100);
                            deferred.resolve(true);
                        })
                    }
                }
                return deferred.promise;
            };


            $scope.getPlayerData();
            $scope.sumRadars = function(){
                //$scope.createRadar(['1373', '1634'], '2013', true).then(function(){
                //$scope.createRadar(['1634']);
                //})
            };
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
    Array.prototype.unique = function() {
        var a = this.concat();
        for(var i=0; i<a.length; ++i) {
            for(var j=i+1; j<a.length; ++j) {
                if(a[i] === a[j])
                    a.splice(j--, 1);
            }
        }

        return a;
    };
    function makeRadarGraph(){

    }
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
                var dataObject = {};
                dataObject['date'] = date;
                dataObject['values'+playerObject.id] = values[index];
                dataObject['count'+playerObject.id] = count[index];
                dataObject['percentage'+playerObject.id] = (field === 'count') ? undefined : (count[index] === 0) ? undefined : Math.round(parseFloat(values[index]/realCount[index])*1000)/1000;
                chartData.data.push(dataObject);
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
        graph.title = title;
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
            graph.balloonText = '<span style="text-align: left; float: left">'+localeObject.fieldNames[field].shortName + ': [[values' + id +']]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage'+ id +']]</span>';

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
    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }