angular.module('Sportomatics').controller('ClubListController', [
  '$http', '$scope', '$location', 'PlayersSearchService', 'MapService', 'SeasonsService', function($http, $scope, $location, PlayersSearchService, MapService, SeasonsService) {
    var url;
    url = $('#ClubListForm').attr('action');
    this.map = true;
    $scope.$location = $location;
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.SeasonsService = SeasonsService;
    $scope.countries = {};
    $scope.sparams = {};
    $scope.params = $location.search();
    $scope.params.league = '';
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
      if ($scope.data && $scope.data.league) {
        if ($scope.data.league.pk) {
          return $scope.data.league.pk === league;
        } else {
          return league === null;
        }
      } else {
        return false;
      }
    };
    $scope.list = function(all) {
      var params;
      params = '';
      params += '&order_by=' + ($scope.params.order_by || '%s_title');
      if ($scope.params.reversed) {
        params += '&reversed=true';
      }
      if ($scope.params.season || $scope.season) {
        params += '&season=' + ($scope.params.season || $scope.season);
      }
      if ($scope.params.league !== void 0) {
        params += '&league=' + ($scope.params.league || '');
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
    $scope.next = function(isAll) {
      url = $scope.data.next;
      if (isAll) {
        url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
      }
      $scope.loaded = false;
      return $http.get(url).success(function(data) {
        if (isAll) {
          $scope.data = data;
        } else {
          $scope.data.next = data.next;
          $scope.data.results = $scope.data.results.concat(data.results);
          $scope.clubs = $scope.clubs.concat(data.results);
        }
        $scope.loaded = true;
      });
    };
    PlayersSearchService.loadCountries($scope, $location, function() {});
    $scope.list();
  }
]);
