angular.module('Sportomatics').controller('PlayersSearchController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'tags','$timeout',
    ($http, $scope, $location, PlayersSearchService, tags, $timeout) ->
        $scope.tags = tags

        $scope.PlayersSearchService = PlayersSearchService
        $scope.$location = $location

        $scope.params = $location.search()

        $scope.setState = (state) ->
            $location.search('state', state)
            $scope.params = $location.search()
            # start searching
            if state == 'table' and not $scope.data
                PlayersSearchService.search($scope)
            return

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

        $scope.countries = []


        if $scope.params.citizenship
            $scope.citizenship = JSON.parse($scope.params.citizenship)
        if $scope.params.club
            $scope.club = JSON.parse($scope.params.club)
        if $scope.params.league2
            $scope.league2 = JSON.parse($scope.params.league2)

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

        $scope.search = () ->
            $scope.setState('table')
            PlayersSearchService.search($scope)
            return

        PlayersSearchService.loadCountries($scope)

        # autorun if tab active
        if $scope.params.state == 'table' and not $scope.data
            # wait for $scope.params initialization
            f = () ->
                PlayersSearchService.search($scope)
            $timeout(f, 1000)

        $('.unstackable.striped.table').visibility({
            'once': false,
            'observeChanges': true,
            'onBottomVisible': () ->
                if $scope.data and $scope.data.next
                    PlayersSearchService.next($scope)
        })

        return
])
