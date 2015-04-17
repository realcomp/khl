angular.module('Sportomatics').controller('ClubNumbersController', [
    '$http', '$scope', '$location',
    ($http, $scope, $location) ->
        $scope.$location = $location

        url = $('#PlayerNumbersApi').attr('href')
        club = $('[name="club"]').val()
        player = $('[name="player"]').val()

        $scope.limit = {}
        $scope.data = {}
        $scope.params = $location.search()

        $scope.PlayerPartnersPopup = {
            'data': null,
            'isClubsVisible': false,
        }

        $scope.PlayerPartnersPopupShow = (player, $event) ->
            popup = $('.player-partners-popup:hidden')
            url = $('#PlayerCardLink').attr('href')
            if popup.length
                $scope.PlayerPartnersPopup.data = null
                $http.get(url.replace(0, player.pk)
                ).success((data) ->
                    $scope.PlayerPartnersPopup.data = data
                    return
                )
                $('.player-partners-popup:hidden').show(500).offset({
                    'left': $event.pageX,
                    'top': $event.pageY,
                })
            return

        $scope.getLimit = (number) ->
            # get limit by player's number
            if not $scope.limit[number]
                $scope.limit[number] = 4
            return $scope.limit[number]

        $scope.increaseLimit = (number) ->
            $scope.limit[number] += 4
            return

        $scope.getSeasonsCount = (group) ->
            i = 0
            seasons = []
            for club in group.clubs
                for season in club.seasons
                    if season.pk not in seasons
                        seasons.push(season.pk)
                        i += 1
            return i

        $scope.setSeason = (season) ->
            $location.search('season', season or null)
            $scope.params = $location.search()
            $scope.list()

        $scope.list = () ->
            params = ''
            if club
                params += '&club=' + club
            if player
                params += '&player=' + player
            if $scope.params.season
                params += '&season=' + $scope.params.season

            $scope.loaded = false
            $http.get(url + '?' + params
            ).success((data) ->
                $scope.data = data
                $scope.loaded = true
                return
            )
            return

        $scope.list()

        return
])
