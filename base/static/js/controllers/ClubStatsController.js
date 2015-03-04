angular.module('Sportomatics')
.controller('ClubStatsController', [
    '$http', '$scope', 'PlayersSearchService', '$location',
    function($http, $scope, PlayersSearchService, $location) {

    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;

    $scope.data = {};
    $scope.loader = false;

    $location.search('club', +$('[name="club"]').val());
    $scope.params = $location.search();

    $scope.sparams = {
        countriesSelected: [],
        leaguesSelected: [],
        leaguesSelectedLoaded: false
    };

    $scope.PlayerPartnersPopup = {
        data: null,
        isClubsVisible: false
    };

    $scope.PlayerPartnersPopupShow = function(e, event) {
        var popup = $('.player-partners-popup:hidden'),
        url = $('#PlayerCardLink').attr('href');
        if (popup.length) {
            $scope.PlayerPartnersPopup.data = null;
            $http.get(url.replace(0, this.player.pk))
            .success(function(data) {
                $scope.PlayerPartnersPopup.data = data;
            });
            $('.player-partners-popup:hidden').show(500).offset({
                left: event.pageX,
                top: event.pageY
            });
        }
    };

    $scope.setPlayersFilter = function(obj) {
        PlayersSearchService.setPlayersFilter($scope, obj);
    };

    PlayersSearchService.search($scope);
}]);
