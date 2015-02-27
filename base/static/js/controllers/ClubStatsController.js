angular.module('Sportomatics')
.controller('ClubStatsController', [
    '$http', '$scope', 'PlayersSearchService',
    function($http, $scope, PlayersSearchService) {
    $scope.PlayersSearchService = PlayersSearchService;

    $scope.data = {};
    $scope.loader = false;

    $scope.params = {
        orderBy: '[%22%s_lastname%22,%22%s_name%22]',
        orderByReversed: false,
        ratedBy: '',
        alphabetFilter: null,
        isPlaying: true,
        playersFilter: null,
        clubsFilter: {
            pk: +$('[name="club"]').val()
        },
        countriesSelected: [],
        leaguesSelected: []
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

    $scope.moreClubs = function(e) {
        $(e).closest('td').toggleClass('show-more-clubs')
    };

    $scope.setPlayersFilter = function(obj) {
        PlayersSearchService.setPlayersFilter($scope, obj);
    };

    PlayersSearchService.search($scope);
}]);
