angular.module('Sportomatics').controller('PlayersSearch2Controller', [
  '$http', '$scope', '$location', 'PlayersSearchService', 'tags', '$timeout', function($http, $scope, $location, PlayersSearchService, tags, $timeout) {
    $scope.tags = tags;
    $timeout(function() {
      return $('.ui.dropdown').dropdown();
    }, 0);
    $scope.loadCountries = function(query) {
      return $scope.tags.loadCountries($scope.countriesURL, query);
    };
    $scope.loadClubs = function(query) {
      return $scope.tags.loadClubs($scope.clubsURL, query);
    };
    $scope.loadPlayers = function(query) {
      return $scope.tags.loadPlayers($scope.playersURL, query);
    };
    $scope.loadLeagues = function(query) {
      return $http.get($scope.leaguesURL);
    };
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;
    $scope.data = {};
    $scope.countries = [];
    $scope.loader = false;
    $scope.params = $location.search();
    if ($scope.params.citizenship) {
      $scope.citizenship = JSON.parse($scope.params.citizenship);
    }
    if ($scope.params.club) {
      $scope.club = JSON.parse($scope.params.club);
    }
    if ($scope.params.league2) {
      $scope.league2 = JSON.parse($scope.params.league2);
    }
    if ($("#ageRange").length) {
      $("#ageRange").ionRangeSlider({
        'hide_min_max': true,
        'keyboard': true,
        'min': 15,
        'max': 65,
        'from': $scope.params.age__lte || 15,
        'to': $scope.params.age__gte || 65,
        'type': 'double',
        'step': 1,
        'grid': false
      });
    }
    if ($("#relatedRange").length) {
      $("#relatedRange").ionRangeSlider({
        'hide_min_max': true,
        'keyboard': true,
        'min': 0,
        'max': 100,
        'from': $scope.params.related_value__gte || 40,
        'to': $scope.params.related_value__lte || 80,
        'type': 'double',
        'step': 1,
        'grid': false
      });
    }
    $scope.PlayerPartnersPopup = {
      'data': null,
      'isClubsVisible': false
    };
    $scope.PlayerPartnersPopupShow = function(e, event) {
      var popup, url;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length) {
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, this.player.pk)).success(function(data) {
          $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
    $scope.setCitizenship = function(event) {
      if (event.target.id === 'isCitizenshipAll' && event.target.checked) {
        $('#isCitizenshipRussia').attr('checked', false);
        $('#isCitizenshipOther').attr('checked', false);
      }
      if (event.target.id === 'isCitizenshipRussia' && event.target.checked) {
        $('#isCitizenshipAll').attr('checked', false);
      }
      if (event.target.id === 'isCitizenshipOther' && event.target.checked) {
        self.isCitizenshipOther = event.target.checked;
        self.isCitizenshipAll = false;
        $('#isCitizenshipAll').attr('checked', false);
      }
    };
    $scope.setPlayersFilter = function(obj) {
      PlayersSearchService.setPlayersFilter($scope, obj);
    };
    $scope.setClubsFilter = function(obj) {
      PlayersSearchService.setClubsFilter($scope, obj);
    };
    $scope.setSeason = function(e) {
      if ($(e).val()) {
        $location.search('season', $(e).val());
      } else {
        $location.search('season', null);
      }
      $scope.params = $location.search();
    };
    $scope.setCountry = function(country) {
      $scope.setLeague('');
      $location.search('country', country || null);
      $timeout(function() {
        return $('.ui.dropdown.leagues').dropdown();
      }, 0);
    };
    $scope.setLeague = function(league) {
      if (!league) {
        $('.ui.dropdown.leagues .text').text('');
      }
      $location.search('league', league || null);
    };
  }
]);
