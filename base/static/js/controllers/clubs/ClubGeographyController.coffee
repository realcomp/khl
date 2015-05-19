angular.module('Sportomatics').controller 'ClubGeographyController', ($http, MapService, $scope, $timeout, $location, SeasonsService) ->
    $scope.$location = $location
    $scope.SeasonsService = SeasonsService

    $scope.params = $location.search()

    $scope.setSeason = (season) ->
        $location.search('season', season)
        $scope.params = $location.search()
        $scope.list()
        return

    $scope.switchHistory = () ->
        $location.search('is_history', not $scope.params.is_history or null)
        $scope.params = $location.search()
        $scope.list()
        return

    clubTeamApi = document.getElementById("club-players-api").value
    loader = $('.loader')
    loader.addClass('active')
    self = this
    self.reverse = false
    $scope.state = 'table'
    $scope.sortBy = 'fio'

    $scope.setState = (state) ->
        $scope.state = state
        if state is 'map'
            $timeout(() ->
                $scope.setMap()
            , 500)

    $scope.setSortBy = (sortBy) ->
        $scope.sortBy = sortBy
        _.sortBy($scope.players, $scope.sortBy)
        if $scope.sortBy is sortBy then $scope.players = $scope.players.reverse()

    $scope.list = () ->
        params = ''
        if not $scope.params.is_history
            if $scope.params.season
                season = $scope.params.season
            else
                season = SeasonsService.getDefaultSeason()
            params = 'season=' + season

        $http.get(clubTeamApi + '?' + params)
            .success (data) ->
                # $scope.players = _.sortBy(_.filter(data.all_players, (player) ->
                $scope.players = _.sortBy(_.filter(data, (player) ->
                    return player.birth_place? and player.birth_place.length isnt 0
                ), $scope.sortBy)
                $scope.cities = _.sortBy(_.map(_.groupBy(_.map($scope.players, (player) ->
                    return city: player.birth_place
                ), 'city'), (value, key) ->
                    return (
                        name: key,
                        count: value.length
                    )
                ), 'count').reverse()
                loader.removeClass('active')

    $scope.list()

    $scope.setMap = () ->
        if MapService.isRendered() is true then MapService.remove()
        MapService.createClubsMap($scope.players, 'players').then(() ->
            loader.removeClass('active')
        )


    return
