angular.module('Sportomatics').controller('PlayersSearchController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'tags',
    ($http, $scope, $location, PlayersSearchService, tags) ->
        $scope.tags = tags

        $scope.loadCountries = (query) ->
            return $scope.tags.loadCountries($scope.countriesURL, query)

        $scope.loadClubs = (query) ->
            return $scope.tags.loadClubs($scope.clubsURL, query)

        $scope.loadLeagues = (query) ->
            return $http.get($scope.leaguesURL)

        $scope.getUnchecker = (isDefault, defaultValue) ->
            return () ->
                if ((isDefault and $(this).attr('value') != defaultValue) or
                        (!isDefault and $(this).attr('value') == defaultValue))
                    $(this).attr('checked', false)

        $scope.PlayersSearchService = PlayersSearchService
        $scope.$location = $location

        $scope.data = {}
        $scope.countries = []
        $scope.loader = false

        $scope.params = $location.search()

        if $scope.params.citizenship
            $scope.citizenship = JSON.parse($scope.params.citizenship)
        if $scope.params.club
            $scope.club = JSON.parse($scope.params.club)
        if $scope.params.league2
            $scope.league2 = JSON.parse($scope.params.league2)

        if $("#ageRange").length
            $("#ageRange").ionRangeSlider({
                'hide_min_max': true,
                'keyboard': true,
                'min': 15,
                'max': 45,
                'from': $scope.params.age__lte or 18,
                'to': $scope.params.age__gte or 25,
                'type': 'double',
                'step': 1,
                'grid': false
            })

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

        $scope.lineCheck = (e) ->
            defaultValue = ''
            isDefault = $(e).attr('value') == defaultValue
            if ($(e).is(':checked'))
                $('input[name="line"]').each($scope.getUnchecker(isDefault, defaultValue))
            return

        $scope.setCitizenship = (event) ->
            if (event.target.id == 'isCitizenshipAll' and event.target.checked)
                $('#isCitizenshipRussia').attr('checked', false)
                $('#isCitizenshipOther').attr('checked', false)
            if (event.target.id == 'isCitizenshipRussia' and event.target.checked)
                $('#isCitizenshipAll').attr('checked', false)
            if (event.target.id == 'isCitizenshipOther' and event.target.checked)
                self.isCitizenshipOther = event.target.checked
                self.isCitizenshipAll = false
                $('#isCitizenshipAll').attr('checked', false)
            return

        $scope.contractCheck = (e) ->
            isDefault = $(e).attr('value') == ''
            if ($(e).is(':checked'))
                $('input[name="contract"]').each($scope.getUnchecker(isDefault, ''))
            return

        $scope.setPlayersFilter = (obj) ->
            PlayersSearchService.setPlayersFilter($scope, obj)
            return

        $scope.setClubsFilter = (obj) ->
            PlayersSearchService.setClubsFilter($scope, obj)
            return

        $scope.setSeason = (e) ->
            if $(e).val()
                $location.search('season', $(e).val())
            else
                $location.search('season', null)
            $scope.params = $location.search()
            return

        # PlayersSearchService.search($scope)
        PlayersSearchService.loadCountries($scope, $location, PlayersSearchService.search)

        return
])
