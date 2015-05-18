angular.module('Sportomatics').controller('NumbersController', [
    '$http', '$scope', '$location', 'SeasonsService',
    ($http, $scope, $location, SeasonsService) ->
        $scope.$location = $location
        $scope.SeasonsService = SeasonsService

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

        $scope.setSeason = (season) ->
            $location.search('season', season)
            $scope.params = $location.search()
            $scope.list()
            return

        $scope.getLimit = (number) ->
            # get limit by player's number
            if not $scope.limit[number]
                $scope.limit[number] = 5
            return $scope.limit[number]

        $scope.increaseLimit = (number) ->
            $scope.limit[number] += 5
            return

        $scope.getSeasonsCount = (group) ->
            i = 0
            clubplayers = []
            for club in group.clubs
                for clubplayer in club.clubplayers
                    if clubplayer.pk not in clubplayers
                        clubplayers.push(clubplayer.pk)
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
