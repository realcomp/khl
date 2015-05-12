angular.module('Sportomatics').controller 'ClubGeographyController', ($http, MapService, $scope, $timeout) ->
    clubTeamApi = document.getElementById("club-team-api").value
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


    giveCountryCodes = (player) ->
        if player.citizenship?
            if not player.citizenship.code?
                _.each($scope.countryCodes, (country) ->
                    if player.citizenship.title
                        if country.name is player.citizenship.title
                            player.citizenship.code = country.code
                )
    $http.get(clubTeamApi + '?season=19')
        .success (data) ->
            $http.get('/static/json/countries-json-ru-codes.json')
                .success((codes) ->
                    $scope.countryCodes = codes
                    $scope.loaded = true
                    _.each data.all_players, giveCountryCodes
                ).then(() ->
                    $scope.players = _.sortBy(_.filter(data.all_players, (player) ->
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
                )
            loader.removeClass('active')

    $scope.setMap = () ->
        if MapService.isRendered() is true then MapService.remove()
        MapService.createClubsMap($scope.players, 'players').then(() ->
            loader.removeClass('active')
        )


    return
