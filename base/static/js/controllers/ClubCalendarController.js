angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory', function($scope, $http, $location, $parse, MapService, HighchartsFactory) {
    $scope.MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    $scope.data = {};
    $scope.params = $location.search();
    $scope.club = 'wdq';
    $scope.games = [
      {
        is_home: false,
        date: '2010-07-01',
        opponent: {
          pk: 1,
          title: 'Металлург',
          logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif',
          score: -4
        },
        score: 5
      }, {
        is_home: false,
        date: '2010-07-02',
        opponent: {
          pk: 1,
          title: 'СКА',
          logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif',
          score: -3
        },
        score: 2
      }, {
        is_home: false,
        date: '2010-07-03',
        opponent: {
          pk: 1,
          title: 'Авангард',
          logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif',
          score: -3
        },
        score: 7
      }, {
        is_home: false,
        date: '2010-07-07',
        opponent: {
          pk: 1,
          title: 'ХК Сочи',
          logo: 'dev.sportomatics.ru/media/filer_public/5b/a4/5ba48a7f-2335-40a8-90cb-4d7f7b8e7bf8/logo_metallurg_magnitogorsk.gif',
          score: -4
        },
        score: 2
      }
    ];
    $scope.CalendarEventPopup = {};
    $scope.CalendarEventPopupShow = function(e, event) {
      var params;
      if ($('.calendar-event-popup:hidden').length && this.cell.schedule) {
        $scope.CalendarEventPopup.data = null;
        $scope.CalendarEventPopup.is_home = this.cell.schedule.is_home;
        $scope.CalendarEventPopup.is_guest = this.cell.schedule.is_guest;
        params = '';
        if (this.cell.schedule.is_home) {
          params = '?is_home=true';
        }
        if (this.cell.schedule.is_guest) {
          params = '?is_guest=true';
        }
        $http.get($scope.urlPopup.replace(0, this.cell.schedule.pk) + params).success(function(data) {
          $scope.CalendarEventPopup.data = data;
        });
        $('.calendar-event-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
    $scope.setType = function(type) {
      $location.search('type', type || null);
      $scope.params = $location.search();
    };
    if ($scope.params.season) {
      $('[name="season"]').attr('value', $scope.params.season);
    }
    $scope.setSeason = function(e) {
      $location.search('season', $(e).val());
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.parseSchedules = function(data) {
      var getDate, k, len, ref, result, s;
      result = {};
      getDate = $parse('date|date:"yyyy-MM-dd"');
      ref = data.results;
      for (k = 0, len = ref.length; k < len; k++) {
        s = ref[k];
        result[getDate(s)] = s;
      }
      return result;
    };
    $scope.getSchedule = function(schedules, date) {
      var strfdate;
      strfdate = function(date) {
        var d, m, y;
        y = 1900 + date.getYear();
        m = String(date.getMonth() + 1);
        if (m.length < 2) {
          m = '0' + m;
        }
        d = String(date.getDate());
        if (d.length < 2) {
          d = '0' + d;
        }
        return [y, m, d].join('-');
      };
      return schedules[strfdate(date)];
    };
    $scope.getCalendar = function(date, schedules) {
      var cell, day, daysInM, i, j, k, month, result, row, startDoW, year;
      year = date.getYear() + 1900;
      month = date.getMonth();
      daysInM = new Date(year, month + 1, 0).getDate();
      startDoW = new Date(year, month, 1).getDay() - 1;
      if (startDoW < 0) {
        startDoW = 6;
      }
      result = [];
      i = 0;
      row = [];
      while (i * 7 < daysInM + startDoW && i <= 6) {
        row = [];
        for (j = k = 0; k < 7; j = ++k) {
          cell = {
            'cell': i * 7 + j
          };
          day = cell.cell - startDoW + 1;
          if ((1 <= day && day <= daysInM)) {
            cell['date'] = new Date(year, month, day);
            cell['schedule'] = $scope.getSchedule(schedules, cell.date);
          }
          row.push(cell);
        }
        result.push(row);
        i += 1;
      }
      return result;
    };
    $scope.isHome = function(cell) {
      return cell.schedule && cell.schedule.is_home && $scope.params.type !== 'guest';
    };
    $scope.isGuest = function(cell) {
      return cell.schedule && cell.schedule.is_guest && $scope.params.type !== 'home';
    };
    $scope.getLogo = function(cell) {
      if ($scope.isHome(cell)) {
        return cell.schedule.guest_team.logo;
      }
      if ($scope.isGuest(cell)) {
        return cell.schedule.home_team.logo;
      }
      return null;
    };
    $scope.monthDelta = function(date, deltaM) {
      var d;
      d = new Date(date);
      d.setDate(1);
      d.setMonth(d.getMonth() + deltaM);
      return d;
    };
    $scope.getMinEndDate = function(data) {
      var a, b;
      a = new Date();
      b = new Date(data.season.end_date);
      if (a < b) {
        return a;
      } else {
        return b;
      }
    };
    $scope.list = function() {
      var params;
      $scope.params = $location.search();
      params = '';
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        var date, deltaM;
        console.log(data);
        if (MapService.isRendered()) {
          MapService.remove();
        }
        MapService.createClubsMap(data.results, 'trips');
        $scope.data = data;
        $scope.schedules = $scope.parseSchedules(data);
        date = $scope.getMinEndDate(data);
        $scope.calendars = [
          (function() {
            var k, len, ref, results;
            ref = [-1, 0, 1];
            results = [];
            for (k = 0, len = ref.length; k < len; k++) {
              deltaM = ref[k];
              results.push({
                'date': $scope.monthDelta(date, deltaM),
                'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
              });
            }
            return results;
          })()
        ];
        return $scope.loaded = true;
      });
      return $scope.createGamesChart();
    };
    $scope.createGamesChart = function() {
      var clubGamesChart, clubObject, opponentObject, seriesClub, seriesOpponent;
      seriesClub = {};
      seriesOpponent = {};
      opponentObject = {
        name: 'opponents',
        data: $scope.games.map(function(game, index) {
          return {
            x: index,
            y: game.opponent.score,
            date: game.date,
            name: game.opponent.title + ' - Club',
            score: Math.abs(game.opponent.score) + ' : ' + Math.abs(game.score),
            color: Math.abs(game.opponent.score) > Math.abs(game.score) ? '#FF0000' : 'green',
            dataLabels: {
              enabled: true,
              align: 'left',
              crop: false,
              verticalAlign: 'bottom',
              y: 20,
              formatter: function() {
                console.log(this);
                return this.key.split('-')[0];
              },
              inside: false
            }
          };
        })
      };
      clubObject = {
        name: 'club',
        data: $scope.games.map(function(game, index) {
          return {
            x: index,
            y: game.score,
            date: game.date,
            name: 'Club - ' + game.opponent.title,
            score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent.score),
            color: Math.abs(game.opponent.score) > Math.abs(game.score) ? '#FF0000' : 'green'
          };
        })
      };
      clubGamesChart = new HighchartsFactory.ClubGamesChart('chartdiv', [clubObject, opponentObject]);
      return clubGamesChart.draw();
    };
    $scope.previous = function() {
      var date, deltaM;
      date = $scope.calendars[$scope.calendars.length - 1][0].date;
      return $scope.calendars.push((function() {
        var k, len, ref, results;
        ref = [-3, -2, -1];
        results = [];
        for (k = 0, len = ref.length; k < len; k++) {
          deltaM = ref[k];
          results.push({
            'date': $scope.monthDelta(date, deltaM),
            'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
            'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
          });
        }
        return results;
      })());
    };
  }
]);
