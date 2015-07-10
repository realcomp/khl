var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').controller('NumbersController', [
  '$http', '$scope', '$location', 'SeasonsService', function($http, $scope, $location, SeasonsService) {
    var club, player, url;
    $scope.$location = $location;
    $scope.SeasonsService = SeasonsService;
    url = $('#PlayerNumbersApi').attr('href');
    club = $('[name="club"]').val();
    player = $('[name="player"]').val();
    $scope.limit = {};
    $scope.data = {};
    $scope.params = $location.search();
    $scope.PlayerPartnersPopup = {
      'data': null,
      'isClubsVisible': false
    };
    $scope.PlayerPartnersPopupShow = function(player, $event) {
      var popup;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length) {
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, player.pk)).success(function(data) {
          $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': $event.pageX,
          'top': $event.pageY
        });
      }
    };
    $scope.setSeason = function(season) {
      $location.search('season', season);
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.getLimit = function(number) {
      if (!$scope.limit[number]) {
        $scope.limit[number] = 5;
      }
      return $scope.limit[number];
    };
    $scope.increaseLimit = function(number) {
      $scope.limit[number] += 5;
    };
    $scope.getSeasonsCount = function(group) {
      var clubplayer, clubplayers, i, j, k, len, len1, ref, ref1, ref2;
      i = 0;
      clubplayers = [];
      ref = group.clubs;
      for (j = 0, len = ref.length; j < len; j++) {
        club = ref[j];
        ref1 = club.clubplayers;
        for (k = 0, len1 = ref1.length; k < len1; k++) {
          clubplayer = ref1[k];
          if (ref2 = clubplayer.pk, indexOf.call(clubplayers, ref2) < 0) {
            clubplayers.push(clubplayer.pk);
            i += 1;
          }
        }
      }
      return i;
    };
    $scope.setSeason = function(season) {
      $location.search('season', season || null);
      $scope.params = $location.search();
      return $scope.list();
    };
    $scope.list = function() {
      var params;
      params = '';
      if (club) {
        params += '&club=' + club;
      }
      if (player) {
        params += '&player=' + player;
      }
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      $scope.data = {};
      $scope.loaded = false;
      $http.get(url + '?' + params).success(function(data) {
        $scope.data = data;
        $scope.loaded = true;
      });
    };
    $scope.list();
  }
]);
