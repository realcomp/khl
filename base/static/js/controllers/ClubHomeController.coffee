angular.module('Sportomatics').controller 'ClubHomeController', ($scope, $location, $http, HighchartsFactory) ->
    $scope.clubMatchApi = document.getElementById('club-match-api').value
    $scope.clubPk = document.getElementById('team-id').value
    $scope.params = $location.search()

    $scope.createVisitorsChart = () ->
            params = ''
            params += '?club='+$scope.clubPk
            #if $scope.params.season
            params += '&season=19'# + $scope.params.season
            $scope.loaded = false
            $http.get($scope.clubMatchApi + params)
                .success (data) ->
                    $scope.games = _.filter(_.sortBy(data, (el) ->
                        return new Date(el).getTime()
                    ).reverse(), (game) ->
                        return game.is_home is true
                    )
                    seriesClub = {}
                    seriesOpponent = {}
                    visitorsObject = (
                        name: 'club'
                        data: $scope.games.map((game, index) ->
                            #opponentAddress = if game.opponent.address and game.opponent.address.title then game.opponent.address.title else ''
                            return (
                                x: index
                                y: game.spectators
                                date: game.date
                                name: game.opponent.title_verbose
                                score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score)
                                spectators: game.spectators + ' (' + parseInt(parseFloat(game.arena_capacity_rate).toFixed(2)*100) + '%)'
                            )
                        ).filter (toFilter) ->
                            return toFilter?
                    )
                    $scope.loaded = true
                    clubGamesChart = new HighchartsFactory.ArenaVisitorsChart 'chartdiv', [visitorsObject], $scope.games[0].arena_capacity
                    clubGamesChart.draw()

    $scope.createVisitorsChart()

    return
