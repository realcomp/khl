angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http){
        $scope.player_id = $('#player-id').val();
        $scope.url = $('#url').val();
        console.log($scope.url);
        $scope.params = {
        };

        $scope.setPlaying = function(value){
            $scope.params['is_playing'] = 1;
            $scope.getPartners();
        };
        $scope.getPartners = function(){
            if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                $scope.url += '?'+ $.param($scope.params)
            }
            $http.get($scope.url)
                .success(function(data){
                    console.log(data)
                    $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 3});
                })
        };
        $scope.getPartners();

    })