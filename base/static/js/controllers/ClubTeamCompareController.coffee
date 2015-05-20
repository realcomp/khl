angular.module('Sportomatics').controller 'ClubTeamCompareController', ($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory, $timeout) ->
    self = this;
    this.url = document.getElementById('api-player-indicators').value
    this.clubPk = document.getElementById('team-id').value
    averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart()
    $scope.localeObject = LocaleFactory.selectedLocale
    $scope.setField = averageClubPlayerIndicatorsChart.setField
    $scope.field = averageClubPlayerIndicatorsChart.getField()
    $scope.dataType = averageClubPlayerIndicatorsChart.getDataType()
    $scope.clubs = []
    $scope.clubsWithAddedPlayers = {}
    $scope.clubsWithPlace = {}
    $scope.offenders = true
    $scope.defenders = true
    $scope.currentClubId = 0
    $scope.params = (
        professional: true
    )
    $scope.dataType = 'graph-serial';

    $scope.setDataType = (type, event) ->
        $scope.dataType = type;
        if type is 'graph-radar'
            $timeout(() ->
                $('#params').addClass('display-none')
                $scope.createRadar();
            , 100)
        else
            $timeout(() ->
                $('#params').removeClass('display-none')
                $scope.listAveragePlayer();
            , 100)

    $scope.selectedRadarFields = [{
        field: "goals"
    }, {
        field: "points"
    }, {
        field: "assists"
    }, {
        field: "plus_minus"
    }];
    $scope.$watch('selectedRadarFields', (newval) ->
        if newval and $scope.dataType is 'graph-radar'
            $scope.createRadar()
    , true)

    $scope.setParams = () ->
        $('#regularParams').toggleClass('display-none');
        $('#professionalParams').toggleClass('display-none');
        $('.ui.checkbox-regular').checkbox('uncheck');
        $('.ui.checkbox-professional').checkbox('check');
        return null

    $scope.$on 'field-changed', (newval) ->
        $scope.field = field
        if $scope.clubs.length > 0
            $scope.listAveragePlayer()

    $scope.$on 'tooltip', (value, value2) ->
        $scope.clubTooltips = value2.points.map((point) ->
            return {
                result: point.y
                color: point.series.color
                logo: point.series.logo
                title: point.series.title
            }
        )

    $scope.showPersonalList = () ->
        $('.overlay-black').removeClass('hidden');
        $('#personal-list').removeClass('hidden');
        return null

    $scope.getActiveState = (array) ->
        if _.contains(array, $scope.field)
            return 'active'
        else return ''

    $scope.setSeason = (season) ->
        $scope.season = season

    $scope.setSelectedPlayer = (obj) ->
        if obj? and obj.originalObject?
            $scope.selectedPlayer = obj.originalObject

    $scope.addAverageClubPlayerData = (clubPk) ->
        if not $scope.selectedClub? and not clubPk?
            return
        if $scope.selectedClub? and $scope.selectedClub.originalObject?
            pk = $scope.selectedClub.originalObject.pk
        if not pk?
            if clubPk?
                pk = clubPk
                $scope.selectedClub = (
                    originalObject:
                        title: document.getElementById('team-name-hidden').value
                        pk: clubPk
                        color: null
                        logo: document.getElementById('club-logo').value
                )
            else
                return
        url = $('#club-team-api').val().replace(/(\/)([0-9]+)(\/)/, '/') + pk
        if $scope.season?
            url += '?season=' + $scope.season
        else
            $scope.season = 19
        $http.get(url).success (data, status, headers) ->
            LocaleFactory.setLocale headers()['content-language']
            players = data.all_players = _.filter(data.all_players, (player) ->
                player.line > 1
            )
            queries = []
            _.each players, (player) ->
                player.selected = true
                queries.push $http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season')
                return
            $scope.loader = true
            $q.all(queries).then (results) ->
                $scope.loader = false
                seasonResult = _.find(results[0].data.results, (result) ->
                    return result.season.pk.toString() is $scope.season
                )
                if not seasonResult?
                    seasonResult = _.last results[0].data.results
                clubObject =
                    all_players: data.all_players
                    offender_players: data.offender_players
                    defender_players: data.defender_players
                    title: data.title
                    color: if data.main_color? then data.main_color else CHART_COLORS[$scope.clubs.length]
                    pk: data.pk
                    id: $scope.currentClubId
                    logo: data.logo
                    address: data.address
                    dataBySeason:
                        results: [{
                            season: seasonResult['season']
                        }]
                    results: results
                    seasonResult: seasonResult['season']
                $scope.clubs.push clubObject
                $scope.currentClubId += 1
                $timeout( () ->
                    #if $scope.dataType is 'graph-serial' then $scope.listAveragePlayer()
                    #if $scope.dataType is 'graph-radar' then $scope.createRadar()
                    $scope.listAveragePlayer()
                , 100)
                return
            return
        return

    $scope.addPlayerToClub = (id) ->
        club = _.findWhere($scope.clubs, id: id)
        $q.all([$http.get(self.url.replace('/0/', '/' + $scope.selectedPlayer.pk + '/') + '?group_by=season')]).then (results) ->
            $scope.selectedPlayer.selected = true
            $scope.selectedPlayer.added = true
            club.all_players.push $scope.selectedPlayer
            club.results.push results[0]
            $scope.clubsWithAddedPlayers['club_' + club.id] = true
            $scope.clubsWithPlace['club_' + id] = if _.filter(club.all_players, {selected: false}).length > _.filter(club.all_players, {added: true}).length then true else false
            $scope.listAveragePlayer()

    $scope.togglePlayerSelection = (id, index) ->
        club = _.findWhere($scope.clubs, id: id)
        player = club.all_players[index]
        player.selected = not player.selected
        $scope.clubsWithPlace['club_' + id] = if _.filter(club.all_players, {selected: false}).length > _.filter(club.all_players, {added: true}).length then true else false
        $('#player_'+index).attr('checked', !$('#player_'+index).attr('checked'))
        $scope.listAveragePlayer()

    $scope.listAveragePlayer = () ->
        newPlayerIndicatorsData = []
        _.each $scope.clubs, (club) ->
            #if $scope.defenders is false then for player in club.all_players then if player.line_display is 'Defender' then player.selected = false
            #if $scope.offenders is false then for player in club.all_players then if player.line_display is 'Offender' then player.selected = false
            selectedPlayers = _.countBy(_.filter(club.all_players, (player) ->
                return player.line is 3 and $scope.offenders is true or player.line is 2 and $scope.defenders is true
            ), selected: true)['true']
            for key of _.last club.results[0].data.results #идем по всем показателям, берем их из первого объекта
                if _.contains(ALL_FIELDS, key) #если это поле -- показатель
                    averageData = 0
                    _.each club.results, (result) ->
                        player = _.findWhere(club.all_players, pk: Number(result.config.url.match("players\/(.*)\/indicators")[1]))
                        player.result = _.find(result.data.results, (result) ->
                            return result.season.pk.toString() is club.seasonResult.pk.toString()
                        )[$scope.field]
                        return if player.line is 3 and not $scope.offenders or player.line is 2 and not $scope.defenders
                        if player.selected is true
                            averageData += parseFloat(_.last(result.data.results)[key])
                        return
                    averageData = parseFloat(averageData / selectedPlayers).toFixed(3)
                    club.dataBySeason.results[0][key] = averageData
            clubObject = {
                name: '<span class="bold">' + club.title + '</span><br>' + club.seasonResult.title
                data: club.dataBySeason.results.map (el) ->
                    return (
                        x: new Date("2015").getTime()#new Date(el.season.end_date.split('-')[0]).getTime()
                        y: parseFloat(el[$scope.field])
                        drilldown: el.season.end_date
                    )
                color: club.color,
                stack: club.pk + club.seasonResult.pk
                logo: club.logo
            }
            newPlayerIndicatorsData.push clubObject

        if $scope.dataType is 'graph-serial'
            averageClubPlayerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData)
            averageClubPlayerIndicatorsChart.setContext($scope);
            averageClubPlayerIndicatorsChart.setType('linear')
            averageClubPlayerIndicatorsChart.setPeriod(30);
            averageClubPlayerIndicatorsChart.setPreventLabels(true);
            averageClubPlayerIndicatorsChart.draw()
            self.chart = $('#chartdiv').highcharts()
            legendContent = ''
            _.each newPlayerIndicatorsData, (result) ->
                legendContent += HTML_INDICATORS_LIST_ITEM(parseFloat(result.data[0].y).toFixed(3), result.name, result.logo, result.color)
            $('#legend-content').html(legendContent)
            return null
        else
            $scope.createRadar()

    $scope.createRadar = () ->
        # function to create radar chart for one or multiple players
        categories = $scope.selectedRadarFields.map((el) ->
            el['field']
        )
        #$scope.playerSeasons = $scope.dataBySeason.results.map((e) ->
        #    e.season.end_date.substr 0, 4
        #)        if $scope.clubs.length > 0
        chartData = []
        _.each $scope.clubs, (club, index) ->
            data = club.dataBySeason.results.map((el) ->
                return {
                    name: '<span class="bold">' + club.title + '</span><br>' + club.seasonResult.title
                    data: categories.map((category) ->
                        if category is 'shots'
                            return parseInt(el[category]) / 10 / parseInt(el['count'])
                        parseInt(el[category]) / parseInt(el['count'])
                    )
                    pointPlacement: 'on'
                    color: club.color
                    title: club.title
                    seasonResult: club.seasonResult
                    logo: club.logo
                }
            ).filter((toFilter) ->
                toFilter?
            )
            chartData.push data[0]

        console.log chartData
        $scope.playerStatsSpiderChart = new (HighchartsFactory.PlayerStatsSpiderChart)('chartdiv2', chartData, categories)
        $scope.playerStatsSpiderChart.setContext $scope
        $scope.playerStatsSpiderChart.setLocaleObject $scope.localeObject
        $scope.playerStatsSpiderChart.draw()
        self.spiderChart = $('#chartdiv2').highcharts()
        ### legend ###
        legendContent = ''
        _.each chartData, (result) ->
            legendContent += HTML_INDICATORS_LIST_ITEM(parseFloat(_.last(result.data)).toFixed(3), result.name, result.logo, result.color)
        $('#legend-content').html(legendContent)
        $('#legend-header').html('<span>'+$scope.localeObject.fieldNames[_.last(categories)].fullName+'</span')
        ### legend ###

        return null

    $scope.addAverageClubPlayerData(this.clubPk)

    return
