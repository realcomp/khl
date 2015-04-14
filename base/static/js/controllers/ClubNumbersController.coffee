angular.module('Sportomatics').controller('ClubNumbersController', [
    '$http', '$scope', '$location',
    ($http, $scope, $location) ->
        $scope.$location = $location

        $scope.data = {};
        $scope.params = $location.search()

        return
])
