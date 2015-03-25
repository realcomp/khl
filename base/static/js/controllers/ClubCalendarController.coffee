angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location', '$parse',
    ($scope, $http, $location, $parse) ->
        $scope.MONTHS = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
            'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        $scope.data = {}
        $scope.params = $location.search()

        $scope.CalendarEventPopup = {}
        $scope.CalendarEventPopupShow = (e, event) ->
            if $('.calendar-event-popup:hidden').length and this.cell.schedule
                $scope.CalendarEventPopup.data = null
                $scope.CalendarEventPopup.is_home = this.cell.schedule.is_home
                $scope.CalendarEventPopup.is_guest = this.cell.schedule.is_guest
                params = ''
                if this.cell.schedule.is_home
                    params = '?is_home=true'
                if this.cell.schedule.is_guest
                    params = '?is_guest=true'
                $http.get($scope.urlPopup.replace(0, this.cell.schedule.pk) + params
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
            return

        $scope.previous = () ->
            date = $scope.calendars[$scope.calendars.length - 1][0].date
            $scope.calendars.push({
                'date': $scope.monthDelta(date, deltaM),
                'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
            } for deltaM in [-3, -2, -1])

        return
])
