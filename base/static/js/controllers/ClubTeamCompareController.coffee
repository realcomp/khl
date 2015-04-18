angular.module('Sportomatics').controller 'ClubTeamCompareController', ($scope) ->
    $scope.$watch 'selectedClub', (newval) ->
        console.log newval
    $scope.$on '$viewContentLoaded', () ->
        PlayerIndicatorsController = angular.element(document.getElementById('scope')).scope()
        console.log PlayerIndicatorsController
    return
