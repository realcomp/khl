angular.module('Sportomatics').factory('RadarChartFactory', function(ChartFactory, LocaleFactory, $http, $q, $timeout){

    var RadarChart = function(){

        var self = this;

        // Variables:

        this.localeObject = LocaleFactory.locale_ru;
        this.playerId = document.getElementById('player-id').value;
        this.playerName = document.getElementById('player-name').value;
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
            this.apiPlayersUrl = value;
        };

        this.setSelectedRadarFields = function(selectedRadarFields){
            if(selectedRadarFields != null)
            this.selectedRadarFields = selectedRadarFields;
        };

        this.getSeasons = function(){
            return this.seasons;
        };

        this.setLocaleObject = function(localeObject){
            this.localeObject = localeObject;
        };

        this.create = function(players, dataBySeason, season, sum) { // function to create radar chart for one or multiple players

            var deferred = $q.defer();

            this.seasons = dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); })
            this.playersInRadarChart = [];
            this.playersRadarChartData = [];
            _.each(this.selectedRadarFields, function(field){
                self.playersRadarChartData.push({
                    field: field.field
                })
            });
            this.playersRadarChartGraphs = [];
            if(players.length > 0) { // multiple players
                if (sum) {
                    var playersRequestArray = [];
                    _.each(players, function (player) {
                        var url = self.apiPlayersUrl + player + '/indicators/?group_by=season';
                        playersRequestArray.push($http.get(url));
                    });
                    $q.all(playersRequestArray).then(function (results) { // we should request all players data
                        self.lastSeason = Math.max.apply(Math, this.dataBySeason.results.map(function (o) {
                            return parseInt(o.season.end_date.substr(0, 4));
                        })).toString();
                        self.playerSeasons = this.dataBySeason.results.map(function (e) {
                            return e.season.end_date.substr(0, 4);
                        });

                        _.each(results, function (result) {
                            var playerSeasonsDataResults = result.data.results;
                            var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                return e.season.end_date.substr(0, 4);
                            });
                            self.playerSeasons = self.playerSeasons.concat(playerSeasons).unique().sort();

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
                            self.playersInRadarChart.push({
                                player: player,
                                playerData: playerDataInSeason
                            });
                        });
                        _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                            radarChartDataCategory['value'] = radarChartDataCategory['value'] / self.playersInRadarChart.length;
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
                        $http.get(url)
                            .success(function (playerSeasonsData) {
                                var playerSeasonsDataResults = playerSeasonsData.results;
                                var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                    return e.season.end_date.substr(0, 4);
                                });
                                var playerDataInSeason = _.filter(playerSeasonsDataResults, function (e) {
                                    return e.season.end_date.indexOf(season) > -1;
                                })[0];
                                self.seasons = self.seasons.concat(playerSeasons).unique().sort();
                                _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                                    if (playerDataInSeason && playerDataInSeason['count']) {
                                        radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                        if(radarChartDataCategory.field === 'shots')
                                            radarChartDataCategory['value' + player] /= 10;
                                    } else {
                                        radarChartDataCategory['value' + player] = 0;
                                    }
                                });
                                $http.get(self.apiPlayersUrl+player)
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
                                            return title + ', ' + self.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                                        };
                                        self.playersInRadarChart.push({
                                            player: player,
                                            playerData: playerDataInSeason
                                        });
                                        self.playersRadarChartGraphs.push(graph);
                                    }).then(function () {
                                        ChartFactory.generateRadarChart(self.playersRadarChartData, self.playersRadarChartGraphs).then(function (chart) {
                                            self.chartRadar = chart;
                                            deferred.resolve(true);
                                        })
                                    });
                            })
                    })
                }
                else { // 1 player
                    var player = players[0];
                    var playerSeasonsData = dataBySeason; //dataBySeason
                    var playerSeasonsDataResults = dataBySeason.results;
                    var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                    var maximums = [];
                    var data = this.playersRadarChartData;
                    var balloonValues = [];
                    _.each(this.playersRadarChartData, function(radarChartDataCategory){
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
                    graph.balloonText = this.playerName + " [[value]]";
                    graph.title = this.playerName;
                    graph.balloonFunction = function(a,b){
                        var value = a.values.value;
                        var title = b.title;
                        if(a.category === 'shots' || a.category === 'shots__avg') value *= 10;
                        return title + ', ' + self.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                    };
                    this.playersInRadarChart.push({
                        player: player,
                        playerData: playerDataInSeason
                    });
                    this.playersRadarChartGraphs.push(graph);
                    console.log(this.playersRadarChartData);
                    ChartFactory.generateRadarChart(this.playersRadarChartData, this.playersRadarChartGraphs).then(function(chart){
                        $timeout(function(){
                            self.chartRadar = chart;
                            self.chartRadar.write('chartdiv2');
                        }, 100);
                        deferred.resolve(true);
                    })
                }
            }

            return deferred.promise;

        }; // createRadar

        this.draw = function(){
            if(this.chartRadar != null)
            this.chartRadar.write('chartdiv2');
        }; // draw

    };

    return {
        PlayerRadarChart: RadarChart
    };

    // End of factory declaration
    
});