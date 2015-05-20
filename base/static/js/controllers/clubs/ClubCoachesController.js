angular.module('Sportomatics').controller('ClubCoachesController', function($scope, $http, $location, SeasonsService) {
  var url;
  url = $('#club-coaches-api').val();
  $scope.$location = $location;
  $scope.SeasonsService = SeasonsService;
  $scope.params = $location.search();
  $scope.setSeason = function(season) {
    $location.search('season', season);
    $scope.params = $location.search();
    $scope.list();
  };
  $scope.list = function() {
    var params, season;
    if ($scope.params.season) {
      season = $scope.params.season;
    } else {
      season = SeasonsService.getDefaultSeason();
    }
    params = 'season=' + season;
    $scope.data = [];
    $scope.loaded = false;
    $http.get(url + '?' + params).success(function(data) {
      $scope.data = [data];
      $scope.loaded = true;
    });
  };
  $scope.back = function() {
    var params;
    params = 'season=' + $scope.data[$scope.data.length - 1].previous_season.pk;
    $scope.loaded = false;
    $http.get(url + '?' + params).success(function(data) {
      $scope.data.push(data);
      $scope.loaded = true;
    });
  };
  $scope.list();
  $('#footer').visibility({
    'once': false,
    'observeChanges': true,
    'onBottomVisible': function() {
      if ($scope.data && $scope.data[$scope.data.length - 1].previous_season.pk) {
        return $scope.back();
      }
    }
  });
});
