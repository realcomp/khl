angular.module('Sportomatics').controller('ClubGeographyController', function($http, MapService, $scope, $timeout) {
  var clubTeamApi, giveCountryCodes, loader, self;
  clubTeamApi = document.getElementById("club-team-api").value;
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
  giveCountryCodes = function(player) {
    if (player.citizenship != null) {
      if (player.citizenship.code == null) {
        return _.each($scope.countryCodes, function(country) {
          if (player.citizenship.title) {
            if (country.name === player.citizenship.title) {
              return player.citizenship.code = country.code;
            }
          }
        });
      }
    }
  };
  $http.get(clubTeamApi + '?season=19').success(function(data) {
    $http.get('/static/json/countries-json-ru-codes.json').success(function(codes) {
      $scope.countryCodes = codes;
      $scope.loaded = true;
      return _.each(data.all_players, giveCountryCodes);
    }).then(function() {
      $scope.players = _.sortBy(_.filter(data.all_players, function(player) {
        return (player.birth_place != null) && player.birth_place.length !== 0;
      }), $scope.sortBy);
      return $scope.cities = _.sortBy(_.map(_.groupBy(_.map($scope.players, function(player) {
        return {
          city: player.birth_place
        };
      }), 'city'), function(value, key) {
        return {
          name: key,
          count: value.length
        };
      }), 'count').reverse();
    });
    return loader.removeClass('active');
  });
  $scope.setMap = function() {
    if (MapService.isRendered() === true) {
      MapService.remove();
    }
    return MapService.createClubsMap($scope.players, 'players').then(function() {
      return loader.removeClass('active');
    });
  };
});
