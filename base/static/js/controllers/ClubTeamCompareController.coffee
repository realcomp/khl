angular.module('Sportomatics').controller 'ClubTeamCompareController', ($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory, $timeout) ->
    self = this;
    this.url = document.getElementById('api-player-indicators').value
    averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart()
    $scope.localeObject = LocaleFactory.selectedLocale;
    $scope.setField = averageClubPlayerIndicatorsChart.setField
    $scope.field = averageClubPlayerIndicatorsChart.getField()
    $scope.dataType = averageClubPlayerIndicatorsChart.getDataType()
    $scope.clubs = []
    $scope.offenders = true
    $scope.defenders = true

    $scope.$watch 'field', () ->
        if $scope.clubs.length > 0
            $scope.listAveragePlayer()

    $scope.setSelectedPlayer = (obj) ->
        if obj? and obj.originalObject?
            $scope.selectedPlayer = obj.originalObject

    $scope.addAverageClubPlayerData = () ->
        if not $scope.selectedClub?
            return
        pk = $scope.selectedClub.originalObject.pk
        if not pk?
            return
        url = $('#club-team-api').val().replace('0/', '') + pk
        $http.get(url).success (data, status, headers) ->
            LocaleFactory.setLocale headers()['content-language']
            players = data.all_players = _.filter(data.all_players, (player) ->
                player.line_display.indexOf('Goalkeeper') is -1
            )
            queries = []
            _.each players, (player) ->
                player.selected = true
                queries.push $http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season')
                return
            $scope.loader = true
            $q.all(queries).then (results) ->
                $scope.loader = false
                lastSeasonResult = _.last results[0].data.results
                clubObject =
                    all_players: data.all_players,
                    offender_players: data.offender_players
                    defender_players: data.defender_players
                    title: $scope.selectedClub.originalObject.title
                    color: $scope.selectedClub.originalObject.main_color or getRandomColor()
                    id: $scope.selectedClub.originalObject.pk
                    dataBySeason:
                        results: [{
                            season: lastSeasonResult['season']
                        }]
                    results: results
                $scope.clubs.push clubObject
                $timeout( () ->
                    $scope.listAveragePlayer()
                , 100)
                return
            return
        return

    $scope.addPlayerToClub = (title) ->
        club = _.findWhere($scope.clubs, title: title)
        $q.all([$http.get(self.url.replace('/0/', '/' + $scope.selectedPlayer.pk + '/') + '?group_by=season')]).then (results) ->
            $scope.selectedPlayer.selected = true
            club.all_players.push $scope.selectedPlayer
            club.results.push results[0]
            $scope.listAveragePlayer()

    $scope.togglePlayerSelection = (title, index) ->
        club = _.findWhere($scope.clubs, title: title)
        player = club.all_players[index]
        player.selected = not player.selected
        $('#player_'+index).attr('checked', !$('#player_'+index).attr('checked'))
        $scope.listAveragePlayer()

    $scope.listAveragePlayer = () ->
        newPlayerIndicatorsData = []
        console.log $scope.defenders
        _.each $scope.clubs, (club) ->
            #if $scope.defenders is false then for player in club.all_players then if player.line_display is 'Defender' then player.selected = false
            #if $scope.offenders is false then for player in club.all_players then if player.line_display is 'Offender' then player.selected = false
            selectedPlayers = _.countBy(_.filter(club.all_players, (player) ->
                return player.line_display is 'Offender' and $scope.offenders is true or player.line_display is 'Defender' and $scope.defenders is true
            ), selected: true)['true']
            console.log selectedPlayers
            for key of _.last club.results[0].data.results #идем по всем показателям, берем их из первого объекта
                if _.contains(ALL_FIELDS, key) #если это поле -- показатель
                    averageData = 0
                    _.each club.results, (result) ->
                        player = _.findWhere(club.all_players, pk: Number(result.config.url.match("players\/(.*)\/indicators")[1]))
                        player.result = _.last(result.data.results)[$scope.field]
                        return if player.line_display is 'Offender' and not $scope.offenders or player.line_display is 'Defender' and not $scope.defenders
                        if player.selected is true
                            averageData += parseFloat(_.last(result.data.results)[key])
                        return
                    averageData = parseFloat(averageData / selectedPlayers).toFixed(3)
                    club.dataBySeason.results[0][key] = averageData
            clubObject = {
                name: club.title
                data: club.dataBySeason.results.map (el) ->
                    return (
                        x: new Date(el.season.end_date.split('-')[0]).getTime()
                        y: parseFloat(el[$scope.field])
                        drilldown: el.season.end_date
                    )
                color: club.color,
                stack: club.id
            }
            newPlayerIndicatorsData.push clubObject

        averageClubPlayerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData)
        averageClubPlayerIndicatorsChart.setContext($scope);
        averageClubPlayerIndicatorsChart.setPeriod(30);
        averageClubPlayerIndicatorsChart.draw()
        self.chart = $('#chartdiv').highcharts()


    return
