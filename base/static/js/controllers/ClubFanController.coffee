angular.module('Sportomatics').controller 'ClubFanController', ($scope, MapService) ->

    $scope.loaded = true
    console.log $scope.loaded
    MapService.remove() if MapService.isRendered()
    MapService.createClubsMap([], 'fans')

    return