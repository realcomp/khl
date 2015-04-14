angular.module('Sportomatics').controller('PlayersSearchController', [
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
    $scope.loadLeagues = function(query) {
      return $http.get($scope.leaguesURL);
    };
    $scope.getUnchecker = function(isDefault, defaultValue) {
      return function() {
        if ((isDefault && $(this).attr('value') !== defaultValue) || (!isDefault && $(this).attr('value') === defaultValue)) {
          return $(this).attr('checked', false);
        }
      };
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
        'from': $scope.params.age__lte || 18,
        'to': $scope.params.age__gte || 25,
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
    $scope.lineCheck = function(e) {
      var defaultValue, isDefault;
      defaultValue = '';
      isDefault = $(e).attr('value') === defaultValue;
      if ($(e).is(':checked')) {
        $('input[name="line"]').each($scope.getUnchecker(isDefault, defaultValue));
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
    $scope.contractCheck = function(e) {
      var isDefault;
      isDefault = $(e).attr('value') === '';
      if ($(e).is(':checked')) {
        $('input[name="contract_types"]').each($scope.getUnchecker(isDefault, ''));
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
    PlayersSearchService.loadCountries($scope, $location, PlayersSearchService.search);
  }
]);
