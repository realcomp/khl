angular.module('Sportomatics').controller('ClubMainAboutController', [
  '$scope', '$location', '$http', 'SeasonsService', function($scope, $location, $http, SeasonsService) {
    $scope.$location = $location;
    $scope.SeasonsService = SeasonsService;
    $scope.params = $location.search();
    $scope.bestPlayersURL = $('#bestPlayersURL').val();
    $scope.setSeason = function(season) {
      $location.search('season', season);
      $scope.params = $location.search();
      $scope.getBestPlayers();
    };
    $scope.getBestPlayers = function() {
      var params, season;
      if ($scope.params.season) {
        season = $scope.params.season;
      } else {
        season = SeasonsService.getDefaultSeason();
      }
      params = 'season=' + season;
      $scope.loaded = false;
      $http.get($scope.bestPlayersURL + '?' + params).success(function(data) {
        $scope.data = data;
        $scope.loaded = true;
      });
    };
    $scope.getBestPlayers();
  }
]);
