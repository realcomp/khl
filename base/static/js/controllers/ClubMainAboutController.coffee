angular.module('Sportomatics').controller('ClubMainAboutController', [
    '$scope', '$location',
    ($scope, $location) ->
        $scope.$location = $location
        $scope.params = $location.search()

        $scope.setSeason = (season) ->
            $location.search('season', season)
            $scope.params = $location.search()
            return

        return
])
