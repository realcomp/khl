angular.module('Sportomatics').controller('ClubListController', [
  '$http', '$scope', '$location', 'PlayersSearchService', 'MapService', 'SeasonsService', 'OrderService', function($http, $scope, $location, PlayersSearchService, MapService, SeasonsService, OrderService) {
    var url;
    url = $('#ClubListURL').attr('href');
    this.map = true;
    $scope.$location = $location;
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.SeasonsService = SeasonsService;
    $scope.countries = {};
    $scope.sparams = {};
    $scope.params = $location.search();
    $scope.setSeason = function(season) {
      $location.search('season', season);
      $location.search('league', null);
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.setTable = function(isTable) {
      $location.search('is_table', isTable || null);
      $scope.params = $location.search();
    };
    $scope.switchHistory = function() {
      $location.search('is_history', !$scope.params.is_history || null);
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.setCountry = function(country) {
      if (!$scope.isCountryActive(country)) {
        $location.search('country', country);
        $scope.params = $location.search();
        $scope.list();
      }
    };
    $scope.setLeague = function(league) {
      if ($scope.params.league !== league) {
        $location.search('league', league);
        $scope.params = $location.search();
        $scope.list();
      }
    };
    $scope.isCountryActive = function(country) {
      if ($scope.params.country) {
        return $scope.params.country === country;
      } else {
        return country === 1;
      }
    };
    $scope.isLeagueActive = function(league) {
      if ($scope.params.league === '*' && league === '*') {
        return true;
      }
      if ($scope.params.league) {
        return +$scope.params.league === +league;
      } else if ($scope.data.league) {
        return $scope.data.league.pk === +league;
      }
      return false;
    };
    $scope.setOrderBy = function(order_by) {
      if ($scope.loaded) {
        OrderService.setOrderBy($scope, order_by);
        $scope.list();
      }
    };
    $scope.list = function(all) {
      var params;
      params = '&order_by=' + ($scope.params.order_by || '%s_title');
      if ($scope.params.reversed) {
        params += '&reversed=true';
      }
      if ($scope.params.season || $scope.season) {
        params += '&season=' + ($scope.params.season || $scope.season);
      }
      if ($scope.params.league !== '*') {
        params += '&league=' + ($scope.params.league || '');
      }
      if ($scope.params.is_history) {
        params += '&is_history=true';
      }
      params += '&country=' + ($scope.params.country || 1);
      $scope.params = $location.search();
      $scope.data = {};
      $scope.loaded = false;
      $http.get(url + '?' + params).success(function(data) {
        $scope.leagues = data.leagues;
        $scope.data = data;
        $scope.clubs = data.results;
        $scope.loaded = true;
      });
    };
    $scope.next = function() {
      $scope.loaded = false;
      return $http.get($scope.data.next).success(function(data) {
        $scope.data.next = data.next;
        $scope.data.results = $scope.data.results.concat(data.results);
        $scope.clubs = $scope.clubs.concat(data.results);
        $scope.loaded = true;
      });
    };
    PlayersSearchService.loadCountries($scope);
    $scope.list();
    $('.b-tabs-content').visibility({
      'once': false,
      'observeChanges': true,
      'onBottomVisible': function() {
        if ($scope.data.next) {
          return $scope.next();
        }
      }
    });
  }
]);
