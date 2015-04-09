    angular.module('Sportomatics')
        .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q, RadarChartFactory, ClubChartsFactory, PieChartFactory, HighchartsFactory) {
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
            this.chartsCount = 0;
            this.playerUrl = '';
            this.playerId = document.getElementById('player-id').value;
            this.playerName = document.getElementById('player-name').value;
            this.playerColor = document.getElementById('player-color').value;
            this.playerClubs = document.getElementById('player-clubs');
            this.urlClub = document.getElementById('url-club').value.replace('0/', '');
            $scope.apiPlayersUrl = document.getElementById('api-players-url').value;
            $scope.limited = false; // user is not limited by default
            $scope.activeSeason = -1; // all seasons selected by default
            $scope.playersToCompare = [];
            $scope.radarPlayers = [self.playerId]; // array of players to compare in radar chart
            $scope.playerToCompare = { // last found player to compare with
                id: this.compare_to
            };
            $scope.currentPlayerObject = { // object of current player
                id: self.playerId,
                title: self.playerName,
                color: self.playerColor ? self.playerColor : "#408e3a"
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
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason);//.then(function(){});
                }
            };

            $scope.addRadarGraph = function(id){
                if(_.contains($scope.radarPlayers, id)) return;
                $scope.radarPlayers.push(id);
                $scope.createRadar($scope.radarPlayers, $scope.lastSeason);//.then(function(){});
            };

            this.setField = function(field) {
                $location.search('field', field);
                this.field = field;
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
                if(contains($scope.playersToCompare, 'id', (parseInt(player.id)).toString())){
                    $scope.playersToCompare = _.without($scope.playersToCompare, _.findWhere($scope.playersToCompare, {id: (parseInt(player.id)).toString()}));
                    $scope.makeChart($scope.activeSeason > -1);
                }
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

            $scope.addGraph = function(id){
                //$('#chartdiv').empty();
                if(!id) return;
                $location.search('compare_to', id);
                $http.get($scope.apiPlayersUrl+id)
                    .success(function(data){
                        $scope.playerToCompare.photo = data.photo;
                        $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                        $scope.playerToCompare.club = data.club;
                        /*if(contains($scope.playersToCompare, 'id', (parseInt(id)).toString())){
                         $scope.playersToCompare = _.without($scope.playersToCompare, _.findWhere($scope.playersToCompare, {id: (parseInt(id)).toString()}));
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
                                        $scope.playersToCompare.push(playerObject);
                                        $scope.makeChart($scope.activeSeason > -1);
                                    })
                            })
                    })
            };

            $scope.makeChart = function(switched){ // make column chart with multiple players
                var initialData = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason; // initial player data
                var initialGraph = makeGraph('', $scope.currentPlayerObject.title, $scope.currentPlayerObject.color, self.field, null, $scope.localeObject); // initial player graph
                var initialChartData = generateChartData(initialData.results, self.field, self.groupBy); // chart data generated with initial player
                var newChartGraphs = [initialGraph]; // array of graphs we'll use in chart creation
                var newChartData = {}; // object to create chart
                _.each($scope.playersToCompare, function(player, index) {
                    var data = (self.groupBy === 'month') ? player.dataByMonth : player.dataBySeason; // data by season or month same as initial player data
                    newChartData = populateChartData(initialChartData, data.results, self.field, $scope.localeObject, player);
                    var newChartGraph = makeGraph(player.id, player.title, player.color, self.field, null, $scope.localeObject);
                    newChartGraphs.push(newChartGraph);
                });
                if(switched){
                    if($scope.playersToCompare.length === 0) newChartData.data = initialData.results;
                    var datesArray = newChartData.data.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                if(!$scope.playersToCompare.length) newChartData = initialChartData;
                ChartFactory.generateSerialChart(self.field, newChartData, $scope.localeObject, newChartGraphs).then(function(chart){
                    $scope.chart = chart;
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

            };

            $scope.moveToSeason = function(season, index){
                if((self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
                /*$scope.getPlayerDataByMonth().then(function(){
                    zoomData.startDate = season.start_date;
                    zoomData.endDate = season.end_date;
                    $scope.onSeason = true;
                    self.groupBy = 'month';
                    self.data = $scope.dataByMonth;
                    self.list(true);

                })*/
                var chart = $('#chartdiv').highcharts();
                if(chart.drilldownLevels)
                if (chart.drilldownLevels.length > 0) {
                    chart.drillUp();
                    if(index === -1 || $scope.activeSeason === index) return;
                }
                $scope.activeSeason = index;
                chart.series[0].points[index].firePointEvent('click',  {ctrlKey: true});
            };

            this.list = function(switched) {
                if($('.club-id').length !== 0) {
                    return this.listClubs(switched);
                }
                var data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var datesArray = (self.groupBy === 'month') ? data.results.map(function(e){ return new Date(e['date']) }) : data.results.map(function(e){ return new Date(e['season']['end_date']) });
                var min = Math.min.apply(null, datesArray);
                var max = Math.max.apply(null, datesArray);
                if(switched){
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }


                var drilldownSeries = [];



                console.log(newPlayerIndicatorsData)
                var versions = _.groupBy($scope.dataByMonth.results, function(result){
                    if(result.season)
                    return result.season.end_date;
                })
                console.log('versions', versions);
                for(var key in versions){
                    if(versions.hasOwnProperty(key)){
                        drilldownSeries.push({
                            name: $scope.localeObject.fieldNames[self.field].fullName,
                            id: key,
                            data: versions[key].map(function(el){
                                return {
                                    x: new Date(el.date).getTime(),
                                    y: parseFloat(el[self.field])
                                }
                            })
                        })
                    }
                }
                console.log(drilldownSeries)
                var newPlayerIndicatorsData = [{
                    name: $scope.localeObject.fieldNames[self.field].fullName,
                    data: data.results.map(function(el){
                        return {
                            x: new Date(el.season.end_date.split('-')).getTime(),
                            y: parseFloat(el[self.field]),
                            drilldown: el.season.end_date
                        }
                    }),
                    color: $scope.currentPlayerObject.color
                }]
                console.log(newPlayerIndicatorsData)
                self.loader = false;
                var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart('chartdiv', newPlayerIndicatorsData, self.field, drilldownSeries);
                playerIndicatorsChart.setLocaleObject($scope.localeObject)
                playerIndicatorsChart.draw();
                /*$('.season-button').click(function () {
                    var chart = $('#chartdiv').highcharts();
                    console.log(chart)
                    chart.series[0].points[0].firePointEvent('click', {ctrlKey: true});
                });*/
                //document.getElementById('chartdiv').style.marginLeft = '-15px'

                $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
                $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });


                /*$scope.chartData = generateChartData(data.results, self.field, self.groupBy);
                ChartFactory.generateSerialChart(self.field, $scope.chartData, $scope.localeObject, null, $scope.currentPlayerObject).then(function(chart){
                    $scope.chart = chart;

                    if(self.coach){
                        _.each($scope.chart.dataProvider, function(data){
                            if($scope.activeSeason !== -1) data.lineColor = self.playerColor ? self.playerColor : "#408e3a";
                            else
                            _.each($scope.coachData.results, function(coachData){
                                if(new Date(data.date).getFullYear() === new Date(coachData.season.end_date).getFullYear()){
                                    data.lineColor = "#699c97"
                                }
                            })
                        });
                    }
                    if(self.club){
                        console.log($scope.chart.graphs);
                        _.each($scope.chart.dataProvider, function(data){
                            if($scope.activeSeason !== -1) data.lineColor = self.playerColor ? self.playerColor : "#408e3a";
                            else
                            _.each($scope.clubData.results, function(clubData){
                                if(new Date(data.date).getFullYear() === new Date(clubData.season.end_date).getFullYear()){
                                    data.lineColor = "#699c97"
                                }
                            })
                        });
                    }

                    if ($scope.playersToCompare.length > 0) return $scope.makeChart(switched); //player comparison
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
                    $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    //if(self.compare_to)  $scope.addGraph(self.compare_to);
                });*/


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
                                return [new Date(clubResult.season.end_date.split('-')).getTime(), parseFloat(clubResult[self.field])]
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

            $scope.$watch('lastSeason', function(newval){
                if(newval)
                $scope.createRadar($scope.radarPlayers, newval)
            });

            $scope.getPlayerData = function(){
                self.loader = true;
                $http.get(url + '?group_by=season')
                    .success(function(data, status, headers) {
                        if(data.is_limited) $scope.limited = true;
                        self.locale = headers()['content-language']; // determine language locale
                        $scope.localeObject = LocaleFactory['locale_'+self.locale]; // set locale object to use in js
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
                            $scope.getPlayerDataByMonth().then(function(){
                                self.list();
                            })
                        }
                    })
            };

            $scope.getPlayerDataByMonth = function(){
                var deferred = $q.defer();
                if($scope.dataByMonth != null) deferred.resolve(true)
                else{
                    self.loader = true;
                    $http.get(url + '?group_by=month')
                        .success(function(data){
                            self.loader = false;
                            $scope.dataByMonth = data;
                            $scope.currentPlayerObject.dataByMonth = data;
                            deferred.resolve(true);
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

            $scope.$watch('selectedRadarFields', function(newval){
                if(newval && $scope.lastSeason){
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason, null, $scope.selectedRadarFields)
                }
            }, true);

            $scope.createRadar = function(players, season, sum, selectedRadarFields){ // function to create radar chart for one or multiple players
                $scope.RadarChart = new RadarChartFactory.PlayerRadarChart();
                $scope.RadarChart.setSelectedRadarFields(selectedRadarFields);
                $scope.RadarChart.create(players, $scope.dataBySeason, season, sum).then(function(){
                    $scope.playerSeasons = $scope.RadarChart.seasons;
                    $scope.RadarChart.draw();
                });
            };

            $scope.getPlayerData();
        })

    var KHL_NEWEST_FIELDS = ['shots', 'pis__avg', 'shots__avg', 'faceoff', 'winfaceoff', 'winfaceoff_p__avg', 'gamingtime__avg', 'change_count__avg'];
    var AVERAGE_AVAILABLE_FIELDS = ['goals', 'assists', 'points', 'plus_minus', 'penalty_time'];

    function generateChartData(data, field, groupBy) {
        var chartData = {};
        chartData.groupBy = groupBy;
        chartData.data = [];
        var dates = data.map(function(e){
            return (e['date'] != null) ? new Date(e['date']) : new Date(e['season']['end_date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        for(var i = 0; i< dates.length; i++){
            if(!(_.contains(KHL_NEWEST_FIELDS, field) && dates[i].getFullYear() <= 2008))
                chartData.data.push({
                    date: dates[i],
                    values: values[i],
                    count: count[i],
                    percentage: (field === 'count') ? undefined : (count[i] === 0) ? undefined : Math.round(parseFloat(values[i]/realCount[i])*1000)/1000
                });
        }
        return chartData;
    }

    function generateClubsChartGraph(data, field, groupBy){
        var chartData = {};
        chartData.groupBy = groupBy;
        chartData.data = [];
        var dates = data.map(function(e){
            return (e['date'] != null) ? new Date(e['date']) : new Date(e['season']['end_date']);
        });
        return chartData;
    }

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

    function populateChartData(initialData, data, field, localeObject, playerObject){
        var chartData = initialData;
        var dates = data.map(function(e){
            return (e['date'] != null) ? new Date(e['date']) : new Date(e['season']['end_date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        _.each(dates, function(date, index){
            if(!(_.contains(KHL_NEWEST_FIELDS, field) && date.getFullYear() <= 2008)){
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

    function getParameterByName(string, name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(string);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
    }


    function mergeJSON(source1,source2){
        var mergedJSON = source2;
        for (var attrname in source1) {
            if(mergedJSON.hasOwnProperty(attrname)) {
                if ( source1[attrname]!=null && source1[attrname].constructor==Object ) {
                    mergedJSON[attrname] = mergeJSON(source1[attrname], mergedJSON[attrname]);
                }
            } else {
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
        if(_.contains(AVERAGE_AVAILABLE_FIELDS, field))
        graph.balloonText = '<span class="graph-span">'+localeObject.fieldNames[field].shortName + ': [[values' + id +']]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage'+ id +']]</span>';

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