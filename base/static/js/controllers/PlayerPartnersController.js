angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http){
        $scope.player_id = $('#player-id').val();
        $scope.url = $('#url').val();
        console.log($scope.url);
        $scope.params = {
            'is_playing': 'hui'
        };

        $http.get($scope.url + '?'+ $.param( $scope.params ))
            .success(function(data){
                console.log(data)
            })
    })