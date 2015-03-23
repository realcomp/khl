angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location',
    ($scope, $http, $location) ->
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

        $scope.getCalendar = (year, month) ->
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
                    cell = i * 7 + j
                    day = cell - startDoW + 1
                    date = null
                    if 1 <= day <= daysInM
                        date = new Date(year, month, day)
                    row.push({
                        'cell': cell,
                        'date': date,
                    })
                result.push(row)
                i += 1

            return result

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
                $scope.calendars = ({
                    'year': 2015,
                    'month': $scope.MONTHS[m],
                    'table': $scope.getCalendar(2015, m)
                } for m in [0...3])
                $scope.loaded = true
            )
            return

        return
])
