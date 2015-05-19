angular.module('Sportomatics').controller('ClubGeographyController', function($http, MapService, $scope, $timeout, $location, SeasonsService) {
  var clubTeamApi, loader, self;
  $scope.$location = $location;
  $scope.SeasonsService = SeasonsService;
  $scope.params = $location.search();
  $scope.setSeason = function(season) {
    $location.search('season', season);
    $scope.params = $location.search();
    $scope.list();
  };
  $scope.switchHistory = function() {
    $location.search('is_history', !$scope.params.is_history || null);
    $scope.params = $location.search();
    $scope.list();
  };
  clubTeamApi = document.getElementById("club-players-api").value;
  loader = $('.loader');
  loader.addClass('active');
  self = this;
  self.reverse = false;
  $scope.state = 'table';
  $scope.sortBy = 'fio';
  $scope.setState = function(state) {
    $scope.state = state;
    if (state === 'map') {
      return $timeout(function() {
        return $scope.setMap();
      }, 500);
    }
  };
  $scope.setSortBy = function(sortBy) {
    $scope.sortBy = sortBy;
    _.sortBy($scope.players, $scope.sortBy);
    if ($scope.sortBy === sortBy) {
      return $scope.players = $scope.players.reverse();
    }
  };
  $scope.list = function() {
    var params, season;
    params = '';
    if (!$scope.params.is_history) {
      if ($scope.params.season) {
        season = $scope.params.season;
      } else {
        season = SeasonsService.getDefaultSeason();
      }
      params = 'season=' + season;
    }
    return $http.get(clubTeamApi + '?' + params).success(function(data) {
      $scope.players = _.sortBy(_.filter(data, function(player) {
        return (player.birth_place != null) && player.birth_place.length !== 0;
      }), $scope.sortBy);
      $scope.cities = _.sortBy(_.map(_.groupBy(_.map($scope.players, function(player) {
        return {
          city: player.birth_place
        };
      }), 'city'), function(value, key) {
        return {
          name: key,
          count: value.length
        };
      }), 'count').reverse();
      return loader.removeClass('active');
    });
  };
  $scope.list();
  $scope.setMap = function() {
    if (MapService.isRendered() === true) {
      MapService.remove();
    }
    return MapService.createClubsMap($scope.players, 'players').then(function() {
      return loader.removeClass('active');
    });
  };
});
