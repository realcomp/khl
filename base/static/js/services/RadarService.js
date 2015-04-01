angular.module('Sportomatics').service('RadarService', function(ChartFactory, LocaleFactory){
    // TODO: make not singleton
    var self = this;

    // Variables:

    this.apiPlayersUrl = document.getElementById('api-players-url').value;

    this.selectedRadarFields = [{ // default radar fields we use
        field: "goals"
    }, {
        field: "points"
    }, {
        field: "assists"
    }, {
        field: "plus_minus"
    }];

    this.availableFields = _.toArray(LocaleFactory.locale_ru.fieldNames); // generate available fields
    _.each(this.availableFields, function(object){
        object.ticked = !!(object.field === 'points' || object.field === 'goals' || object.field === 'assists' || object.field === 'plus_minus');
    });

    // Methods:

    this.setApiPlayersUrl = function(value){
        self.apiPlayersUrl = value;
    }; // this.setApiPlayersUrl

    this.createRadar = function(players, season, sum) { // function to create radar chart for one or multiple players
        self.playersInRadarChart = [];
        self.playersRadarChartData = [];
        _.each(self.selectedRadarFields, function(field){
            self.playersRadarChartData.push({
                field: field.field
            })
        });
        self.playersRadarChartGraphs = [];
        var deferred = $q.defer();
        if(players.length > 0) { // multiple players
            if (sum) {
                var playersRequestArray = [];
                _.each(players, function (player) {
                    var url = self.apiPlayersUrl + player + '/indicators/?group_by=season';
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
                        _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
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
                    _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                        radarChartDataCategory['value'] = radarChartDataCategory['value'] / $scope.playersInRadarChart.length;
                    });
                    var graph = new AmCharts.AmGraph();
                    graph.valueField = "value";
                    graph.bullet = "round";
                    graph.balloonText = "team [[value]]";
                    self.playersRadarChartGraphs.push(graph);
                    ChartFactory.generateRadarChart(self.playersRadarChartData, self.playersRadarChartGraphs).then(function (chart) {
                        self.chartRadar = chart;
                        self.chartRadar.write('chartdiv2');
                        deferred.resolve(true);
                    })
                });
            } else if (players.length > 1) {
                _.each(players, function (player) {
                    var url = self.apiPlayersUrl + player + '/indicators/?group_by=season';
                    //$http.get(player)
                    $http.get(url)
                        .success(function (playerSeasonsData) {
                            var playerSeasonsDataResults = playerSeasonsData.results;
                            var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                return e.season.end_date.substr(0, 4);
                            });
                            self.playerSeasons = $scope.playerSeasons.concat(playerSeasons).unique().sort();

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
    }; // this.createRadar

    // End of service declaration
});