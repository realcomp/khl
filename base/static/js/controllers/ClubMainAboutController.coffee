angular.module('Sportomatics').controller('ClubMainAboutController', [
    '$scope', '$location', 'SeasonsService',
    ($scope, $location, SeasonsService) ->
        $scope.$location = $location
        $scope.params = $location.search()

        $scope.SeasonsService = SeasonsService

        @setSeason = (season) ->
            $location.search('season', season)
            $scope.params = $location.search()
            return

        return
])
