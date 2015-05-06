angular.module('Sportomatics').controller('ClubMainAboutController', [
  '$scope', '$location', 'SeasonsService', function($scope, $location, SeasonsService) {
    $scope.$location = $location;
    $scope.params = $location.search();
    $scope.SeasonsService = SeasonsService;
    this.setSeason = function(season) {
      $location.search('season', season);
      $scope.params = $location.search();
    };
  }
]);
