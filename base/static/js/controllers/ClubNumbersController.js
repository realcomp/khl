angular.module('Sportomatics').controller('ClubNumbersController', [
  '$http', '$scope', '$location', function($http, $scope, $location) {
    $scope.$location = $location;
    $scope.data = {};
    $scope.params = $location.search();
    $scope.list = function() {
      $http.get($scope.url).success(function(data) {
        $scope.data = data;
      });
    };
    return;
    return $scope.list();
  }
]);
