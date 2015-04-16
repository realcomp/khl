angular.module('Sportomatics').controller('ClubNumbersController', [
  '$http', '$scope', '$location', function($http, $scope, $location) {
    var club, player, url;
    $scope.$location = $location;
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
    $scope.getLimit = function(number) {
      if (!$scope.limit[number]) {
        $scope.limit[number] = 4;
      }
      return $scope.limit[number];
    };
    $scope.increaseLimit = function(number) {
      $scope.limit[number] += 4;
    };
    $scope.getSeasonsCount = function(group) {
      var i, j, len, ref;
      i = 0;
      ref = group.clubs;
      for (j = 0, len = ref.length; j < len; j++) {
        club = ref[j];
        i += club.seasons.length;
      }
      return i;
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
      $scope.loaded = false;
      $http.get(url + '?' + params).success(function(data) {
        $scope.data = data;
        $scope.loaded = true;
      });
    };
    $scope.list();
  }
]);
