angular.module('Sportomatics')
    .controller('RadarController', function($scope, ChartFactory){
        $scope.createRadar = function(players, season, sum){
            $scope.playersInRadarChart = [];
            $scope.playersRadarChartData = [];
            _.each($scope.selectedRadarFields, function(field){
                $scope.playersRadarChartData.push({
                    field: field.field
                })
            });
            $scope.playersRadarChartGraphs = [];
            var deferred = $q.defer();
            if(players.length > 1){ // Multiple players
                if(sum){
                    var playersRequestArray = [];
                    _.each(players, function(player){
                        var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                        playersRequestArray.push($http.get(url));
                    });
                    $q.all(playersRequestArray).then(function(results) {
                        $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
                        $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

                        _.each(results, function(result){
                            var playerSeasonsDataResults = result.data.results;
                            var playerSeasons = playerSeasonsDataResults.map(function(e){ return e.season.end_date.substr(0,4); });
                            $scope.playerSeasons = $scope.playerSeasons.concat(playerSeasons).unique().sort();

                            var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                            _.each($scope.playersRadarChartData, function(radarChartDataCategory, index){
                                if(playerDataInSeason){
                                    if(radarChartDataCategory['value']){
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
                        _.each($scope.playersRadarChartData, function(radarChartDataCategory, index){
                            radarChartDataCategory['value'] = radarChartDataCategory['value'] / $scope.playersInRadarChart.length;
                        });
                        var graph = new AmCharts.AmGraph();
                        graph.valueField = "value";
                        graph.bullet = "round";
                        graph.balloonText = "team [[value]]";
                        $scope.playersRadarChartGraphs.push(graph);
                        ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                            $scope.chartRadar = chart;
                            $scope.chartRadar.write('chartdiv2');
                            deferred.resolve(true);
                        })
                    });


                } else {
                    _.each(players, function(player){
                        var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                        $http.get(url)
                            .success(function(playerSeasonsData){
                                var playerSeasonsDataResults = playerSeasonsData.results;
                                var playerSeasons = playerSeasonsDataResults.map(function(e){ return e.season.end_date.substr(0,4); })
                                $scope.playerSeasons = $scope.playerSeasons.concat(playerSeasons).unique().sort();

                                var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                                console.log(player, playerDataInSeason)
                                //if(playerDataInSeason){
                                _.each($scope.playersRadarChartData, function(radarChartDataCategory){
                                    if(playerDataInSeason){
                                        radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'] ;
                                    } else {
                                        radarChartDataCategory['value' + player] = 0;
                                    }
                                });
                                var graph = new AmCharts.AmGraph();
                                graph.valueField = "value" + player;
                                graph.bullet = "round";
                                graph.balloonText = "player " + player + " [[value]]";
                                $scope.playersInRadarChart.push({
                                    player: player,
                                    playerData: playerDataInSeason
                                });
                                $scope.playersRadarChartGraphs.push(graph);
                                //  }
                            }).then(function(){
                                ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                                    $scope.chartRadar = chart;
                                    $scope.chartRadar.write('chartdiv2');
                                    deferred.resolve(true);
                                })
                            });
                    })
                }
            } else { // 1 player
                var player = players[0];
                var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                $http.get(url)
                    .success(function(playerSeasonsData){
                        var playerSeasonsDataResults = playerSeasonsData.results;
                        var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                        _.each($scope.playersRadarChartData, function(radarChartDataCategory){
                            if(playerDataInSeason && playerDataInSeason['count']){
                                radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'] ;
                            } else {
                                radarChartDataCategory['value' + player] = 0;
                            }
                        });
                        var graph = new AmCharts.AmGraph();
                        graph.valueField = "value" + player;
                        graph.bullet = "round";
                        graph.balloonText = "player " + player + parseInt("[[value]]");
                        graph.balloonFunction = function(a,b){
                            return a.category + ': ' + a.values.value;
                        };
                        $scope.playersInRadarChart.push({
                            player: player,
                            playerData: playerDataInSeason
                        });
                        $scope.playersRadarChartGraphs.push(graph);
                    }).then(function(){
                        ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                            $scope.chartRadar = chart;
                            $scope.chartRadar.write('chartdiv2');
                            deferred.resolve(true);
                        })
                    });
            }
            return deferred.promise;
        };
    });