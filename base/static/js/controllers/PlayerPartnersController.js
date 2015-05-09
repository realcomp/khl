angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http, $location){
        $scope.player_id = $('#player-id').val();
        $scope.rate_by_param = parseInt($location.search()['rate_by']);
        $scope.is_playing_param = parseInt($location.search()['is_playing']);
        $scope.currentUrl = window.location.href.replace(/(\/)([0-9]+)(\/)/, '/');

        $scope.params = {
            rate_by: $scope.rate_by_param || '',
            is_playing: ''
        };

        $scope.go = function(href){
            var path = href;
            if($scope.rate_by_param) path+= "#?rate_by=" + $scope.rate_by_param;
            window.location.href = path;
        };
        $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
        $scope.increaseLimit = function(index){
            $scope.limit[index] += 4;
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
        $scope.getPartners = function(stopPropagation){
            $http.get('/static/json/countries-json-ru-codes.json')
                .success(function(data){
                    $scope.countryCodes = data;
                }).then(function(){
                    $scope.url = $('#partners-url').val();
                    if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                        $scope.url += '?'+ $.param($scope.params)
                    }
                    $scope.loaded = false;
                    $http.get($scope.url)
                        .success(function(data){
                            _.each(data, function(object){
                                _.each(object.players, function(player){
                                    if(player.citizenship){
                                        if(!player.citizenship.code){
                                            _.each($scope.countryCodes, function(country){
                                                if(player.citizenship.title)
                                                if(country.name === player.citizenship.title){
                                                    player.citizenship.code = country.code;
                                                }
                                            })
                                        }
                                    }
                                })
                            });
                            $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
                            $scope.loaded = true;
                            if($scope.params.rate_by){
                                $scope.playersBySeasonTime = data;
                            } else {
                                $scope.playersBySeasonTime = [];
                                $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 0});
                            }
                            console.log($scope.playersBySeasonTime, $scope.playersBySeasonCount)
                            $scope.briefPartners = [];
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
                            /*$scope.params.rate_by = !$scope.params.rate_by;
                            if(!stopPropagation)
                                $scope.getPartners(true)
                            else
                                $scope.briefPartners*/
                        })
                });
        };

        $scope.getPartners();

    });
