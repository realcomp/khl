angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http, $location){
        $scope.player_id = $('#player-id').val();
        $scope.url = $('#url').val();
        console.log($scope.url);
        $scope.params = {
        };
        $scope.go = function(path){
            window.open(path);
        }
        $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
        $scope.increaseLimit = function(index){
            console.log(index);
            $scope.limit[index] += 4;
        }
        $scope.setPlaying = function(value){
            $scope.params['is_playing'] = 1;
            $scope.getPartners();
        };
        $scope.getPartners = function(){
            if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                $scope.url += '?'+ $.param($scope.params)
            }
            $scope.loader = true;
            $http.get($scope.url)
                .success(function(data){
                    console.log(data)
                    $scope.loader = false;
                    $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 0});

                })
        };
        $scope.getPartners();

    })