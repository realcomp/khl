angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory', '$timeout',
    ($scope, $http, $location, $parse, MapService, HighchartsFactory, $timeout) ->
        $scope.MONTHS = [
            'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль',
            'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        $scope.MONTHS_ROD = [
            'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля',
            'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
        $scope.data = {}
        $scope.params = $location.search()
        $scope.gameDaysOnly = false

        $scope.clubName = document.getElementById('team-name-hidden').value
        $scope.clubAddress = if document.getElementById('club-address')? then document.getElementById('club-address').innerHTML else ''
        $scope.clubMatchApi = if document.getElementById('club-match-api')? then document.getElementById('club-match-api').value;
        $scope.clubCalendarApi = $scope.url = if document.getElementById('club-calendar-api')? then document.getElementById('club-calendar-api').value;
        $scope.clubPk = document.getElementById('team-id').value;
        $scope.clubLogo = document.getElementById('club-logo').value
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

        $scope.getCalendarDays = (date, schedules) ->
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
                result.push (cell: 'empty')
                for j in [0...7]
                    cell = {
                        'cell': i * 7 + j,
                    }
                    day = cell.cell - startDoW + 1
                    if 1 <= day <= daysInM
                        cellDate = new Date(year, month, day)
                        cell['date'] = cellDate
                        cell['schedule'] = $scope.getSchedule(schedules, cell.date)
                        if cell['schedule']?
                            cell['schedule']['formattedDate'] = new Date(cell['schedule']['date']).ddmmFormatted()
                    row.push(cell)
                    result.push cell
                #result.push(row)
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
            if a.getTime() < b.getTime()
                return a
            else
                return b

        $scope.list = () ->
            $scope.wholeSeason = false
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
                MapService.remove() if MapService.isRendered()
                MapService.createClubsMap(data.results, 'trips') if $('#clubs-map').length > 0
                $scope.data = data
                $scope.schedules = $scope.parseSchedules(data)
                date = $scope.getMinEndDate(data)
                array = []
                if date isnt (new Date(data.season.end_date))
                    countToEnd = new Date($scope.data.season.end_date).getMonth() - date.getMonth()
                    i = 0
                    while i < countToEnd
                        array.push i
                        i++
                $scope.calendars = []
                _.each array, (deltaM) ->
                    table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules)
                    gamesInMonth = _.filter table, (cell) ->
                        cell.schedule?
                    if gamesInMonth.length > 0
                        $scope.calendars.push
                            'date': $scope.monthDelta(date, deltaM)
                            'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                            'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()]
                            'table': table
                $scope.loaded = true
                if $scope.calendars.length is 0
                    $scope.noGames = true
            )
            if $('#clubGamesChart').length is 0 then return
            return $scope.createGamesChart()

        $scope.createGamesChart = () ->
            params = ''
            params += '?club='+$scope.clubPk
            if $scope.params.season
                params += '&season=' + $scope.params.season
            else
                params += '&season=19'
            $scope.loaded = false
            $http.get($scope.clubMatchApi + params)
                .success (data) ->
                    data = [{"id":36733,"date":"2015-02-24T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":92,"title_verbose":"Динамо Мн (Минск)","url":"/ru/hockey/clubs/92/","logo":"/media/filer_public/87/76/87765483-7780-4371-bd60-3adc68aa0859/dinamo-mn.gif","address":{"pk":60,"title":"Минск"},"title":"Динамо Мн"},"score":3,"opponent_score":1,"is_home":true,"spectators":5136,"arena_capacity":8512,"arena_capacity_rate":0.6033834586466166,"capacity_rate_average":0.7654664003759398},{"id":36721,"date":"2015-02-22T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":10,"title_verbose":"Торпедо (Нижний Новгород)","url":"/ru/hockey/clubs/10/","logo":"/media/filer_public/5b/2f/5b2f77a1-8172-4f03-9135-1c441b3a0965/bbfce1c18b92b3ccc5091f10a20a731b.jpg","address":{"pk":8,"title":"Нижний Новгород"},"title":"Торпедо"},"score":2,"opponent_score":3,"is_home":true,"spectators":6705,"arena_capacity":8512,"arena_capacity_rate":0.7877114661654135,"capacity_rate_average":0.7654664003759398},{"id":36686,"date":"2015-02-20T16:30:00Z","overtime_win":true,"bullet_win":false,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":2,"opponent_score":1,"is_home":true,"spectators":7763,"arena_capacity":8512,"arena_capacity_rate":0.9120065789473685,"capacity_rate_average":0.7654664003759398},{"id":36673,"date":"2015-02-18T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":9,"title_verbose":"Северсталь (Череповец)","url":"/ru/hockey/clubs/9/","logo":"/media/filer_public/74/96/7496f393-089b-4859-95f4-50c2e10ed839/4919a0b4f92b29a921dbfa5cfdef450e.jpg","address":{"pk":7,"title":"Череповец"},"title":"Северсталь"},"score":1,"opponent_score":3,"is_home":true,"spectators":4567,"arena_capacity":8512,"arena_capacity_rate":0.5365366541353384,"capacity_rate_average":0.7654664003759398},{"id":36662,"date":"2015-02-15T14:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":2,"opponent_score":0,"is_home":false,"spectators":5600,"arena_capacity":8512,"arena_capacity_rate":0.6578947368421053,"capacity_rate_average":0.7654664003759398},{"id":36650,"date":"2015-02-13T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":12,"title_verbose":"Локомотив (Ярославль)","url":"/ru/hockey/clubs/12/","logo":"/media/filer_public/fb/ee/fbeeed12-5e22-43e4-b08e-dedd18cc60bc/2cf68953c6cd4fabe9285a28a5b3267a.jpg","address":{"pk":10,"title":"Ярославль"},"title":"Локомотив"},"score":3,"opponent_score":4,"is_home":false,"spectators":9007,"arena_capacity":8512,"arena_capacity_rate":1.0581531954887218,"capacity_rate_average":0.7654664003759398},{"id":36638,"date":"2015-02-11T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":20,"title_verbose":"Витязь (Московская область)","url":"/ru/hockey/clubs/20/","logo":"/media/filer_public/82/7e/827e82a7-7611-4a37-b344-774a6420ddf9/97c602120c26bffddf2ce5779921cd94.jpg","address":{"pk":46,"title":"Московская область"},"title":"Витязь"},"score":6,"opponent_score":3,"is_home":false,"spectators":4600,"arena_capacity":8512,"arena_capacity_rate":0.5404135338345865,"capacity_rate_average":0.7654664003759398},{"id":36628,"date":"2015-02-09T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":53,"title_verbose":"Йокерит (Хельсинки)","url":"/ru/hockey/clubs/53/","logo":"/media/filer_public/4b/f6/4bf62f62-5bea-49da-b138-9bf788bd72cf/a78704a94b9f8c9adb73ab3fcb533f65.jpg","address":{"pk":97,"title":"Хельсинки"},"title":"Йокерит"},"score":2,"opponent_score":1,"is_home":false,"spectators":13396,"arena_capacity":8512,"arena_capacity_rate":1.5737781954887218,"capacity_rate_average":0.7654664003759398},{"id":36473,"date":"2015-02-03T16:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":17,"title_verbose":"Ак Барс (Казань)","url":"/ru/hockey/clubs/17/","logo":"/media/filer_public/84/0c/840c37b0-8e28-448b-b0f3-faeea77291f1/89eec748745b21cb5cd68131a21a9718.jpg","address":{"pk":14,"title":"Казань"},"title":"Ак Барс"},"score":4,"opponent_score":1,"is_home":false,"spectators":7427,"arena_capacity":8512,"arena_capacity_rate":0.8725328947368421,"capacity_rate_average":0.7654664003759398},{"id":36451,"date":"2015-02-01T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":20,"title_verbose":"Витязь (Московская область)","url":"/ru/hockey/clubs/20/","logo":"/media/filer_public/82/7e/827e82a7-7611-4a37-b344-774a6420ddf9/97c602120c26bffddf2ce5779921cd94.jpg","address":{"pk":46,"title":"Московская область"},"title":"Витязь"},"score":3,"opponent_score":2,"is_home":true,"spectators":6022,"arena_capacity":8512,"arena_capacity_rate":0.7074718045112782,"capacity_rate_average":0.7654664003759398},{"id":36417,"date":"2015-01-30T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":12,"title_verbose":"Локомотив (Ярославль)","url":"/ru/hockey/clubs/12/","logo":"/media/filer_public/fb/ee/fbeeed12-5e22-43e4-b08e-dedd18cc60bc/2cf68953c6cd4fabe9285a28a5b3267a.jpg","address":{"pk":10,"title":"Ярославль"},"title":"Локомотив"},"score":1,"opponent_score":0,"is_home":true,"spectators":7631,"arena_capacity":8512,"arena_capacity_rate":0.896499060150376,"capacity_rate_average":0.7654664003759398},{"id":36381,"date":"2015-01-28T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":56,"title_verbose":"ХК Сочи (Сочи)","url":"/ru/hockey/clubs/56/","logo":"/media/filer_public/21/13/2113fc87-7fe4-4371-8371-521f2568bd56/4a39e817291e2e8d0fdef66c76f31fbd.jpg","address":{"pk":124,"title":"Сочи"},"title":"ХК Сочи"},"score":3,"opponent_score":0,"is_home":true,"spectators":4951,"arena_capacity":8512,"arena_capacity_rate":0.5816494360902256,"capacity_rate_average":0.7654664003759398},{"id":36153,"date":"2015-01-22T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":18,"title_verbose":"Нефтехимик (Нижнекамск)","url":"/ru/hockey/clubs/18/","logo":"/media/filer_public/aa/65/aa65da5d-c919-466a-a32a-4c46802f4c0a/873a6498c0d793f9ab988e02ad3afb6d.jpg","address":{"pk":15,"title":"Нижнекамск"},"title":"Нефтехимик"},"score":2,"opponent_score":0,"is_home":true,"spectators":4220,"arena_capacity":8512,"arena_capacity_rate":0.4957706766917293,"capacity_rate_average":0.7654664003759398},{"id":36139,"date":"2015-01-20T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":16,"title_verbose":"Лада (Тольятти)","url":"/ru/hockey/clubs/16/","logo":"/media/filer_public/b5/d6/b5d695ee-7ded-4e9d-8461-53785e174716/eb0c02803b9e72c0b25545e04d530062.jpg","address":{"pk":13,"title":"Тольятти"},"title":"Лада"},"score":1,"opponent_score":2,"is_home":true,"spectators":4765,"arena_capacity":8512,"arena_capacity_rate":0.5597979323308271,"capacity_rate_average":0.7654664003759398},{"id":36124,"date":"2015-01-17T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":55,"title_verbose":"Слован (Братислава)","url":"/ru/hockey/clubs/55/","logo":"/media/filer_public/95/1f/951f697c-f20c-4f06-8ff9-8be4de117766/58fd2a739bb9dc9190231af6a7bac575.jpg","address":{"pk":91,"title":"Братислава"},"title":"Слован"},"score":2,"opponent_score":0,"is_home":false,"spectators":10055,"arena_capacity":8512,"arena_capacity_rate":1.1812734962406015,"capacity_rate_average":0.7654664003759398},{"id":36117,"date":"2015-01-15T17:30:00Z","overtime_win":true,"bullet_win":false,"opponent":{"id":54,"title_verbose":"Медвешчак (Загреб)","url":"/ru/hockey/clubs/54/","logo":"/media/filer_public/19/61/19617583-c6aa-4b65-a158-955ab7c9dc6a/e11c30916343c60e685e3ae82d6076b2.jpg","address":{"pk":107,"title":"Загреб"},"title":"Медвешчак"},"score":4,"opponent_score":3,"is_home":false,"spectators":5000,"arena_capacity":8512,"arena_capacity_rate":0.5874060150375939,"capacity_rate_average":0.7654664003759398},{"id":36106,"date":"2015-01-13T16:00:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":92,"title_verbose":"Динамо Мн (Минск)","url":"/ru/hockey/clubs/92/","logo":"/media/filer_public/87/76/87765483-7780-4371-bd60-3adc68aa0859/dinamo-mn.gif","address":{"pk":60,"title":"Минск"},"title":"Динамо Мн"},"score":2,"opponent_score":3,"is_home":false,"spectators":15086,"arena_capacity":8512,"arena_capacity_rate":1.7723214285714286,"capacity_rate_average":0.7654664003759398},{"id":35905,"date":"2015-01-10T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":51,"title_verbose":"Атлант (Московская область)","url":"/ru/hockey/clubs/51/","logo":"/media/filer_public/73/7c/737c2572-7c22-46e1-b0e1-e0b9cc1d3def/6c1a7394af880566b4b4afdb003df140.jpg","address":{"pk":46,"title":"Московская область"},"title":"Атлант"},"score":3,"opponent_score":2,"is_home":false,"spectators":6700,"arena_capacity":8512,"arena_capacity_rate":0.787124060150376,"capacity_rate_average":0.7654664003759398},{"id":35893,"date":"2015-01-08T11:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":5,"title_verbose":"Авангард (Омская область)","url":"/ru/hockey/clubs/5/","logo":"/media/filer_public/f1/56/f1563eef-103d-4d69-ba6b-31c4cb74337b/6a4532ecbbf83bbf5e44ec91f004df02.jpg","address":{"pk":5,"title":"Омская область"},"title":"Авангард"},"score":7,"opponent_score":3,"is_home":false,"spectators":10300,"arena_capacity":8512,"arena_capacity_rate":1.2100563909774436,"capacity_rate_average":0.7654664003759398},{"id":35882,"date":"2015-01-05T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":0,"opponent_score":1,"is_home":false,"spectators":5600,"arena_capacity":8512,"arena_capacity_rate":0.6578947368421053,"capacity_rate_average":0.7654664003759398},{"id":35862,"date":"2014-12-28T14:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":11,"title_verbose":"СКА (Санкт-Петербург)","url":"/ru/hockey/clubs/11/","logo":"/media/filer_public/7b/2e/7b2e111f-27a1-4cfd-a181-d17fa08542a4/74515728fdbe9c39b803d8c970a06dfb.jpg","address":{"pk":9,"title":"Санкт-Петербург"},"title":"СКА"},"score":2,"opponent_score":1,"is_home":false,"spectators":12257,"arena_capacity":8512,"arena_capacity_rate":1.439967105263158,"capacity_rate_average":0.7654664003759398},{"id":35851,"date":"2014-12-26T16:30:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":10,"title_verbose":"Торпедо (Нижний Новгород)","url":"/ru/hockey/clubs/10/","logo":"/media/filer_public/5b/2f/5b2f77a1-8172-4f03-9135-1c441b3a0965/bbfce1c18b92b3ccc5091f10a20a731b.jpg","address":{"pk":8,"title":"Нижний Новгород"},"title":"Торпедо"},"score":1,"opponent_score":2,"is_home":false,"spectators":5200,"arena_capacity":8512,"arena_capacity_rate":0.6109022556390977,"capacity_rate_average":0.7654664003759398},{"id":33460,"date":"2014-12-24T16:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":9,"title_verbose":"Северсталь (Череповец)","url":"/ru/hockey/clubs/9/","logo":"/media/filer_public/74/96/7496f393-089b-4859-95f4-50c2e10ed839/4919a0b4f92b29a921dbfa5cfdef450e.jpg","address":{"pk":7,"title":"Череповец"},"title":"Северсталь"},"score":2,"opponent_score":5,"is_home":false,"spectators":2600,"arena_capacity":8512,"arena_capacity_rate":0.30545112781954886,"capacity_rate_average":0.7654664003759398},{"id":33445,"date":"2014-12-14T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":2,"opponent_score":1,"is_home":false,"spectators":5600,"arena_capacity":8512,"arena_capacity_rate":0.6578947368421053,"capacity_rate_average":0.7654664003759398},{"id":33432,"date":"2014-12-12T16:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":56,"title_verbose":"ХК Сочи (Сочи)","url":"/ru/hockey/clubs/56/","logo":"/media/filer_public/21/13/2113fc87-7fe4-4371-8371-521f2568bd56/4a39e817291e2e8d0fdef66c76f31fbd.jpg","address":{"pk":124,"title":"Сочи"},"title":"ХК Сочи"},"score":6,"opponent_score":1,"is_home":false,"spectators":9112,"arena_capacity":8512,"arena_capacity_rate":1.0704887218045114,"capacity_rate_average":0.7654664003759398},{"id":33401,"date":"2014-12-07T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":11,"title_verbose":"СКА (Санкт-Петербург)","url":"/ru/hockey/clubs/11/","logo":"/media/filer_public/7b/2e/7b2e111f-27a1-4cfd-a181-d17fa08542a4/74515728fdbe9c39b803d8c970a06dfb.jpg","address":{"pk":9,"title":"Санкт-Петербург"},"title":"СКА"},"score":2,"opponent_score":1,"is_home":true,"spectators":8009,"arena_capacity":8512,"arena_capacity_rate":0.9409069548872181,"capacity_rate_average":0.7654664003759398},{"id":33398,"date":"2014-12-05T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":55,"title_verbose":"Слован (Братислава)","url":"/ru/hockey/clubs/55/","logo":"/media/filer_public/95/1f/951f697c-f20c-4f06-8ff9-8be4de117766/58fd2a739bb9dc9190231af6a7bac575.jpg","address":{"pk":91,"title":"Братислава"},"title":"Слован"},"score":7,"opponent_score":2,"is_home":true,"spectators":4672,"arena_capacity":8512,"arena_capacity_rate":0.5488721804511278,"capacity_rate_average":0.7654664003759398},{"id":33391,"date":"2014-12-03T16:30:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":54,"title_verbose":"Медвешчак (Загреб)","url":"/ru/hockey/clubs/54/","logo":"/media/filer_public/19/61/19617583-c6aa-4b65-a158-955ab7c9dc6a/e11c30916343c60e685e3ae82d6076b2.jpg","address":{"pk":107,"title":"Загреб"},"title":"Медвешчак"},"score":2,"opponent_score":3,"is_home":true,"spectators":4107,"arena_capacity":8512,"arena_capacity_rate":0.4824953007518797,"capacity_rate_average":0.7654664003759398},{"id":33378,"date":"2014-12-01T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":10,"title_verbose":"Торпедо (Нижний Новгород)","url":"/ru/hockey/clubs/10/","logo":"/media/filer_public/5b/2f/5b2f77a1-8172-4f03-9135-1c441b3a0965/bbfce1c18b92b3ccc5091f10a20a731b.jpg","address":{"pk":8,"title":"Нижний Новгород"},"title":"Торпедо"},"score":5,"opponent_score":3,"is_home":true,"spectators":4221,"arena_capacity":8512,"arena_capacity_rate":0.49588815789473684,"capacity_rate_average":0.7654664003759398},{"id":33364,"date":"2014-11-29T14:30:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":3,"opponent_score":4,"is_home":true,"spectators":8125,"arena_capacity":8512,"arena_capacity_rate":0.9545347744360902,"capacity_rate_average":0.7654664003759398},{"id":33344,"date":"2014-11-24T16:30:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":51,"title_verbose":"Атлант (Московская область)","url":"/ru/hockey/clubs/51/","logo":"/media/filer_public/73/7c/737c2572-7c22-46e1-b0e1-e0b9cc1d3def/6c1a7394af880566b4b4afdb003df140.jpg","address":{"pk":46,"title":"Московская область"},"title":"Атлант"},"score":3,"opponent_score":2,"is_home":true,"spectators":4487,"arena_capacity":8512,"arena_capacity_rate":0.5271381578947368,"capacity_rate_average":0.7654664003759398},{"id":33317,"date":"2014-11-19T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":59,"title_verbose":"Югра (Ханты-Мансийск)","url":"/ru/hockey/clubs/59/","logo":"/media/filer_public/2e/fa/2efaf518-8c60-4236-b12a-0515014ed423/7d3df77462524aa8184d721aa2f632d3.jpg","address":{"pk":61,"title":"Ханты-Мансийск"},"title":"Югра"},"score":4,"opponent_score":1,"is_home":true,"spectators":4452,"arena_capacity":8512,"arena_capacity_rate":0.5230263157894737,"capacity_rate_average":0.7654664003759398},{"id":33303,"date":"2014-11-16T15:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":91,"title_verbose":"Динамо Р (Рига)","url":"/ru/hockey/clubs/91/","logo":"/media/filer_public/2b/56/2b56f66e-55b7-4c52-9075-19bac874f7af/dinamo-r.gif","address":{"pk":59,"title":"Рига"},"title":"Динамо Р"},"score":1,"opponent_score":3,"is_home":false,"spectators":8790,"arena_capacity":8512,"arena_capacity_rate":1.0326597744360901,"capacity_rate_average":0.7654664003759398},{"id":33283,"date":"2014-11-12T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":11,"title_verbose":"СКА (Санкт-Петербург)","url":"/ru/hockey/clubs/11/","logo":"/media/filer_public/7b/2e/7b2e111f-27a1-4cfd-a181-d17fa08542a4/74515728fdbe9c39b803d8c970a06dfb.jpg","address":{"pk":9,"title":"Санкт-Петербург"},"title":"СКА"},"score":4,"opponent_score":1,"is_home":false,"spectators":12295,"arena_capacity":8512,"arena_capacity_rate":1.4444313909774436,"capacity_rate_average":0.7654664003759398},{"id":33274,"date":"2014-11-10T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":20,"title_verbose":"Витязь (Московская область)","url":"/ru/hockey/clubs/20/","logo":"/media/filer_public/82/7e/827e82a7-7611-4a37-b344-774a6420ddf9/97c602120c26bffddf2ce5779921cd94.jpg","address":{"pk":46,"title":"Московская область"},"title":"Витязь"},"score":1,"opponent_score":0,"is_home":false,"spectators":4200,"arena_capacity":8512,"arena_capacity_rate":0.4934210526315789,"capacity_rate_average":0.7654664003759398},{"id":33260,"date":"2014-11-06T16:30:00Z","overtime_win":true,"bullet_win":false,"opponent":{"id":5,"title_verbose":"Авангард (Омская область)","url":"/ru/hockey/clubs/5/","logo":"/media/filer_public/f1/56/f1563eef-103d-4d69-ba6b-31c4cb74337b/6a4532ecbbf83bbf5e44ec91f004df02.jpg","address":{"pk":5,"title":"Омская область"},"title":"Авангард"},"score":5,"opponent_score":4,"is_home":true,"spectators":6208,"arena_capacity":8512,"arena_capacity_rate":0.7293233082706767,"capacity_rate_average":0.7654664003759398},{"id":33249,"date":"2014-11-04T14:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":14,"title_verbose":"Салават Юлаев (Уфа)","url":"/ru/hockey/clubs/14/","logo":"/media/filer_public/9a/f7/9af72665-d8a0-4603-b2f2-2b07809aa6a2/salavat-iulaev.gif","address":{"pk":12,"title":"Уфа"},"title":"Салават Юлаев"},"score":6,"opponent_score":0,"is_home":true,"spectators":5844,"arena_capacity":8512,"arena_capacity_rate":0.6865601503759399,"capacity_rate_average":0.7654664003759398},{"id":33241,"date":"2014-11-02T14:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":53,"title_verbose":"Йокерит (Хельсинки)","url":"/ru/hockey/clubs/53/","logo":"/media/filer_public/4b/f6/4bf62f62-5bea-49da-b138-9bf788bd72cf/a78704a94b9f8c9adb73ab3fcb533f65.jpg","address":{"pk":97,"title":"Хельсинки"},"title":"Йокерит"},"score":1,"opponent_score":3,"is_home":true,"spectators":6859,"arena_capacity":8512,"arena_capacity_rate":0.8058035714285714,"capacity_rate_average":0.7654664003759398},{"id":33232,"date":"2014-10-31T16:30:00Z","overtime_win":true,"bullet_win":false,"opponent":{"id":11,"title_verbose":"СКА (Санкт-Петербург)","url":"/ru/hockey/clubs/11/","logo":"/media/filer_public/7b/2e/7b2e111f-27a1-4cfd-a181-d17fa08542a4/74515728fdbe9c39b803d8c970a06dfb.jpg","address":{"pk":9,"title":"Санкт-Петербург"},"title":"СКА"},"score":4,"opponent_score":3,"is_home":true,"spectators":8015,"arena_capacity":8512,"arena_capacity_rate":0.9416118421052632,"capacity_rate_average":0.7654664003759398},{"id":33210,"date":"2014-10-27T16:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":91,"title_verbose":"Динамо Р (Рига)","url":"/ru/hockey/clubs/91/","logo":"/media/filer_public/2b/56/2b56f66e-55b7-4c52-9075-19bac874f7af/dinamo-r.gif","address":{"pk":59,"title":"Рига"},"title":"Динамо Р"},"score":3,"opponent_score":4,"is_home":true,"spectators":4614,"arena_capacity":8512,"arena_capacity_rate":0.5420582706766918,"capacity_rate_average":0.7654664003759398},{"id":33191,"date":"2014-10-23T12:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":42,"title_verbose":"Сибирь (Новосибирская область)","url":"/ru/hockey/clubs/42/","logo":"/media/filer_public/e3/e8/e3e842a8-31ce-401e-ab79-84235d102830/7af58a349de57ede56d9a28bfd4afe0c.jpg","address":{"pk":105,"title":"Новосибирская область"},"title":"Сибирь"},"score":5,"opponent_score":3,"is_home":false,"spectators":7400,"arena_capacity":8512,"arena_capacity_rate":0.8693609022556391,"capacity_rate_average":0.7654664003759398},{"id":33176,"date":"2014-10-21T12:00:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":8,"title_verbose":"Металлург Нк (Новокузнецк)","url":"/ru/hockey/clubs/8/","logo":"/media/filer_public/66/99/6699f71e-b3ae-45f3-ab94-49f8714a57bb/logo_metallurg_novokuznetsk.gif","address":{"pk":6,"title":"Новокузнецк"},"title":"Металлург Нк"},"score":2,"opponent_score":3,"is_home":false,"spectators":3073,"arena_capacity":8512,"arena_capacity_rate":0.36101973684210525,"capacity_rate_average":0.7654664003759398},{"id":33162,"date":"2014-10-19T06:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":4,"title_verbose":"Амур (Хабаровск)","url":"/ru/hockey/clubs/4/","logo":"/media/filer_public/af/ba/afbaf364-d108-4712-8310-6fff0c960890/5dfadd8d4b156ed313bdd2303000f014.jpg","address":{"pk":4,"title":"Хабаровск"},"title":"Амур"},"score":3,"opponent_score":2,"is_home":false,"spectators":6281,"arena_capacity":8512,"arena_capacity_rate":0.7378994360902256,"capacity_rate_average":0.7654664003759398},{"id":33151,"date":"2014-10-17T09:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":60,"title_verbose":"Адмирал (Владивосток)","url":"/ru/hockey/clubs/60/","logo":"/media/filer_public/7c/45/7c458537-7116-4e8d-ac88-98a317cf91dc/9124c36ae605a27df2d04c87a53f5226.jpg","address":{"pk":106,"title":"Владивосток"},"title":"Адмирал"},"score":4,"opponent_score":1,"is_home":false,"spectators":5500,"arena_capacity":8512,"arena_capacity_rate":0.6461466165413534,"capacity_rate_average":0.7654664003759398},{"id":33130,"date":"2014-10-12T13:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":9,"title_verbose":"Северсталь (Череповец)","url":"/ru/hockey/clubs/9/","logo":"/media/filer_public/74/96/7496f393-089b-4859-95f4-50c2e10ed839/4919a0b4f92b29a921dbfa5cfdef450e.jpg","address":{"pk":7,"title":"Череповец"},"title":"Северсталь"},"score":5,"opponent_score":1,"is_home":true,"spectators":5147,"arena_capacity":8512,"arena_capacity_rate":0.6046757518796992,"capacity_rate_average":0.7654664003759398},{"id":33113,"date":"2014-10-09T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":10,"title_verbose":"Торпедо (Нижний Новгород)","url":"/ru/hockey/clubs/10/","logo":"/media/filer_public/5b/2f/5b2f77a1-8172-4f03-9135-1c441b3a0965/bbfce1c18b92b3ccc5091f10a20a731b.jpg","address":{"pk":8,"title":"Нижний Новгород"},"title":"Торпедо"},"score":1,"opponent_score":3,"is_home":false,"spectators":5600,"arena_capacity":8512,"arena_capacity_rate":0.6578947368421053,"capacity_rate_average":0.7654664003759398},{"id":33106,"date":"2014-10-07T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":12,"title_verbose":"Локомотив (Ярославль)","url":"/ru/hockey/clubs/12/","logo":"/media/filer_public/fb/ee/fbeeed12-5e22-43e4-b08e-dedd18cc60bc/2cf68953c6cd4fabe9285a28a5b3267a.jpg","address":{"pk":10,"title":"Ярославль"},"title":"Локомотив"},"score":2,"opponent_score":0,"is_home":true,"spectators":5937,"arena_capacity":8512,"arena_capacity_rate":0.6974859022556391,"capacity_rate_average":0.7654664003759398},{"id":33095,"date":"2014-10-05T13:00:00Z","overtime_win":true,"bullet_win":false,"opponent":{"id":56,"title_verbose":"ХК Сочи (Сочи)","url":"/ru/hockey/clubs/56/","logo":"/media/filer_public/21/13/2113fc87-7fe4-4371-8371-521f2568bd56/4a39e817291e2e8d0fdef66c76f31fbd.jpg","address":{"pk":124,"title":"Сочи"},"title":"ХК Сочи"},"score":2,"opponent_score":1,"is_home":true,"spectators":5226,"arena_capacity":8512,"arena_capacity_rate":0.6139567669172933,"capacity_rate_average":0.7654664003759398},{"id":33081,"date":"2014-10-02T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":12,"title_verbose":"Локомотив (Ярославль)","url":"/ru/hockey/clubs/12/","logo":"/media/filer_public/fb/ee/fbeeed12-5e22-43e4-b08e-dedd18cc60bc/2cf68953c6cd4fabe9285a28a5b3267a.jpg","address":{"pk":10,"title":"Ярославль"},"title":"Локомотив"},"score":2,"opponent_score":4,"is_home":false,"spectators":8963,"arena_capacity":8512,"arena_capacity_rate":1.052984022556391,"capacity_rate_average":0.7654664003759398},{"id":33070,"date":"2014-09-30T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":20,"title_verbose":"Витязь (Московская область)","url":"/ru/hockey/clubs/20/","logo":"/media/filer_public/82/7e/827e82a7-7611-4a37-b344-774a6420ddf9/97c602120c26bffddf2ce5779921cd94.jpg","address":{"pk":46,"title":"Московская область"},"title":"Витязь"},"score":6,"opponent_score":4,"is_home":true,"spectators":4260,"arena_capacity":8512,"arena_capacity_rate":0.5004699248120301,"capacity_rate_average":0.7654664003759398},{"id":33051,"date":"2014-09-27T11:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":61,"title_verbose":"Барыс (Астана)","url":"/ru/hockey/clubs/61/","logo":"/media/filer_public/c2/9d/c29d195e-e9e2-4e71-a3ff-69d9e27e35d6/bcf515fc3fff50fc092e270ca3243547.jpg","address":{"pk":58,"title":"Астана"},"title":"Барыс"},"score":2,"opponent_score":1,"is_home":false,"spectators":3970,"arena_capacity":8512,"arena_capacity_rate":0.4664003759398496,"capacity_rate_average":0.7654664003759398},{"id":33041,"date":"2014-09-25T15:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":56,"title_verbose":"ХК Сочи (Сочи)","url":"/ru/hockey/clubs/56/","logo":"/media/filer_public/21/13/2113fc87-7fe4-4371-8371-521f2568bd56/4a39e817291e2e8d0fdef66c76f31fbd.jpg","address":{"pk":124,"title":"Сочи"},"title":"ХК Сочи"},"score":1,"opponent_score":0,"is_home":false,"spectators":9209,"arena_capacity":8512,"arena_capacity_rate":1.0818843984962405,"capacity_rate_average":0.7654664003759398},{"id":33025,"date":"2014-09-23T13:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":14,"title_verbose":"Салават Юлаев (Уфа)","url":"/ru/hockey/clubs/14/","logo":"/media/filer_public/9a/f7/9af72665-d8a0-4603-b2f2-2b07809aa6a2/salavat-iulaev.gif","address":{"pk":12,"title":"Уфа"},"title":"Салават Юлаев"},"score":4,"opponent_score":2,"is_home":false,"spectators":7020,"arena_capacity":8512,"arena_capacity_rate":0.8247180451127819,"capacity_rate_average":0.7654664003759398},{"id":33020,"date":"2014-09-21T13:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":34,"title_verbose":"Трактор (Челябинск)","url":"/ru/hockey/clubs/34/","logo":"/media/filer_public/c5/ea/c5ea686d-f9ca-44f8-9b6f-a91a9a7fa79f/afc9e3d12dd54656d7b4a7fd6a3f7d12.jpg","address":{"pk":3,"title":"Челябинск"},"title":"Трактор"},"score":4,"opponent_score":1,"is_home":true,"spectators":5162,"arena_capacity":8512,"arena_capacity_rate":0.606437969924812,"capacity_rate_average":0.7654664003759398},{"id":33015,"date":"2014-09-19T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":57,"title_verbose":"Автомобилист (Екатеринбург)","url":"/ru/hockey/clubs/57/","logo":"/media/filer_public/a5/22/a5228b14-bb6d-47fa-ad0c-505aa17e598c/7b84c940f884393f3b79dbd94dd9fa15.jpg","address":{"pk":35,"title":"Екатеринбург"},"title":"Автомобилист"},"score":4,"opponent_score":2,"is_home":true,"spectators":4178,"arena_capacity":8512,"arena_capacity_rate":0.49083646616541354,"capacity_rate_average":0.7654664003759398},{"id":33003,"date":"2014-09-17T15:30:00Z","overtime_win":false,"bullet_win":true,"opponent":{"id":58,"title_verbose":"Металлург (Магнитогорск)","url":"/ru/hockey/clubs/58/","logo":"/media/filer_public/28/ea/28ea12dc-50e2-4fdd-9430-b9f48dcb5ae6/2c8183806235cb9f5632d250cf96c491.jpg","address":{"pk":1,"title":"Магнитогорск"},"title":"Металлург"},"score":0,"opponent_score":1,"is_home":true,"spectators":5939,"arena_capacity":8512,"arena_capacity_rate":0.6977208646616542,"capacity_rate_average":0.7654664003759398},{"id":32975,"date":"2014-09-13T13:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":17,"title_verbose":"Ак Барс (Казань)","url":"/ru/hockey/clubs/17/","logo":"/media/filer_public/84/0c/840c37b0-8e28-448b-b0f3-faeea77291f1/89eec748745b21cb5cd68131a21a9718.jpg","address":{"pk":14,"title":"Казань"},"title":"Ак Барс"},"score":3,"opponent_score":2,"is_home":true,"spectators":6259,"arena_capacity":8512,"arena_capacity_rate":0.7353148496240601,"capacity_rate_average":0.7654664003759398},{"id":32953,"date":"2014-09-08T15:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":9,"title_verbose":"Северсталь (Череповец)","url":"/ru/hockey/clubs/9/","logo":"/media/filer_public/74/96/7496f393-089b-4859-95f4-50c2e10ed839/4919a0b4f92b29a921dbfa5cfdef450e.jpg","address":{"pk":7,"title":"Череповец"},"title":"Северсталь"},"score":3,"opponent_score":2,"is_home":false,"spectators":3345,"arena_capacity":8512,"arena_capacity_rate":0.3929746240601504,"capacity_rate_average":0.7654664003759398},{"id":32933,"date":"2014-09-05T15:30:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":27,"title_verbose":"ЦСКА (Москва)","url":"/ru/hockey/clubs/27/","logo":"/media/filer_public/44/6b/446b9ec8-c178-40c7-909f-e94d85cd1409/873b8ab6871bcd67ce0f76d50eda209b.jpg","address":{"pk":2,"title":"Москва"},"title":"ЦСКА"},"score":1,"opponent_score":4,"is_home":true,"spectators":6749,"arena_capacity":8512,"arena_capacity_rate":0.7928806390977443,"capacity_rate_average":0.7654664003759398},{"id":32922,"date":"2014-09-03T13:00:00Z","overtime_win":false,"bullet_win":false,"opponent":{"id":58,"title_verbose":"Металлург (Магнитогорск)","url":"/ru/hockey/clubs/58/","logo":"/media/filer_public/28/ea/28ea12dc-50e2-4fdd-9430-b9f48dcb5ae6/2c8183806235cb9f5632d250cf96c491.jpg","address":{"pk":1,"title":"Магнитогорск"},"title":"Металлург"},"score":1,"opponent_score":6,"is_home":false,"spectators":7523,"arena_capacity":8512,"arena_capacity_rate":0.8838110902255639,"capacity_rate_average":0.7654664003759398}]
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
                                name: game.opponent.title + ' - ' + $scope.clubName
                                score: Math.abs(game.opponent_score) + ' : ' + Math.abs(game.score)
                                color: if (Math.abs(game.opponent_score) > Math.abs(game.score)) then '#e74c3c' else '#82b440'
                                leftLogo: game.opponent.logo
                                rightLogo: $scope.clubLogo
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
                                name: $scope.clubName + ' - ' + game.opponent.title
                                score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score)
                                color: if (Math.abs(game.opponent_score) > Math.abs(game.score)) then '#e74c3c' else '#82b440'
                                leftLogo: $scope.clubLogo
                                rightLogo: game.opponent.logo
                            )
                        ).filter (toFilter) ->
                            return toFilter?
                    )
                    $scope.loaded = true
                    $scope.stats = (
                        date: new Date().ddmmyyyy('.')
                        games: $scope.games.length
                        won: _.filter $scope.games, (game) ->
                            return game.score > game.opponent.score
                        lost: _.filter $scope.games, (game) ->
                            return game.score < game.opponent.score
                        wonHome: _.filter $scope.games, (game) ->
                            return game.score > game.opponent.score and game.is_home is true
                        lostHome: _.filter $scope.games, (game) ->
                            return game.score < game.opponent.score and game.is_home is true
                    )
                    $timeout(() ->
                        $('.message .close').on 'click', () ->
                            $(this).closest('.message').fadeOut()
                    , 500)
                    clubGamesChart = new HighchartsFactory.ClubGamesChart 'chartdiv', [clubObject, opponentObject]
                    clubGamesChart.draw()
                    self.chart = $("#chartdiv").highcharts()
                    self.chart.tooltip.hide()
                    _.last(self.chart.series[0].data).setState('hover')
                    self.chart.tooltip.refresh([_.last(self.chart.series[0].data)])

        $scope.previous = () ->
            date = $scope.calendars[$scope.calendars.length - 3].date
            _.each [-3,-2,-1], (deltaM) ->
                $scope.calendars.push
                    'date': $scope.monthDelta(date, deltaM)
                    'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()]
                    'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()]
                    'table': $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules)

        $scope.toggleGameDaysOnly = () ->
            $scope.gameDaysOnly = !$scope.gameDaysOnly

        $scope.showWholeSeason = () ->
            if $scope.wholeSeason is true
                $scope.wholeSeason = false
                data = $scope.data
                date = $scope.getMinEndDate(data)
                array = []
                if date isnt (new Date(data.season.end_date))
                    countToEnd = new Date($scope.data.season.end_date).getMonth() - date.getMonth()
                    i = 0
                    while i < countToEnd
                        array.push i
                        i++
                $scope.calendars = []
                _.each array, (deltaM) ->
                    table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules)
                    gamesInMonth = _.filter table, (cell) ->
                        cell.schedule?
                    if gamesInMonth.length > 0
                        $scope.calendars.push
                            'date': $scope.monthDelta(date, deltaM),
                            'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                            'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()]
                            'table': table
                return
            $scope.wholeSeason = true
            $scope.noGames = false
            date = new Date($scope.data.season.start_date)
            array = []
            countToEnd = Math.abs(new Date($scope.data.season.end_date).getMonth()+12 - date.getMonth())
            i = 0
            while i < countToEnd
                array.push i
                i++
            $scope.calendars = []
            _.each array, (deltaM) ->
                table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules)
                gamesInMonth = _.filter table, (cell) ->
                    cell.schedule?
                if gamesInMonth.length > 0
                    $scope.calendars.push
                        'date': $scope.monthDelta(date, deltaM),
                        'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                        'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()]
                        'table': table
            return


        $scope.list()

        return
])
