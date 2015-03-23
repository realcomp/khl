angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location', '$parse',
    ($scope, $http, $location, $parse) ->
        $scope.MONTHS = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
            'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        $scope.data = {}
        $scope.params = $location.search()

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

        $scope.getSchedules = (data) ->
            result = {}
            getDate = $parse('date|date:"yyyy-MM-dd"')
            for s in data
                result[getDate(s)] = s
            return result

        $scope.getCalendar = (year, month, schedules) ->
            daysInM = new Date(year, month + 1, 0).getDate()
            # day of week, shift left because sunday is 0
            startDoW = new Date(year, month, 1).getDay() - 1
            if startDoW < 0
                startDoW = 6

            result = []
            i = 0
            row = []
            strfdate = (date) ->
                y = 1900 + date.getYear()
                m = String(date.getMonth() + 1)
                if m.length < 2
                    m = '0' + m
                d = String(date.getDate())
                if d.length < 2
                    d = '0' + d
                [y, m, d].join('-')
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
                        cell['schedule'] = schedules[strfdate(cell.date)]
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

        $scope.list = () ->
            $scope.params = $location.search()
            params = ''
            if $scope.params.season
                params += '&season=' + $scope.params.season
            $scope.data = {};
            $scope.loaded = false;
            $http.get($scope.url + '?' + params
            ).success((data) ->
                $scope.data = data
                $scope.schedules = $scope.getSchedules(data)
                $scope.calendars = ({
                    'year': 2015,
                    'month': $scope.MONTHS[m],
                    'table': $scope.getCalendar(2015, m, $scope.schedules)
                } for m in [0...3])
                $scope.loaded = true
            )
            return

        return
])
