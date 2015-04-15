angular.module('Sportomatics')
    .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, LocaleFactory, $state, $location, $q, HighchartsFactory) {
        //http://www.amcharts.com/lib/images/
        var self = this;
        var url = $('#IndicatorsLink').attr('href');
        this.field = $location.search()['field'] || 'count';
        this.club = parseInt($location.search()['club']) || null;
        this.coach = parseInt($location.search()['coach']) || null;
        this.compare_to = parseInt($location.search()['compare_to']) || null;
        this.groupBy = 'season';
        this.data = [];
        this.graphData = {};
        this.playerId = document.getElementById('player-id').value;
        this.playerName = document.getElementById('player-name').value;
        this.playerColor = document.getElementById('player-color').value;
        this.playerClubs = document.getElementById('player-clubs');
        this.urlClub = document.getElementById('url-club').value.replace('0/', '');
        $scope.apiPlayersUrl = document.getElementById('api-players-url').value;
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
            color: self.playerColor ? self.playerColor : "#408e3a"
        };
        $scope.dataType = 'graph-serial'; // we'll be on serial chart tab by default

        $scope.setDataType = function(type, preventCreation){
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
                    $scope.createRadar();
                }, 100)
            } else {
                if(preventCreation == null)
                $timeout(function(){
                    $scope.makeChart();
                }, 100)
            }
        };

        $scope.addRadarGraph = function(id, preventCreation){
            if(_.findWhere($scope.radarPlayers, {id: id})) return;
            $http.get($scope.apiPlayersUrl + id)
                .success(function(player){
                    $http.get($scope.apiPlayersUrl + id + '/indicators/?group_by=season')
                        .success(function(data){
                            $scope.radarPlayers.push({
                                id: id,
                                color: player.club.main_color || null,
                                fio: player.fio,
                                dataBySeason: data
                            })
                            if(preventCreation == null)
                            $scope.createRadar();
                            $scope.addGraph(id, true);
                        })
                })
        };

        this.setField = function(field, preventList) {
            $location.search('field', field);
            this.field = field;
            if(preventList == null)
            this.list();
        };

        $scope.setField = function(field, preventList){
            self.setField(field, preventList);
        }

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

        $scope.$watch('playerToCompare.id', function(newval){
            if(newval){
                $http.get($scope.apiPlayersUrl+newval)
                    .success(function(data){
                        $scope.playerToCompare.photo = data.photo;
                        $scope.playerToCompare.name = data.name + ' ' + data.lastname + ' ( ' + data.club.title + ' )';
                        $scope.playerToCompare.club = data.club;
                    })
            } else {
                $scope.playerToCompare = {};
                $location.search('compare_to', null);
            }
        });

        $scope.addGraph = function(id, preventCreation){
            if(!id || _.findWhere($scope.playersToCompare, {id: id})) return;
            $location.search('compare_to', id);
            $http.get($scope.apiPlayersUrl+id)
                .success(function(data){
                    $scope.playerToCompare.photo = data.photo;
                    $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                    $scope.playerToCompare.club = data.club;
                    var playerObject = {
                        title: $scope.playerToCompare.name || id,
                        color: $scope.playerToCompare.club.main_color || getRandomColor(),
                        id: id,
                        link: $scope.apiPlayersUrl + id + '/indicators/'
                    };
                    var url = playerObject.link;
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
                                    $scope.dataBySeason.results = _.sortBy($scope.dataBySeason.results.concat(_.filter(data.results, function(result){
                                        return !_.filter($scope.dataBySeason.results, function(el){
                                            return el.season.end_date === result.season.end_date
                                        }).length
                                    })), function(el){ return new Date(el.season.end_date.split('-'))})
                                    self.loader = false;
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
            console.log('making chart')
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 365;

            var results = [];
            if($scope.activeSeason === -1){ //make chart grouped by seasons
                _.each($scope.playersToCompare, function(playerObject, index){
                    if(index === 0) return;
                    var newPlayerIndicatorsData = {
                        name: playerObject.title,
                        data: playerObject.dataBySeason.results.map(function(el){
                            return {
                                x: new Date(el.season.end_date.split('-')[0]).getTime(),
                                y: parseFloat(el[self.field]),
                                drilldown: el.season.end_date
                            }
                        }),
                        color: playerObject.color,
                        stack: playerObject.id
                    }
                    results.push(newPlayerIndicatorsData);
                    if(self.chart.drilldownLevels && self.chart.drilldownLevels.length > 0) {
                        console.log(self.chart);
                        self.chart.drillUp();
                    }

                    if(!_.findWhere(self.chart.series, {name: newPlayerIndicatorsData.name}))
                    self.chart.addSeries(newPlayerIndicatorsData);
                })
                /*var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart('chartdiv', results, self.field);
                playerIndicatorsChart.setLocaleObject($scope.localeObject)
                playerIndicatorsChart.setContext($scope);
                playerIndicatorsChart.setPeriod(30);
                playerIndicatorsChart.draw();
                self.chart = $('#chartdiv').highcharts();*/
            } else { // make chart on some season
                var results = [];
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
                                y: parseFloat(el[self.field])
                            }
                        }),
                        color: playerObject.color
                    })
                })

                var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart('chartdiv', results, self.field);
                playerIndicatorsChart.setLocaleObject($scope.localeObject)
                playerIndicatorsChart.setContext($scope);
                playerIndicatorsChart.setPeriod(30);
                playerIndicatorsChart.draw();
                self.chart = $('#chartdiv').highcharts();
            }
        };

        $scope.isDisabled = function(season){
            return _.contains(KHL_NEWEST_FIELDS, self.field) && (parseInt(season.end_date.split('-')[0]) < 2009 );
        };

        $scope.setGroupBy = function(groupby){
            self.groupBy = groupby;
            self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
            $scope.onSeason = false;
            self.list();
            $scope.activeSeason = -1;
        };

        $scope.moveToSeason = function(season, index, date){
            if(index !== -1)
            if(_.contains(KHL_NEWEST_FIELDS, self.field) && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
            var chart = $('#chartdiv').highcharts();
            if(index === -1 || $scope.activeSeason === index) {
                $scope.activeSeason = -1;
                self.list();
                return;
            }
            $scope.activeSeason = index;
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
            if($scope.currentPlayerObject.dataByMonth){
                $scope.drilldown = (date != null) ? date : $scope.currentPlayerObject.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                $scope.makeChart()
            } else {
                $scope.getPlayerDataByMonth().then(function(){
                    $scope.drilldown = (date != null) ? date : $scope.currentPlayerObject.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                    $scope.makeChart()
                })
            }
        };

        this.list = function() {

            if($scope.activeSeason !== -1) return $scope.makeChart();

            if($('.club-id').length !== 0) {
                return this.listClubs(switched);
            }

            var newPlayerIndicatorsData = [{
                name: $scope.currentPlayerObject.title,
                data: $scope.initialDataBySeason.results.map(function(el){
                    return {
                        x: new Date(el.season.end_date.split('-')[0]).getTime(),
                        y: parseFloat(el[self.field]),
                        drilldown: el.season.end_date
                    }
                }),
                color: $scope.currentPlayerObject.color,
                stack: 'hi'
            }]

            self.loader = false;
            var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart('chartdiv', newPlayerIndicatorsData, self.field);
            playerIndicatorsChart.setLocaleObject($scope.localeObject)
            playerIndicatorsChart.setContext($scope);
            playerIndicatorsChart.draw();
            self.chart = $('#chartdiv').highcharts();
            if ($scope.playersToCompare.length > 1) {
                if($scope.activeSeason === -1){
                    $scope.makeChart(); //player comparison
                }
            }
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;

            $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

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

        this.listClubs = function(switched){

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
            self.loader = true;
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
                            return [new Date(clubResult.season.end_date.split('-')[0]).getTime(), parseFloat(clubResult[self.field])]
                        }),
                        club: club,
                        color: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? "#699c97" : "#408e3a" ) : (club.main_color.length === 0) ? null : club.main_color,
                        showInLegend: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? true : false ) : null,
                    }
                    newData.push(object)
                })

                if(document.getElementById('isPlayerShort') == null){ //player-clubs page

                    self.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsChart('chartdiv', newData, self.field);
                    playerClubsChart.setLocaleObject($scope.localeObject)
                    playerClubsChart.draw();
                    document.getElementById('chartdiv').style.marginLeft = '-15px'

                } else {
                    console.log(newData)
                    var newDataPie = newData.map(function(el){
                        return {
                            name: el.name,
                            y: _.reduce(el.data, function(pv, cv){ return pv + cv[1] }, 0),
                            pk: el.club.pk,
                            url: self.urlClub + el.club.pk + '?season=' + toSeason(el.club.seasons[0])
                        };
                    })
                    console.log(newDataPie)
                    self.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsPieChart('chartdiv', newDataPie, self.field);
                    playerClubsChart.draw();
                }

            })

        }; //List clubs

        $scope.getPlayerData = function(){
            self.loader = true;
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
                    self.loader = false;
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
                self.loader = true;
                $http.get(url + '?group_by=month')
                    .success(function(data){
                        self.loader = false;
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
            self.loader = true;
            $http.get(url + params)
                .success(function(data) {
                    $scope.coachData = data;
                    self.loader = false;
                    self.list();
                })
        };

        $scope.getClubData = function(){
            if(self.club == null) return self.listClubs();
            var params = '?group_by=season&club=' + self.club;
            self.loader = true;
            $http.get(url + params)
                .success(function(data) {
                    $scope.clubData = data;
                    self.loader = false;
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

        $scope.$watch('selectedRadarFields', function(newval){
            if(newval && $scope.lastSeason && $scope.dataType === 'graph-radar'){
                $scope.createRadar()
            }
        }, true);

        $scope.$watch('lastSeason', function(newval){
            if(newval && $scope.dataType === 'graph-radar'){
                $scope.createRadar()
            }
        });

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
                        color: $scope.currentPlayerObject.color
                    }
                }
            }).filter(function(toFilter){ return toFilter != undefined; });
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });
            $scope.playerStatsSpiderChart = new HighchartsFactory.PlayerStatsSpiderChart('chartdiv2', data, categories, $scope.lastSeason);
            $scope.playerStatsSpiderChart.setContext($scope);
            $scope.playerStatsSpiderChart.setLocaleObject($scope.localeObject);
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
                                pointPlacement: 'on'
                            }
                        }
                    }).filter(function(toFilter){ return toFilter != undefined; });
                    self.spiderChart.addSeries(data[0]);
                    var playerSeasons = playerObject.dataBySeason.results.map(function (e) { return e.season.end_date.substr(0, 4); });
                    $scope.playerSeasons = _.uniq($scope.playerSeasons.concat(playerSeasons)).sort();
                })
            }
        };

        // RUN

        $scope.getPlayerData();
    })

    var KHL_NEWEST_FIELDS = ['shots', 'pis__avg', 'shots__avg', 'faceoff', 'winfaceoff', 'winfaceoff_p__avg', 'gamingtime__avg', 'change_count__avg'];
    var AVERAGE_AVAILABLE_FIELDS = ['goals', 'assists', 'points', 'plus_minus', 'penalty_time'];

    function toSeason(value){
        //TODO заменить
        var seasons = {
            s2002: 1,
            s2003: 2,
            s2001: 3,
            s2004: 4,
            s2000: 5,
            s1999: 6,
            s1998: 7,
            s2005: 8,
            s2006: 9,
            s1997: 10,
            s2007: 11,
            s2008: 12,
            s2009: 13,
            s2010: 14,
            s2011: 15,
            s2012: 16,
            s2013: 17,
            s2014: 18,
            s2015: 19
        }
        return seasons['s'+value];
    }

    function getArrayElementIndex(array, field, value){
        _.each(array, function(element, index){
            if(element[field].toString() === value.toString()){
                return index;
            }
        });
        return null;
    }

    function getParameterByName(string, name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(string);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
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
