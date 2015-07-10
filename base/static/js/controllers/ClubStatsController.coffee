angular.module('Sportomatics').controller('ClubStatsController', [
    '$http', '$scope', '$location', 'PlayersSearchService',
    ($http, $scope, $location, PlayersSearchService) ->
        $scope.PlayersSearchService = PlayersSearchService
        $scope.$location = $location

        $scope.data = {};
        $scope.countries = [];
        $scope.loader = false;

        $scope.club = [{'pk': +$('[name="club"]').val()}]
        $scope.club_enabled = true

        $scope.params = $location.search()

        $scope.PlayerPartnersPopup = {
            'data': null,
            'isClubsVisible': false,
        }

        $scope.PlayerPartnersPopupShow = (e, event) ->
            popup = $('.player-partners-popup:hidden')
            url = $('#PlayerCardLink').attr('href')
            if popup.length
                $scope.PlayerPartnersPopup.data = null
                $http.get(url.replace(0, @player.pk)).success (data) ->
                    $scope.PlayerPartnersPopup.data = data
                    return
                $('.player-partners-popup:hidden').show(500).offset({
                    'left': event.pageX,
                    'top': event.pageY,
                })
            return

        $scope.setPlayersFilter = (obj) ->
            PlayersSearchService.setPlayersFilter($scope, obj)
            return

        $scope.setSeason = (e) ->
            $location.search('season', $(e).val())
            $scope.params = $location.search()
            PlayersSearchService.search($scope)
            return

        PlayersSearchService.search($scope)

        return
])
