angular.module('Sportomatics').controller 'ClubTeamCompareController', ($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory) ->
    self = this;
    this.url = document.getElementById('api-player-indicators').value

    #averageClubPlayerIndicatorsChart = new IndicatorsFactory.PlayerIndicatorsChart()
    averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart()
    $scope.localeObject = LocaleFactory.selectedLocale;
    $scope.setField = averageClubPlayerIndicatorsChart.setField
    $scope.field = averageClubPlayerIndicatorsChart.getField()
    $scope.dataType = averageClubPlayerIndicatorsChart.getDataType()
    $scope.loader = true
    $scope.clubs = []

    $scope.addAverageClubPlayerData = () ->
        if not $scope.selectedClub?
            return
        pk = $scope.selectedClub.originalObject.pk
        if not pk?
            return
        url = $('#club-team-api').val().replace('0/', '') + pk
        $http.get(url).success (data, status, headers) ->
            LocaleFactory.setLocale headers()['content-language']
            console.log LocaleFactory.selectedLocale
            players = data.all_players = _.filter(data.all_players, (player) ->
                player.line_display.indexOf('Goalkeeper') is -1
            )
            data.offender_players.map (el) ->
                el.selected = true
                return el
            data.defender_players.map (el) ->
                el.selected = true
                return el
            queries = []
            _.each players, (player) ->
                player.selected = true
                queries.push $http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season')
                return
            $q.all(queries).then (results) ->
                lastSeasonResult = _.last results[0].data.results
                clubObject =
                    players: data.all_players,
                    offender_players: data.offender_players
                    defender_players: data.defender_players
                    title: $scope.selectedClub.originalObject.title
                    color: $scope.selectedClub.originalObject.main_color or getRandomColor()
                    id: $scope.selectedClub.originalObject.pk
                    dataBySeason:
                        results: [{
                            season: lastSeasonResult['season']
                        }]
                console.log results[0].config.url.match("players\/(.*)\/indicators")[1]
                for key of lastSeasonResult
                    if _.contains(ALL_FIELDS, key)
                        averageData = 0
                        _.each results, (result) ->
                            averageData += parseFloat(result.data.results[result.data.results.length - 1][key])
                            return
                        averageData = parseFloat(averageData / results.length).toFixed(3)
                        clubObject.dataBySeason.results[0][key] = averageData
                $scope.clubs.push clubObject
                self.listAvergePlayer()
                return
            return
        return

    $scope.calculateTeamData = () ->
        _.each $scope.clubs, (club) ->
            players = _.filter club.all_players, (player) ->
                return player.line_display.indexOf('Goalkeeper') is -1  and player.selected is true

    this.listAvergePlayer = () ->
        newPlayerIndicatorsData = []
        _.each $scope.clubs, (club) ->
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
        averageClubPlayerIndicatorsChart.draw();
        self.chart = $('#chartdiv').highcharts()

    return
