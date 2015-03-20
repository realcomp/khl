angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.data = {};
    $scope.params = $location.search();
    $scope.setType = function(type) {
      $location.search('type', type || null);
      $scope.params = $location.search();
    };
    if ($scope.params.season) {
      $('[name="season"]').attr('value', $scope.params.season);
    }
    $scope.setSeason = function(e) {
      $location.search('season', $(e).val());
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.list = function() {
      var params;
      params = '';
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        $scope.data = data;
        return $scope.loaded = true;
      });
    };
  }
]);
