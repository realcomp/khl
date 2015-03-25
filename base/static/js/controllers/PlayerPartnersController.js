angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http, $location){
        $scope.player_id = $('#player-id').val();
        console.log($scope.url);

        $scope.params = {
            rate_by: '',
            is_playing: ''
        };
        $scope.go = function(path){
            window.location.href = path;
        };
        $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
        $scope.increaseLimit = function(index){
            console.log(index);
            $scope.limit[index] += 4;
        };
        $scope.setPlaying = function(value){
            $scope.params['is_playing'] = value;
            $scope.getPartners();
        };
        $scope.setRateBy = function(type){
            $scope.params['rate_by'] = type;
            $scope.getPartners();
        };
        $scope.getPartners = function(){
            $scope.url = $('#url').val();
            if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                $scope.url += '?'+ $.param($scope.params)
            }
            $scope.loader = true;
            $http.get($scope.url)
                .success(function(data){
                    $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
                    $scope.loader = false;
                    if($scope.params.rate_by){
                        $scope.playersBySeasonTime = data;
                    } else {
                        $scope.playersBySeasonTime = [];
                        $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 0});
                    }
                })
        };
        $scope.getPartners();

    });