angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http, $location){
        $scope.player_id = $('#player-id').val();
        $scope.clubTeamApi = $('#club-team-api').val();
        $scope.rate_by_param = parseInt($location.search()['rate_by']);
        $scope.is_playing_param = parseInt($location.search()['is_playing']);
        $scope.currentUrl = window.location.href.replace(/(\/)([0-9]+)(\/)/, '/');
        $scope.current_team = false;
        var section = (document.getElementById('section') != null) ? document.getElementById('section').value : null;

        $scope.params = {
            rate_by: $scope.rate_by_param || '',
            is_playing: ''
        };

        $scope.go = function(href){
            var path = href;
            if($scope.rate_by_param) path+= "#?rate_by=" + $scope.rate_by_param;
            window.location.href = path;
        };
        $scope.limit = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8];
        $scope.increaseLimit = function(index){
            $scope.limit[index] += 8;
        };
        $scope.setPlaying = function(value){
            $scope.params['is_playing'] = value;
            $scope.is_playing_param = value;
            $location.search('is_playing', value);
            $scope.getPartners();
        };
        $scope.setRateBy = function(value){
            $scope.params['rate_by'] = value;
            $scope.rate_by_param = value;
            $location.search('rate_by', value);
            $scope.getPartners();
        };
        $scope.setCurrentTeam = function(){
            $scope.current_team = !$scope.current_team;
            $scope.getPartners();
        }
        $scope.getPartners = function(stopPropagation){
            $scope.url = $('#api-player-partners').val();
            if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                $scope.url += '?'+ $.param($scope.params)
            }
            $scope.loaded = false;
            $http.get($scope.url)
                .success(function(data){
                    if($scope.current_team === true){
                        var tempData = [];
                        _.each(data, function(object){
                            object.players = _.filter(object.players, function(player){
                                return _.findWhere($scope.currentTeam, {pk: player.id}) != null
                            })
                        })
                    }
                    $scope.limit = [8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8];
                    $scope.loaded = true;
                    if($scope.params.rate_by){
                        $scope.playersBySeasonTime = data;
                    } else {
                        $scope.playersBySeasonTime = [];
                        $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 0});
                    }
                    $scope.briefPartners = [];
                    if($scope.params.rate_by !== 1){
                        _.each($scope.playersBySeasonCount, function(object){
                            if (object.seasons_count < 4) return;
                            _.each(object.players, function(player){
                                if ($scope.briefPartners.length < 4) {
                                    $scope.briefPartners.push({
                                        seasons_count: object.seasons_count,
                                        player: player
                                    })
                                }
                            })
                        })
                    } else {
                        _.each($scope.playersBySeasonTime, function(object){
                            if (object.seasons_count < 4) return;
                            _.each(object.players, function(player){
                                if ($scope.briefPartners.length < 4) {
                                    $scope.briefPartners.push({
                                        season_title: object.season.title,
                                        player: player
                                    })
                                }
                            })
                        })
                    }
                })
        };
        $scope.getCurrentTeam = function(){
            if($scope.currentTeam != null || section === 'Main') return $scope.getPartners();
            $http.get($scope.clubTeamApi)
                .success(function(data){
                    $scope.currentTeam = data.all_players;
                    $scope.getPartners();
                })
        }

        $scope.getCurrentTeam();

    });
