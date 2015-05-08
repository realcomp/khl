angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory', function($scope, $http, $location, $parse, MapService, HighchartsFactory) {
    $scope.MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    $scope.MONTHS_ROD = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня', 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря'];
    $scope.data = {};
    $scope.params = $location.search();
    $scope.gameDaysOnly = false;
    $scope.clubName = document.getElementById('team-name-hidden').value;
    $scope.clubAddress = document.getElementById('club-address') != null ? document.getElementById('club-address').innerHTML : '';
    $scope.clubMatchApi = document.getElementById('club-match-api') != null ? document.getElementById('club-match-api').value : void 0;
    $scope.clubCalendarApi = $scope.url = document.getElementById('club-calendar-api') != null ? document.getElementById('club-calendar-api').value : void 0;
    $scope.clubPk = document.getElementById('team-id').value;
    $scope.games = [];
    $scope.selection = 'all';
    $scope.setSelecton = function(selection) {
      $scope.selection = selection;
      return $scope.createGamesChart();
    };
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
    $scope.getCalendarDays = function(date, schedules) {
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
        result.push({
          cell: 'empty'
        });
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
          result.push(cell);
        }
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
      if (a.getTime() < b.getTime()) {
        return a;
      } else {
        return b;
      }
    };
    $scope.list = function() {
      var params;
      $scope.wholeSeason = false;
      $scope.params = $location.search();
      params = '';
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      } else {
        params += '&season=19';
      }
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        var array, countToEnd, date, i;
        if (MapService.isRendered()) {
          MapService.remove();
        }
        if ($('#clubs-map').length > 0) {
          MapService.createClubsMap(data.results, 'trips');
        }
        $scope.data = data;
        $scope.schedules = $scope.parseSchedules(data);
        date = $scope.getMinEndDate(data);
        array = [];
        if (date !== (new Date(data.season.end_date))) {
          countToEnd = new Date($scope.data.season.end_date).getMonth() - date.getMonth();
          i = 0;
          while (i < countToEnd) {
            array.push(i);
            i++;
          }
        }
        $scope.calendars = [];
        _.each(array, function(deltaM) {
          var gamesInMonth, table;
          table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules);
          gamesInMonth = _.filter(table, function(cell) {
            return cell.schedule != null;
          });
          if (gamesInMonth.length > 0) {
            return $scope.calendars.push({
              'date': $scope.monthDelta(date, deltaM),
              'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
              'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()],
              'table': table
            });
          }
        });
        $scope.loaded = true;
        if ($scope.calendars.length === 0) {
          $scope.noGames = true;
        }
        return console.log($scope.calendars.length);
      });
      return $scope.createGamesChart();
    };
    $scope.createGamesChart = function() {
      var params;
      params = '';
      params += '?club=' + $scope.clubPk;
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      return $http.get($scope.clubMatchApi + params).success(function(data) {
        var clubGamesChart, clubObject, opponentObject, seriesClub, seriesOpponent;
        $scope.games = _.sortBy(data, function(el) {
          return new Date(el).getTime();
        }).reverse();
        seriesClub = {};
        seriesOpponent = {};
        opponentObject = {
          name: 'opponents',
          data: $scope.games.map(function(game, index) {
            if ($scope.selection === 'home' && game.is_home === false) {
              return;
            }
            if ($scope.selection === 'guest' && game.is_home === true) {
              return;
            }
            return {
              x: index,
              y: -Math.abs(game.opponent_score),
              date: game.date,
              name: game.opponent.title_verbose + ' - ' + $scope.clubName + ' ' + $scope.clubAddress,
              score: Math.abs(game.opponent_score) + ' : ' + Math.abs(game.score),
              color: Math.abs(game.opponent_score) > Math.abs(game.score) ? '#e74c3c' : '#2ecc71'
            };
          }).filter(function(toFilter) {
            return toFilter != null;
          })
        };
        clubObject = {
          name: 'club',
          data: $scope.games.map(function(game, index) {
            var opponentAddress;
            if ($scope.selection === 'home' && game.is_home === false) {
              return;
            }
            if ($scope.selection === 'guest' && game.is_home === true) {
              return;
            }
            opponentAddress = game.opponent.address && game.opponent.address.title ? game.opponent.address.title : '';
            return {
              x: index,
              y: game.score,
              date: game.date,
              name: $scope.clubName + ' ' + $scope.clubAddress + ' - ' + game.opponent.title_verbose,
              score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score),
              color: Math.abs(game.opponent_score) > Math.abs(game.score) ? '#e74c3c' : '#2ecc71'
            };
          }).filter(function(toFilter) {
            return toFilter != null;
          })
        };
        clubGamesChart = new HighchartsFactory.ClubGamesChart('chartdiv', [clubObject, opponentObject]);
        return clubGamesChart.draw();
      });
    };
    $scope.previous = function() {
      var date;
      date = $scope.calendars[$scope.calendars.length - 3].date;
      return _.each([-3, -2, -1], function(deltaM) {
        return $scope.calendars.push({
          'date': $scope.monthDelta(date, deltaM),
          'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
          'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()],
          'table': $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules)
        });
      });
    };
    $scope.toggleGameDaysOnly = function() {
      return $scope.gameDaysOnly = !$scope.gameDaysOnly;
    };
    $scope.showWholeSeason = function() {
      var array, countToEnd, data, date, i;
      if ($scope.wholeSeason === true) {
        $scope.wholeSeason = false;
        data = $scope.data;
        date = $scope.getMinEndDate(data);
        array = [];
        if (date !== (new Date(data.season.end_date))) {
          countToEnd = new Date($scope.data.season.end_date).getMonth() - date.getMonth();
          i = 0;
          while (i < countToEnd) {
            array.push(i);
            i++;
          }
        }
        $scope.calendars = [];
        _.each(array, function(deltaM) {
          var gamesInMonth, table;
          table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules);
          gamesInMonth = _.filter(table, function(cell) {
            return cell.schedule != null;
          });
          if (gamesInMonth.length > 0) {
            return $scope.calendars.push({
              'date': $scope.monthDelta(date, deltaM),
              'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
              'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()],
              'table': table
            });
          }
        });
        return;
      }
      $scope.wholeSeason = true;
      $scope.noGames = false;
      date = new Date($scope.data.season.start_date);
      array = [];
      countToEnd = Math.abs(new Date($scope.data.season.end_date).getMonth() + 12 - date.getMonth());
      i = 0;
      while (i < countToEnd) {
        array.push(i);
        i++;
      }
      $scope.calendars = [];
      _.each(array, function(deltaM) {
        var gamesInMonth, table;
        table = $scope.getCalendarDays($scope.monthDelta(date, deltaM), $scope.schedules);
        gamesInMonth = _.filter(table, function(cell) {
          return cell.schedule != null;
        });
        if (gamesInMonth.length > 0) {
          return $scope.calendars.push({
            'date': $scope.monthDelta(date, deltaM),
            'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
            'month_display_rod': $scope.MONTHS_ROD[$scope.monthDelta(date, deltaM).getMonth()],
            'table': table
          });
        }
      });
    };
    $scope.list();
  }
]);
