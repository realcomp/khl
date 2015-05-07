angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory',
    ($scope, $http, $location, $parse, MapService, HighchartsFactory) ->
        $scope.MONTHS = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
            'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        $scope.data = {}
        $scope.params = $location.search()

        $scope.clubName = document.getElementById('team-name-hidden').value
        $scope.clubAddress = if document.getElementById('club-address')? then document.getElementById('club-address').innerHTML else ''
        $scope.clubMatchApi = if document.getElementById('club-match-api')? then document.getElementById('club-match-api').value;
        $scope.clubCalendarApi = $scope.url = if document.getElementById('club-calendar-api')? then document.getElementById('club-calendar-api').value;
        $scope.clubPk = document.getElementById('team-id').value;
        $scope.games = []

        $scope.selection = 'all'
        $scope.setSelecton = (selection) ->
            $scope.selection = selection
            $scope.createGamesChart()

        $scope.CalendarEventPopup = {}
        $scope.CalendarEventPopupShow = (e, event) ->
            if $('.calendar-event-popup:hidden').length and @cell.schedule
                $scope.CalendarEventPopup.data = null
                $scope.CalendarEventPopup.is_home = @cell.schedule.is_home
                $scope.CalendarEventPopup.is_guest = @cell.schedule.is_guest
                params = ''
                if @cell.schedule.is_home
                    params = '?is_home=true'
                if @cell.schedule.is_guest
                    params = '?is_guest=true'
                $http.get($scope.urlPopup.replace(0, @cell.schedule.pk) + params
                ).success((data) ->
                    $scope.CalendarEventPopup.data = data;
                    return
                )
                $('.calendar-event-popup:hidden').show(500).offset({
                    'left': event.pageX,
                    'top': event.pageY,
                })
                return

        $scope.setType = (type) ->
            $location.search('type', type or null)
            $scope.params = $location.search()
            return

        if $scope.params.season
            $('[name="season"]').attr('value', $scope.params.season)

        $scope.setSeason = (e) ->
            $location.search('season', $(e).val())
            $scope.params = $location.search() # don't work
            $scope.list()
            return

        $scope.parseSchedules = (data) ->
            result = {}
            getDate = $parse('date|date:"yyyy-MM-dd"')
            for s in data.results
                result[getDate(s)] = s
            return result

        $scope.getSchedule = (schedules, date) ->
            strfdate = (date) ->
                y = 1900 + date.getYear()
                m = String(date.getMonth() + 1)
                if m.length < 2
                    m = '0' + m
                d = String(date.getDate())
                if d.length < 2
                    d = '0' + d
                [y, m, d].join('-')
            return schedules[strfdate(date)]

        $scope.getCalendar = (date, schedules) ->
            year = date.getYear() + 1900
            month = date.getMonth()
            daysInM = new Date(year, month + 1, 0).getDate()
            # day of week, shift left because sunday is 0
            startDoW = new Date(year, month, 1).getDay() - 1
            if startDoW < 0
                startDoW = 6

            result = []
            i = 0
            row = []
            # last day not in row + infinite loop protection
            # while row.indexOf(daysInM) == -1 and i <= 6
            while i * 7 < daysInM + startDoW and i <= 6
                row = []
                for j in [0...7]
                    cell = {
                        'cell': i * 7 + j,
                    }
                    day = cell.cell - startDoW + 1
                    if 1 <= day <= daysInM
                        cell['date'] = new Date(year, month, day)
                        cell['schedule'] = $scope.getSchedule(schedules, cell.date)
                    row.push(cell)
                result.push(row)
                i += 1

            return result

        $scope.isHome = (cell) ->
            # type is all/home
            return (
                cell.schedule and cell.schedule.is_home and
                $scope.params.type != 'guest')

        $scope.isGuest = (cell) ->
            # type is all/guest
            return (
                cell.schedule and cell.schedule.is_guest and
                $scope.params.type != 'home')

        $scope.getLogo = (cell) ->
            if $scope.isHome(cell)
                return cell.schedule.guest_team.logo
            if $scope.isGuest(cell)
                return cell.schedule.home_team.logo
            return null

        $scope.monthDelta = (date, deltaM) ->
            d = new Date(date)
            d.setDate(1)
            d.setMonth(d.getMonth() + deltaM)
            return d

        $scope.getMinEndDate = (data) ->
            a = new Date()
            b = new Date(data.season.end_date)
            if a < b
                return a
            else
                return b

        $scope.list = () ->
            $scope.params = $location.search()
            params = ''
            if $scope.params.season
                params += '&season=' + $scope.params.season
            else
                params += '&season=19'
            $scope.data = {};
            $scope.loaded = false;

            $http.get($scope.url + '?' + params
            ).success((data) ->
                console.log data
                MapService.remove() if MapService.isRendered()
                MapService.createClubsMap(data.results, 'trips') if $('#clubs-map').length > 0
                $scope.data = data
                $scope.schedules = $scope.parseSchedules(data)
                date = $scope.getMinEndDate(data)
                $scope.calendars = [({
                    'date': $scope.monthDelta(date, deltaM),
                    'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                    'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
                } for deltaM in [-1, 0, 1])]
                $scope.loaded = true
            )
            return $scope.createGamesChart()

        $scope.createGamesChart = () ->
            params = ''
            params += '?club='+$scope.clubPk
            if $scope.params.season
                params += '&season=' + $scope.params.season
            $http.get($scope.clubMatchApi + params)
                .success (data) ->
                    $scope.games = _.sortBy(data, (el) ->
                        return new Date(el).getTime()
                    ).reverse()
                    seriesClub = {}
                    seriesOpponent = {}
                    opponentObject = (
                        name: 'opponents'
                        data: $scope.games.map((game, index) ->
                            if $scope.selection is 'home' and game.is_home is false then return
                            if $scope.selection is 'guest' and game.is_home is true then return
                            return (
                                x: index
                                y: -Math.abs(game.opponent_score)
                                date: game.date
                                name: game.opponent.title_verbose + ' - ' + $scope.clubName + ' ' + $scope.clubAddress
                                score: Math.abs(game.opponent_score) + ' : ' + Math.abs(game.score)
                                color: if (Math.abs(game.opponent_score) > Math.abs(game.score)) then '#e74c3c' else '#2ecc71'
                                #dataLabels:
                                    #enabled: true
                                    #align: 'center'
                                    #verticalAlign: 'bottom'
                                    #rotation: 270
                                    #inside: true
                                    #x: -2
                                    #y: 70
                                    #formatter: () ->
                                    #    return this.key.split('-')[0]
                            )
                        ).filter (toFilter) ->
                            return toFilter?
                    )
                    clubObject = (
                        name: 'club'
                        data: $scope.games.map((game, index) ->
                            if $scope.selection is 'home' and game.is_home is false then return
                            if $scope.selection is 'guest' and game.is_home is true then return
                            opponentAddress = if game.opponent.address and game.opponent.address.title then game.opponent.address.title else ''
                            return (
                                x: index
                                y: game.score
                                date: game.date
                                name: $scope.clubName + ' ' + $scope.clubAddress + ' - ' + game.opponent.title_verbose
                                score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score)
                                color: if (Math.abs(game.opponent_score) > Math.abs(game.score)) then '#e74c3c' else '#2ecc71'
                            )
                        ).filter (toFilter) ->
                            return toFilter?
                    )
                    clubGamesChart = new HighchartsFactory.ClubGamesChart 'chartdiv', [clubObject, opponentObject]
                    clubGamesChart.draw()

        $scope.previous = () ->
            date = $scope.calendars[$scope.calendars.length - 1][0].date
            $scope.calendars.push({
                'date': $scope.monthDelta(date, deltaM),
                'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
            } for deltaM in [-3, -2, -1])

        $scope.list()

        return
])
