angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory',
    ($scope, $http, $location, $parse, MapService, HighchartsFactory) ->
        $scope.MONTHS = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
            'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        $scope.data = {}
        $scope.params = $location.search()

        $scope.club = 'wdq'
        $scope.games = [{
                is_home: false
                date: '2010-07-01'
                opponent:
                    pk: 1
                    title: 'Металлург'
                    logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif'
                    score: -4
                score: 5
            },
            {
                is_home: false
                date: '2010-07-02'
                opponent:
                    pk:1
                    title: 'СКА'
                    logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif'
                    score: -3
                score: 2
            },
            {
                is_home: false
                date: '2010-07-03'
                opponent:
                    pk:1
                    title: 'Авангард',
                    logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif'
                    score: -3
                score: 7
            },
            {
                is_home: false
                date: '2010-07-07'
                opponent:
                    pk:1
                    title: 'ХК Сочи'
                    logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif'
                    score: -4
                score: 2
            }
        ]

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
            $scope.data = {};
            $scope.loaded = false;

            $http.get($scope.url + '?' + params
            ).success((data) ->
                console.log data
                MapService.remove() if MapService.isRendered()
                MapService.createClubsMap(data.results, 'trips')
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
            seriesClub = {}
            seriesOpponent = {}
            opponentObject = (
                name: 'opponents'
                data: $scope.games.map (game, index) ->
                    return (
                        x: index
                        y: game.opponent.score,
                        date: game.date
                        name: game.opponent.title + ' - Club'
                        score: Math.abs(game.opponent.score) + ' : ' + Math.abs(game.score)
                        color: if (Math.abs(game.opponent.score) > Math.abs(game.score)) then '#FF0000' else 'green',
                        dataLabels:
                            enabled: true
                            align: 'center'
                            crop: false
                            verticalAlign: 'bottom'
                            y: 25
                            formatter: () ->
                                console.log this
                                return this.key.split('-')[0]
                            inside: false
                    )#[new Date(game.date.split('-')).getTime(), game.opponent.score]
            )
            clubObject = (
                name: 'club'
                data: $scope.games.map (game, index) ->
                    return (
                        x: index
                        y: game.score
                        date: game.date
                        name: 'Club - ' + game.opponent.title
                        score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent.score)
                        color: if (Math.abs(game.opponent.score) > Math.abs(game.score)) then '#FF0000' else 'green'
                    )#[new Date(game.date.split('-')).getTime(), game.score]
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

        return
])
