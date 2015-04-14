angular.module('Sportomatics').controller('ClubNumbersController', [
  '$http', '$scope', '$location', function($http, $scope, $location) {
    $scope.$location = $location;
    $scope.data = {};
    $scope.params = $location.search();
  }
]);
