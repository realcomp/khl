angular.module('Sportomatics')
    .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, LocaleFactory, $location, $q, HighchartsFactory) {
        //http://www.amcharts.com/lib/images/
        var self = this;
        var url = (document.getElementById('api-player-indicators') != null) ? document.getElementById('api-player-indicators').value : '';
        this.url = url;
        var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart();
        $scope.field = playerIndicatorsChart.getField();
        $scope.setField = playerIndicatorsChart.setField;
        $scope.localeObject = LocaleFactory.selectedLocale;
        this.club = parseInt($location.search()['club']) || null;
        this.coach = parseInt($location.search()['coach']) || null;
        this.compare_to = parseInt($location.search()['compare_to']) || null;
        this.groupBy = 'season';
        this.data = [];
        this.graphData = {};
        this.playerId = (document.getElementById('player-id') != null) ? document.getElementById('player-id').value : '';
        this.playerName = (document.getElementById('player-name') != null) ? document.getElementById('player-name').value : '';
        this.playerPhoto = (document.getElementById('player-photo') != null) ? document.getElementById('player-photo').value : '';
        this.playerColor = (document.getElementById('player-color') != null) ? document.getElementById('player-color').value : '';
        this.playerClubs = document.getElementById('player-clubs');
        this.urlClub = (document.getElementById('url-club') != null) ? document.getElementById('url-club').value.replace('0/', '') : '';
        $scope.apiPlayersUrl = (document.getElementById('api-players-url') != null) ? document.getElementById('api-players-url').value : '';
        $scope.limited = false; // user is not limited by default
        $scope.activeSeason = -1; // all seasons selected by default (index of all seasons is -1)
        $scope.playersToCompare = [];
        $scope.radarPlayers = []; // array of players to compare in radar chart
        $scope.playerToCompare = { // last found player to compare with
            id: this.compare_to
        };
        $scope.currentPlayerObject = { // object of current player
            id: self.playerId,
            title: self.playerName,
            color: self.playerColor ? self.playerColor : "#408e3a",
            photo: self.playerPhoto
        };
        $scope.dataType = 'graph-serial'; // we'll be on serial chart tab by default

        $scope.setParams = function(){
            $('#regularParams').toggleClass('display-none');
            $('#professionalParams').toggleClass('display-none');
            $('.ui.checkbox-regular').checkbox('uncheck');
            $('.ui.checkbox-professional').checkbox('check');
        }

        $scope.setDataType = function(type, event){
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
                $timeout(function(){
                    $('#params').addClass('display-none')
                    $scope.createRadar();
                }, 100)
            } else {
                //if(event.originalEvent != null){
                    $timeout(function(){
                        $('#params').removeClass('display-none')
                        $scope.makeChart();
                    }, 100)
                //}
            }
        };

        $scope.addRadarGraph = function(id, preventCreation){
            if(_.findWhere($scope.radarPlayers, {id: id})) return;
            $http.get($scope.apiPlayersUrl + id)
                .then(function(response){
                    var player = response.data;
                    $http.get($scope.apiPlayersUrl + id + '/indicators/?group_by=season')
                        .success(function(data){
                            $scope.radarPlayers.push({
                                id: id,
                                color: (player.club && player.club.main_color) || CHART_COLORS[$scope.playersToCompare.length-2],
                                fio: player.fio,
                                dataBySeason: data,
                                logo: player.photo
                            })
                            if(preventCreation == null)
                            $scope.createRadar();
                            $scope.addGraph(id, true);
                        })
                }, function(){
                    // player details failed — skip radar for this player
                })
        };

        $scope.$on('field-changed', function(event, preventList){
            console.log(field)
            $location.search('field', field);
            if(preventList == null)
            self.list();
        })

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

        $scope.setSelectedPlayer = function(selectedPlayer){
            if (selectedPlayer == null){
                $location.search('compare_to', null);
                $scope.playerToCompare = {}
            } else {
                $scope.playerToCompare = selectedPlayer.originalObject
            }
        }

        $scope.addGraph = function(id, preventCreation){
            if(!id || _.findWhere($scope.playersToCompare, {id: id})) return;
            $location.search('compare_to', id);
            $http.get($scope.apiPlayersUrl+id)
                .then(function(response){
                    var data = response.data;
                    $scope.playerToCompare.photo = data.photo;
                    $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                    $scope.playerToCompare.club = data.club;
                }, function(){
                    $scope.playerToCompare.name = $scope.playerToCompare.fio || String(id);
                })
                .then(function(){
                    console.log($scope.playerToCompare)
                    var playerObject = {
                        title: $scope.playerToCompare.name || id,
                        color: ($scope.playerToCompare.club && $scope.playerToCompare.club.main_color) || CHART_COLORS[$scope.playersToCompare.length-1],
                        id: id,
                        link: $scope.apiPlayersUrl + id + '/indicators/',
                        logo: $scope.playerToCompare.photo
                    };
                    var url = playerObject.link;
                    $scope.loader = true;
                    $http.get(url + '?group_by=month')
                        .success(function(data){
                            playerObject.dataByMonth = data;
                        }).then(function(){
                            $http.get(url + '?group_by=season')
                                .success(function(data){
                                    playerObject.dataBySeason = data;
                                    $scope.dataBySeason.results = _.sortBy($scope.dataBySeason.results.concat(_.filter(data.results, function(result){
                                        return !_.filter($scope.dataBySeason.results, function(el){
                                            return el.season.end_date === result.season.end_date
                                        }).length
                                    })), function(el){ return new Date(el.season.end_date.split('-'))})
                                    $scope.loader = false;
                                }).then(function(){
                                    $scope.playersToCompare.push(playerObject);
                                    $scope.addRadarGraph(id, true);
                                    if(preventCreation == null)
                                    $scope.makeChart();
                                })
                        })
                })
        };

        $scope.makeChart = function(){ // make column chart with multiple players
            if(self.chart)
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 365;
            var results = [];
            var legendContent = '';
            if($scope.activeSeason === -1){ //make chart grouped by seasons
                _.each($scope.playersToCompare, function(playerObject, index){
                    if(index === 0){
                        var data = playerObject.dataBySeason.results.map(function(el){
                            return {
                                x: new Date(el.season.end_date.split('-')[0]).getTime(),
                                y: parseFloat(el[$scope.field]),
                                drilldown: el.season.end_date
                            }
                        })
                        legendContent += HTML_INDICATORS_LIST_ITEM(_.last(data).y, playerObject.title, playerObject.photo, playerObject.color)
                        return;
                    }
                    var newPlayerIndicatorsData = {
                        name: playerObject.title,
                        data: playerObject.dataBySeason.results.map(function(el){
                            return {
                                x: new Date(el.season.end_date.split('-')[0]).getTime(),
                                y: parseFloat(el[$scope.field]),
                                drilldown: el.season.end_date
                            }
                        }),
                        color: playerObject.color,
                        stack: playerObject.id,
                        logo: playerObject.logo
                    }
                    results.push(newPlayerIndicatorsData);
                    if(!_.findWhere(self.chart.series, {name: newPlayerIndicatorsData.name}))
                    self.chart.addSeries(newPlayerIndicatorsData);
                })
            } else { // make chart on some season
                _.each($scope.playersToCompare, function(playerObject, index){
                    if(playerObject.dataByMonth == null) return;
                    var versions = _.groupBy(playerObject.dataByMonth.results, function(result){
                        if (result.season != null)
                            if(result.season.end_date === $scope.drilldown)
                                return result.season.end_date;
                    })
                    if(versions[$scope.drilldown] != null)
                    results.push({
                        name: playerObject.title,
                        stack: playerObject.id,
                        data: versions[$scope.drilldown].map(function(el){
                            return {
                                x: new Date(el.date).getTime(),
                                y: parseFloat(el[$scope.field])
                            }
                        }),
                        color: playerObject.color,
                        logo: playerObject.logo
                    })
                })

                playerIndicatorsChart.init('chartdiv', results, $scope.field)
                playerIndicatorsChart.setContext($scope);
                playerIndicatorsChart.setPeriod(30);
                playerIndicatorsChart.setHeaderChangeable(true);
                playerIndicatorsChart.draw();
                self.chart = $('#chartdiv').highcharts();
            }
            _.each(results, function(result){
                if(result.data && result.data.length)
                legendContent += HTML_INDICATORS_LIST_ITEM(_.last(result.data).y, result.name, result.logo, result.color)
            })
            $('#legend-header').html($scope.localeObject.fieldNames[$scope.field].fullName + '<br> Сезон ' + (new Date($scope.lastSeason).getFullYear()-1) + '/' + (new Date($scope.lastSeason).getFullYear()).toString().substr(2,4))
            $('#legend-content').html(legendContent)
        };

        $scope.isDisabled = function(season){
            return _.contains(KHL_NEWEST_FIELDS, $scope.field) && (parseInt(season.end_date.split('-')[0]) < 2009 );
        };

        $scope.setGroupBy = function(groupby){
            self.groupBy = groupby;
            self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
            $scope.onSeason = false;
            self.list();
            $scope.activeSeason = -1;
        };

        $scope.moveToSeason = function(season, index, date, fromAnotherChart){
            if(index !== -1 && _.contains(KHL_NEWEST_FIELDS, $scope.field) && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
            var chart = $('#chartdiv').highcharts();
            if(index === -1 || $scope.activeSeason === index && !fromAnotherChart) {
                $scope.activeSeason = -1;
                self.list();
                return;
            }
            $scope.activeSeason = index;
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
            if ($scope.currentPlayerObject.dataByMonth != null){
                $scope.drilldown = (date != null) ? date : $scope.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                $scope.makeChart()
            } else {
                $scope.getPlayerDataByMonth().then(function(){
                    $scope.drilldown = (date != null) ? date : $scope.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                    $scope.makeChart()
                })
            }
        };

        this.list = function() {

            if($scope.selectedClub) return this.listAvergePlayer();
            if($('.club-id').length !== 0 && $('#listClubs').length === 1) return this.listClubs();
            if($('#listClubs').length === 1 && $('.club-id').length === 0) return;

            if($scope.initialDataBySeason == null) return
            if($scope.activeSeason !== -1) return $scope.makeChart();

            console.log($scope.initialDataBySeason)
            var newPlayerIndicatorsData = [{
                name: $scope.currentPlayerObject.title,
                data: $scope.initialDataBySeason.results.map(function(el){
                    return {
                        x: new Date(el.season.end_date.split('-')[0]).getTime(),
                        y: parseFloat(el[$scope.field]),
                        drilldown: el.season.end_date
                    }
                }),
                color: $scope.currentPlayerObject.color,
                stack: 'hi',
                logo: $scope.currentPlayerObject.photo
            }]

            $scope.loader = false;

            playerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData, $scope.field)
            playerIndicatorsChart.setContext($scope);
            playerIndicatorsChart.setPeriod(365);
            playerIndicatorsChart.setHeaderChangeable(true);
            playerIndicatorsChart.draw();
            self.chart = $('#chartdiv').highcharts();
            if ($scope.playersToCompare.length > 1) {
                if($scope.activeSeason === -1){
                    $scope.makeChart(); //player comparison
                }
            }
            //self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;

            $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

            $('#legend-header').html($scope.localeObject.fieldNames[$scope.field].fullName + '<br> Сезон ' + (new Date($scope.lastSeason).getFullYear()-1) + '/' + (new Date($scope.lastSeason).getFullYear()).toString().substr(2,4))
            if ($scope.playersToCompare.length <= 1) {
                var legendContent = ''
                _.each(newPlayerIndicatorsData, function(result){
                    legendContent += HTML_INDICATORS_LIST_ITEM(_.last(result.data).y, result.name, result.logo, result.color)
                })
                $('#legend-content').html(legendContent)
            }

            /*if ($scope.limited) { //not registered users
             $scope.chart.chartCursor = null;
             $scope.chart.chartScrollbar = null;
             $scope.chart.startDuration = null;
             for(var i = 0; i < $scope.chart.graphs.length; i ++){
             $scope.chart.graphs[i].balloonText = '';
             $scope.chart.graphs[i].visibleInLegend = false;
             }
             delete $scope.chart.exportConfig
             }*/

        };

        this.listClubs = function(){

            var queries = [];
            var clubs = [];
            var graphs = [];
            //TODO заменить на обращение к апи
            $('.club-id').each(function(index, value){
                var club = $(value).attr('id').split('_');
                var params = '?group_by=season&club=' + club[1];
                clubs.push({
                    title: club[0],
                    pk: club[1],
                    main_color: club[2]
                });
                queries.push($http.get(url + params))
            });
            $scope.loader = true;
            $q.all(queries).then(function(results, a){
                _.each(results, function(result){
                    _.each(clubs, function(club){
                        if(club.pk === getParameterByName(result.config.url, 'club')){
                            club.seasons = [];
                            club.results = result.data.results;
                            _.each(result.data.results, function(clubResult){
                                club.seasons.push (new Date(clubResult.season.end_date).getFullYear());
                            })
                        }
                    })
                });

                var newData = [];
                _.each(clubs, function(club){
                    var object = {
                        name: club.title,
                        stack: 'season',
                        data: club.results.map(function(clubResult){
                            return [new Date(clubResult.season.end_date.split('-')[0]).getTime(), parseFloat(clubResult[$scope.field])]
                        }),
                        club: club,
                        color: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? "#699c97" : "#408e3a" ) : (club.main_color.length === 0) ? null : club.main_color,
                        showInLegend: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? true : false ) : null,
                    }
                    newData.push(object)
                })

                if(document.getElementById('isPlayerShort') == null){ //player-clubs page

                    $scope.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsChart('chartdiv', newData, $scope.field);
                    playerClubsChart.draw();
                    document.getElementById('chartdiv').style.marginLeft = '-15px'

                } else {
                    var newDataPie = newData.map(function(el){
                        return {
                            name: el.name,
                            y: _.reduce(el.data, function(pv, cv){ return pv + cv[1] }, 0),
                            pk: el.club.pk,
                            url: self.urlClub + el.club.pk + '?season=' + toSeason(el.club.seasons[0])
                        };
                    })
                    $scope.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsPieChart('chartdiv', newDataPie, $scope.field);
                    playerClubsChart.draw();
                }

            })

        }; //List clubs

        $scope.initialPlayerObject = {}
        $scope.getPlayerData = function(){
            $scope.loader = true;
            if($('#clubs-compare').length > 0) return $scope.addAverageClubPlayerData();
            $http.get(url + '?group_by=season')
                .success(function(data, status, headers) {
                    //if(data.is_limited) $scope.limited = true;
                    self.locale = headers()['content-language']; // determine language locale
                    $scope.localeObject = LocaleFactory['locale_'+self.locale]; // set locale object to use in js
                    $scope.initialDataBySeason = {};
                    angular.copy(data, $scope.initialDataBySeason);
                    $scope.dataBySeason = data;
                    $scope.currentPlayerObject.dataBySeason = data;
                    self.data = data; //for table view
                    $scope.loader = false;
                }).then(function(){
                    //$scope.playersToCompare.push(playerObject);
                    if(self.coach){
                        $scope.getCoachData();
                    }
                    else if(self.club) {
                        $scope.getClubData();
                    }
                    else {
                        $scope.playersToCompare.push($scope.currentPlayerObject);
                        self.list();
                    }
                })
        };

        $scope.getPlayerDataByMonth = function(callback){
            var deferred = $q.defer();
            if($scope.dataByMonth != null) deferred.resolve(true)
            else{
                $scope.loader = true;
                $http.get(url + '?group_by=month')
                    .success(function(data){
                        $scope.loader = false;
                        $scope.dataByMonth = data;
                        $scope.currentPlayerObject.dataByMonth = data;
                        deferred.resolve(data);
                    })
            }
            return deferred.promise;
        };

        $scope.getCoachData = function(){
            if(self.coach == null) return;
            var params = '?group_by=season&coach=' + self.coach;
            $scope.loader = true;
            $http.get(url + params)
                .success(function(data) {
                    $scope.coachData = data;
                    $scope.loader = false;
                    self.list();
                })
        };

        $scope.getClubData = function(){
            if(self.club == null) return self.listClubs();
            var params = '?group_by=season&club=' + self.club;
            $scope.loader = true;
            $http.get(url + params)
                .success(function(data) {
                    $scope.clubData = data;
                    $scope.loader = false;
                    self.list();
                })
        };

        $scope.availableFields = _.toArray(LocaleFactory.locale_ru.fieldNames); // generate available fields
        _.each($scope.availableFields, function(object){
            object.ticked = !!(object.field === 'points' || object.field === 'goals' || object.field === 'assists' || object.field === 'plus_minus');
        });

        $scope.selectedRadarFields = [{ // default radar fields we use
            field: "goals"
        }, {
            field: "points"
        }, {
            field: "assists"
        }, {
            field: "plus_minus"
        }];

        /*$scope.$watch('selectedRadarFields', function(newval){
            console.log('dqwdq')
            if(newval && $scope.lastSeason && $scope.dataType === 'graph-radar'){
                $scope.createRadar()
            }
        }, true);*/

        $scope.setLastSeason = function(season){
            $scope.lastSeason = season;
            $scope.createRadar()
        }

        $scope.createRadar = function(){ // function to create radar chart for one or multiple players
            var categories = $scope.selectedRadarFields.map(function(el){ return el['field']; });
            var data = $scope.initialDataBySeason.results.map(function(el){
                if(el.season.end_date.indexOf($scope.lastSeason) > -1){
                    return {
                        name: self.playerName,
                        data: categories.map(function(category){
                            if(category === 'shots') return (parseInt(el[category])/10) / parseInt(el['count']);
                            return parseInt(el[category]) / parseInt(el['count']);
                        }),
                        pointPlacement: 'on',
                        color: $scope.currentPlayerObject.color,
                        logo: $scope.currentPlayerObject.photo
                    }
                }
            }).filter(function(toFilter){ return toFilter != undefined; });
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

            $scope.playerStatsSpiderChart = new HighchartsFactory.PlayerStatsSpiderChart('chartdiv2', data, categories, $scope.lastSeason);
            $scope.playerStatsSpiderChart.setContext($scope);
            $scope.playerStatsSpiderChart.setLocaleObject($scope.localeObject);
            $scope.playerStatsSpiderChart.setHeaderChangeable(true);
            $scope.playerStatsSpiderChart.draw();
            self.spiderChart = $("#chartdiv2").highcharts();
            if($scope.radarPlayers.length > 0){
                _.each($scope.radarPlayers, function(playerObject){
                    var data = playerObject.dataBySeason.results.map(function(el){
                        if(el.season.end_date.indexOf($scope.lastSeason) > -1){
                            return {
                                name: playerObject.fio,
                                data: categories.map(function(category){
                                    if(category === 'shots') return (parseInt(el[category])/10) / parseInt(el['count']);
                                    return parseInt(el[category]) / parseInt(el['count']);
                                }),
                                pointPlacement: 'on',
                                logo: playerObject.logo,
                                color: playerObject.color
                            }
                        }
                    }).filter(function(toFilter){ return toFilter != undefined; });
                    self.spiderChart.addSeries(data[0]);
                    var playerSeasons = playerObject.dataBySeason.results.map(function (e) { return e.season.end_date.substr(0, 4); });
                    $scope.playerSeasons = _.uniq($scope.playerSeasons.concat(playerSeasons)).sort();
                })
            }
            $('#legend-header').html($scope.localeObject.fieldNames[_.last(categories)].fullName)
            var legendContent = ''
            _.each(data, function(result){
                console.log(result)
                legendContent += HTML_INDICATORS_LIST_ITEM(parseFloat(_.last(result.data)).toFixed(3), result.name, result.logo, result.color)
            })
            $('#legend-content').html(legendContent)

        };

        // RUN

        $scope.getPlayerData();
    })


