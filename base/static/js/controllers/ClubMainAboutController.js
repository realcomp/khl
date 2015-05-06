angular.module('Sportomatics').controller('ClubMainAboutController', [
  '$scope', '$location', function($scope, $location) {
    $scope.$location = $location;
    $scope.params = $location.search();
    $scope.setSeason = function(season) {
      $location.search('season', season);
      $scope.params = $location.search();
    };
  }
]);
