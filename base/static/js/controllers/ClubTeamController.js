angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout', 'MapService',
    function($http, $scope, $timeout, MapService) {
        var self = this,
        url = document.getElementById("club-team-api").value,//$('#ClubTeamForm').attr('action'),
        popup = null;
        $scope.type = 'all';
        $scope.cache_players = null;
        $scope.cache_clubs = null;
        $scope.notplaying_players = null;
        $scope.state = 'fio';
        $scope.order_by = 'lastname'
        $scope.season = 19;
        $scope.seasons = [];

        $scope.setOrderBy = function(order_by){
            if($scope.order_by === order_by){
                if ($scope.order_by.indexOf('-') > -1){
                    $scope.order_by = $scope.order_by.replace('-', '');
                } else {
                    $scope.order_by = '-' + $scope.order_by;
                }
            } else {
                $scope.order_by = order_by;
            }
        }

        $scope.setType = function(type){
            $scope.type = type;
            $scope.unMakeTransferArrows();
        };

        $scope.setState = function(state){
            $scope.state = state;
            $scope.getFromCache();
            //if($scope.state = 'is_joined'){
            //    $timeout(function(){
            //        $scope.makeTransferArrows();
            //    }, 500)
            //}
        };

        $scope.playerFilter = function(value){
            if($scope.state === 'coaches') return false;
            return value[$scope.state] != false;
        };

        $scope.go = function(path){
            window.location.href = path;
        };

        $scope.PlayerPartnersPopup = {
            data: null,
            isClubsVisible: true
        };

        $scope.PlayerPartnersPopupShow = function(e, event) {
            var popup = $('.player-partners-popup:hidden'),
            url = $('#PlayerCardLink').attr('href'),
            pk;
            if (popup.length && this.cell_id[0] !== 'trainer') {
                pk = self.getCell(self.players, this.cell_id).pk;
                $scope.PlayerPartnersPopup.data = null;
                $http.get(url.replace(0, pk))
                .success(function(data) {
                    $scope.PlayerPartnersPopup.data = data;
                });
                $('.player-partners-popup:hidden').show(500).offset({
                    left: event.pageX,
                    top: event.pageY
                });
            }
        };

        self.players = {};
        self.clubs = {
            'getLastClub': function() {
                if (this.clubs.length) {
                    return this.clubs[this.clubs.length - 1];
                }
            },
            'clubs': []
        };

        $scope.setSeason = function(season, push) {
            $scope.season = season;
            self.list(push);
        };

        $scope.workWithData = function(data){
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap(data.all_players, 'players');
            var giveCountryCodes = function(player){
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                                player.number = parseInt(player.number);
                                $('#player_'+player.pk+'_flag').addClass(country.code);
                            }
                        })
                    }
                }
            }
            var all_players = data.all_players;
            var players = [];
            _.each(all_players, function(player){
                players.push(player.pk);
            })
            _.each(data.all_players, giveCountryCodes)
            _.each(data.goalkeeper_players, giveCountryCodes)
            _.each(data.offender_players, giveCountryCodes)
            _.each(data.defender_players, giveCountryCodes)
        };

        self.getCell = function(table, cell_id) {
            var group;
            if (table.table && cell_id && Array.isArray(cell_id) && cell_id[1] !== null) {
                group = table.table[cell_id[0]];
                if (group) {
                    return group[cell_id[1]];
                }
            }
        };

        self.isPersonVisible = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            if (cell) {
                switch (self.players.status) {
                    default:
                        return true;
                    case 'joined':
                        return cell.is_joined;
                    case 'left':
                        return cell.is_left;
                    case 'legionnaire':
                        return cell.is_legionnaire;
                    case 'home':
                        return cell.is_home;
                }
            } else {
                return false;
            }
        };

        self.isPersonInCell = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            return cell;
        };

        self.list = function(push) {
            var params = 'season=' + $scope.season;//$('#ClubTeamForm').serialize();
            $scope.loaded = false;
            $http.get(url + '?' + params)
            .success(function(data) {
                if (push){
                    $scope.seasons.push({
                        players: data,
                        season: $scope.season,
                        title: (document.getElementById('season_'+$scope.season) != null ) ? document.getElementById('season_'+$scope.season).value : ''
                    })
                } else {
                    $scope.seasons = [{
                        players: data,
                        season: $scope.season,
                        title: (document.getElementById('season_'+$scope.season) != null ) ? document.getElementById('season_'+$scope.season).value : ''
                    }]
                }
                $scope.players = data;
                $http.get('/static/json/countries-json-ru-codes.json')
                    .success(function(data){
                        $scope.countryCodes = data;
                        $scope.loaded = true;
                    }).then(function(){
                        $scope.workWithData(_.last($scope.seasons).players);
                    });
            });
        };

        this.compare = function(arg) {
            var url = $('#ClubTeamCompareLink').attr('href'),
            club = self.clubs.getLastClub(),
            params, leagues;
            if (club) {
                params = 'source_season=' + club.data.season.pk +
                    '&season=' + club.data.prev_season.pk;
            } else {
                params = 'source_season=' + self.players.data.season.pk +
                    '&season=' + self.players.data.prev_season.pk;
            }
            self.clubs.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                if (data.leagues.length) {
                    var clubRows = [];
                    var clubsInRow = [];
                    var clubs = [];
                    $scope.clubplayers = [];
                    _.each(data.leagues, function(league, index){
                        clubs = clubs.concat(league.clubs);
                        $scope.clubplayers = $scope.clubplayers.concat(league.clubplayers);
                    });
                    _.each(clubs, function(club, index){
                        if(clubsInRow.length < 7){
                            clubsInRow.push(club)
                        }
                        if(index === clubs.length -1 || (index + 1) % 7 === 0){
                            clubRows.push(clubsInRow);
                            clubsInRow = [];
                        }
                    });
                    var clubsObject = {
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs
                        },
                        'league': data.leagues[0],
                        'clubRows': clubRows
                    };
                    self.clubs.clubs.push(clubsObject);
                }
                self.clubs.loader = false;
                if(arg !== false){
                }
            });
        };

        $scope.getFromCache = function() {
            if ($scope.cache_players) {
                $scope.players = $scope.cache_players;
                $scope.clubs = $scope.cache_clubs;
            }
        };

        $scope.makeTransferArrows = function(){
            $scope.getFromCache();
            _.each($scope.clubplayers, function(clubplayer){
                createTransferArrow('#club_'+clubplayer.club, '#player_'+clubplayer.player, clubplayer.pk);
            });
            $( ".player-item" ).each(function() {
                if(!_.findWhere($scope.clubplayers, {player: parseInt($(this).attr('id').split('_')[1]) })){
                    $( this ).addClass("opacity-30");
                } else {
                    var id = $(this).attr('id');
                    $(this).hover(function(){
                        $("canvas").each(function(){
                            if ($(this).attr('player') !== id)
                                $(this).addClass("opacity-10");
                        })
                    }, function(){
                        $("canvas").each(function(){
                            $(this).removeClass("opacity-10");
                        })
                    })
                }
            });
        };
        $scope.unMakeTransferArrows = function(){
            $scope.getFromCache();
            $('canvas').remove();
            $( ".player-item" ).each(function() {
                $( this ).removeClass("opacity-30");
            });
        };

        //this.list(this.compare, false);

        $scope.notPlayingNow = function(callback, callbackArg) {
            $scope.setState('fio');
            $scope.unMakeTransferArrows();
            $scope.players.loader = true;
            if ($scope.notplaying_players) {
                $scope.players = $scope.notplaying_players;
            } else {
                $http.get(url+'?notplaying=1').success(function(data) {
                    $scope.cache_players = $scope.players;
                    $scope.cache_clubs = $scope.clubs;
                    $scope.players = data;
                    $scope.players.data = data;
                    $scope.players.table = {
                        'goalkeeper': data.goalkeeper_players,
                        'defender': data.defender_players,
                        'forward': data.offender_players,
                        'trainer': data.coaches
                    };
                    $scope.notplaying_players = $scope.players;
                });
            }
            $scope.workWithData($scope.players);
            $scope.players.loader = false;
            if (typeof callback === 'function') {
                callback(callbackArg);
            }
        };

        self.list();

        $('.b-tabs-content').visibility({
            once: false,
            observeChanges: true,
            onBottomVisible: function(){
                var newSeason = 1;
                if($scope.seasons.length > 0 && fromSeason($scope.season) !== 1997)
                $scope.setSeason(toSeason(fromSeason($scope.season)-1), true)
            }
        })


    }
]);
