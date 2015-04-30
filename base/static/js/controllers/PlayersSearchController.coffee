angular.module('Sportomatics').controller('PlayersSearchController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'tags','$timeout',
    ($http, $scope, $location, PlayersSearchService, tags, $timeout) ->
        $scope.tags = tags

        $timeout(() ->
             $('.ui.dropdown').dropdown();
        ,0)

        $scope.loadCountries = (query) ->
            return $scope.tags.loadCountries($scope.countriesURL, query)

        $scope.loadClubs = (query) ->
            return $scope.tags.loadClubs($scope.clubsURL, query)

        $scope.loadPlayers = (query) ->
            return $scope.tags.loadPlayers($scope.playersURL, query)

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
                'max': 65,
                'from': $scope.params.age__lte or 15,
                'to': $scope.params.age__gte or 65,
                'type': 'double',
                'step': 1,
                'grid': false
            })

        if $("#relatedRange").length
            $("#relatedRange").ionRangeSlider({
                'hide_min_max': true,
                'keyboard': true,
                'min': 0,
                'max': 100,
                'from': $scope.params.related_value__lte or 40,
                'to': $scope.params.related_value__gte or 80,
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
                $('input[name="contract_types"]').each($scope.getUnchecker(isDefault, ''))
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

        $scope.setCountry = (country) ->
            $scope.setLeague('')
            $location.search('country', country or null)
            # re-initialize leagues dropdown
            $timeout(() ->
                $('.ui.dropdown.leagues').dropdown()
            , 0)
            return

        $scope.setLeague = (league) ->
            if not league
                $('.ui.dropdown.leagues .text').text('')
            $location.search('league', league or null)
            return

        # PlayersSearchService.search($scope)
        PlayersSearchService.loadCountries($scope, $location, PlayersSearchService.search)

        return
])
