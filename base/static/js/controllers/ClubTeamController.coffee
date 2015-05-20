angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout', 'MapService',
    ($http, $scope, $timeout, MapService) ->
        url = document.getElementById("club-team-api").value
        popup = null
        $scope.type = 'all'
        $scope.cache_players = null
        $scope.cache_clubs = null
        $scope.notplaying_players = null
        $scope.state = 'fio'
        $scope.order_by = 'lastname'
        $scope.season = 19
        $scope.seasons = []

        $scope.setOrderBy = (order_by) ->
            if $scope.order_by == order_by
                if $scope.order_by.indexOf('-') > -1
                    $scope.order_by = $scope.order_by.replace('-', '')
                else
                    $scope.order_by = '-' + $scope.order_by
            else
                $scope.order_by = order_by
            return

        $scope.setType = (type) ->
            $scope.type = type
            $scope.unMakeTransferArrows()
            return

        $scope.setState = (state) ->
            $scope.state = state
            $scope.getFromCache()
            # //if($scope.state = 'is_joined'){
            # //    $timeout(function(){
            # //        $scope.makeTransferArrows();
            # //    }, 500)
            # //}
            return

        $scope.playerFilter = (value) ->
            if $scope.state == 'coaches'
                return false
            return value[$scope.state] != false

        $scope.go = (path) ->
            window.location.href = path
            return

        $scope.PlayerPartnersPopup = {
            'data': null,
            'isClubsVisible': true,
        }

        $scope.PlayerPartnersPopupShow = (e, event) ->
            popup = $('.player-partners-popup:hidden')
            url = $('#PlayerCardLink').attr('href')
            if popup.length and this.cell_id[0] != 'trainer'
                pk = $scope.getCell(self.players, this.cell_id).pk
                $scope.PlayerPartnersPopup.data = null
                $http.get(url.replace(0, pk)
                ).success((data) ->
                    $scope.PlayerPartnersPopup.data = data
                )
                $('.player-partners-popup:hidden').show(500).offset({
                    'left': event.pageX,
                    'top': event.pageY,
                })
            return

        $scope.players = {}
        $scope.clubs = {
            'getLastClub': () ->
                if $scope.clubs.length
                    return $scope.clubs[$scope.clubs.length - 1]
                return
            'clubs': [],
        }

        $scope.setSeason = (season, push) ->
            $scope.season = season
            $scope.list(push)
            return

        $scope.getCell = (table, cell_id) ->
            if table.table and cell_id and Array.isArray(cell_id) and cell_id[1] != null
                group = table.table[cell_id[0]]
                if group
                    return group[cell_id[1]]
            return

        $scope.isPersonVisible = (table, cell_id) ->
            cell = $scope.getCell(table, cell_id)
            if cell
                switch self.players.status
                    when 'joined'
                        return cell.is_joined
                    when 'left'
                        return cell.is_left
                    when 'legionnaire'
                        return cell.is_legionnaire
                    when 'home'
                        return cell.is_home
                    else
                        return true
            return false

        $scope.isPersonInCell = (table, cell_id) ->
            cell = $scope.getCell(table, cell_id)
            return cell

        $scope.list = (push) ->
            params = 'season=' + $scope.season
            $scope.loaded = false
            $http.get(url + '?' + params
            ).success((data) ->
                if push
                    title = ''
                    if document.getElementById('season_' + $scope.season) != null
                        title = document.getElementById('season_' + $scope.season).value
                    $scope.seasons.push({
                        'players': data,
                        'season': $scope.season,
                        'title': title,
                    })
                else
                    title = ''
                    if document.getElementById('season_' + $scope.season) != null
                        title = document.getElementById('season_' + $scope.season).value
                    $scope.seasons = [{
                        'players': data,
                        'season': $scope.season,
                        'title': title,
                    }]
                $scope.players = data
                $scope.loaded = true
                return
            )
            return

        $scope.compare = (arg) ->
            url = $('#ClubTeamCompareLink').attr('href')
            club = self.clubs.getLastClub()
            if club
                params = 'source_season=' + club.data.season.pk
                params += '&season=' + club.data.prev_season.pk
            else
                params = 'source_season=' + $scope.players.data.season.pk
                params += '&season=' + $scope.players.data.prev_season.pk
            $scope.clubs.loader = true
            $http.get(url + '?' + params
            ).success((data) ->
                if data.leagues.length
                    clubRows = []
                    clubsInRow = []
                    clubs = []
                    $scope.clubplayers = []
                    _.each(data.leagues, (league, index) ->
                        clubs = clubs.concat(league.clubs)
                        $scope.clubplayers = $scope.clubplayers.concat(league.clubplayers)
                        return
                    )
                    _.each(clubs, (club, index) ->
                        if clubsInRow.length < 7
                            clubsInRow.push(club)
                        if index == clubs.length -1 or (index + 1) % 7 == 0
                            clubRows.push(clubsInRow)
                            clubsInRow = []
                        return
                    )
                    clubsObject = {
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs,
                        },
                        'league': data.leagues[0],
                        'clubRows': clubRows,
                    }
                    self.clubs.clubs.push(clubsObject)
                $scope.clubs.loader = false
                return
            )

        $scope.getFromCache = () ->
            if ($scope.cache_players)
                $scope.players = $scope.cache_players
                $scope.clubs = $scope.cache_clubs
            return

        $scope.makeTransferArrows = () ->
            $scope.getFromCache()
            _.each($scope.clubplayers, (clubplayer) ->
                createTransferArrow(
                    '#club_' + clubplayer.club,
                    '#player_' + clubplayer.player, clubplayer.pk)
                return
            )
            $('.player-item').each(() ->
                if(!_.findWhere($scope.clubplayers,
                        {'player': parseInt($(this).attr('id').split('_')[1])}))
                    $(this).addClass('opacity-30')
                else
                    id = $(this).attr('id')
                    $(this).hover(
                        () ->
                            $('canvas').each(() ->
                                if $(this).attr('player') != id
                                    $(this).addClass('opacity-10')
                                return
                            )
                        ,() ->
                            $("canvas").each(() ->
                                $(this).removeClass("opacity-10")
                                return
                            )
                    )
                return
            )

        $scope.unMakeTransferArrows = () ->
            $scope.getFromCache()
            $('canvas').remove()
            $('.player-item').each(() ->
                $(this).removeClass("opacity-30")
            )

        $scope.notPlayingNow = (callback, callbackArg) ->
            $scope.setState('fio')
            $scope.unMakeTransferArrows()
            $scope.players.loader = true
            if $scope.notplaying_players
                $scope.players = $scope.notplaying_players
            else
                $http.get(url + '?notplaying=1'
                ).success((data) ->
                    $scope.cache_players = $scope.players
                    $scope.cache_clubs = $scope.clubs
                    $scope.players = data
                    $scope.players.data = data
                    $scope.players.table = {
                        'goalkeeper': data.goalkeeper_players,
                        'defender': data.defender_players,
                        'forward': data.offender_players,
                        'trainer': data.coaches,
                    }
                    $scope.notplaying_players = $scope.players
                )
            $scope.workWithData($scope.players)
            $scope.players.loader = false
            if typeof callback == 'function'
                callback(callbackArg)

        $scope.list()

        $('.b-tabs-content').visibility({
            'once': false,
            'observeChanges': true,
            'onBottomVisible': () ->
                newSeason = 1
                if $scope.seasons.length > 0 and fromSeason($scope.season) != 1997
                    $scope.setSeason(toSeason(fromSeason($scope.season) - 1), true)
        })

        return
])
