angular.module('Sportomatics').controller('ClubListController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'MapService', 'SeasonsService', 'OrderService',
    ($http, $scope, $location, PlayersSearchService, MapService, SeasonsService, OrderService) ->
        url = $('#ClubListURL').attr('href')
        @map = true;

        $scope.$location = $location
        $scope.PlayersSearchService = PlayersSearchService
        $scope.SeasonsService = SeasonsService

        $scope.countries = {}
        $scope.sparams = {}

        $scope.params = $location.search()

        $scope.setSeason = (season) ->
            $location.search('season', season)
            $location.search('league', null) # reset league
            $scope.params = $location.search()
            $scope.list()
            return

        $scope.setTable = (isTable) ->
            $location.search('is_table', isTable or null)
            $scope.params = $location.search()
            return

        $scope.switchHistory = () ->
            $location.search('is_history', not $scope.params.is_history or null)
            $scope.params = $location.search()
            $scope.list()
            return

        $scope.setCountry = (country) ->
            if not $scope.isCountryActive(country)
                $location.search('country', country)
                $scope.params = $location.search()
                $scope.list()
            return

        $scope.setLeague = (league) ->
            if $scope.params.league != league
                $location.search('league', league)
                $scope.params = $location.search()
                $scope.list()
            return

        $scope.isCountryActive = (country) ->
            if $scope.params.country
                return $scope.params.country == country
            else
                return country == 1

        $scope.isLeagueActive = (league) ->
            # all
            if $scope.params.league == '*' and league == '*'
                return true
            if $scope.params.league  # selected
                return +$scope.params.league == +league
            else if $scope.data.league  # default
                return $scope.data.league.pk == +league
            return false

        $scope.setOrderBy = (order_by) ->
            if $scope.loaded
                OrderService.setOrderBy($scope, order_by)
                $scope.list()
            return

        $scope.list = (all) ->
            params = '&order_by=' + ($scope.params.order_by or '%s_title')
            if $scope.params.reversed
                params += '&reversed=true'

            # // if ($scope.sparams.leaguesSelected) {
            # //     $location.search('league', $scope.sparams.leaguesSelected);
            # // } else {
            # //     $location.search('league', null);
            # // }
            # // if ($scope.sparams.contriesSelected) {
            # //     $location.search('country', $scope.sparams.countriesSelected);
            # // } else {
            # //     $location.search('country', null);
            # // }

            if $scope.params.season or $scope.season
                params += '&season=' + ($scope.params.season or $scope.season)
            if $scope.params.league != '*'  # not all leagues
                params += '&league=' + ($scope.params.league or '')  # selected or default
            if $scope.params.is_history
                params += '&is_history=true'
            params += '&country=' + ($scope.params.country or 1)

            $scope.params = $location.search()
            $scope.data = {}
            $scope.loaded = false
            $http.get(url + '?' + params
            ).success((data) ->
                $scope.leagues = data.leagues
                $scope.data = data
                $scope.clubs = data.results
                $scope.loaded = true
                return
            )
            return

        $scope.next = () ->
            $scope.loaded = false
            $http.get($scope.data.next
            ).success((data) ->
                $scope.data.next = data.next
                $scope.data.results = $scope.data.results.concat(data.results)
                $scope.clubs = $scope.clubs.concat(data.results)
                $scope.loaded = true
                return
            )

        PlayersSearchService.loadCountries($scope)

        $scope.list()

        $('.b-tabs-content').visibility({
            'once': false,
            'observeChanges': true,
            'onBottomVisible': () ->
                if $scope.data.next
                    $scope.next()
        })

        return
])
