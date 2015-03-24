angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', '$parse', function($scope, $http, $location, $parse) {
    $scope.MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    $scope.data = {};
    $scope.params = $location.search();
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
    $scope.getSchedules = function(data) {
      var getDate, k, len, result, s;
      result = {};
      getDate = $parse('date|date:"yyyy-MM-dd"');
      for (k = 0, len = data.length; k < len; k++) {
        s = data[k];
        result[getDate(s)] = s;
      }
      return result;
    };
    $scope.getCalendar = function(year, month, schedules) {
      var cell, day, daysInM, i, j, k, result, row, startDoW, strfdate;
      daysInM = new Date(year, month + 1, 0).getDate();
      startDoW = new Date(year, month, 1).getDay() - 1;
      if (startDoW < 0) {
        startDoW = 6;
      }
      result = [];
      i = 0;
      row = [];
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
      while (i * 7 < daysInM + startDoW && i <= 6) {
        row = [];
        for (j = k = 0; k < 7; j = ++k) {
          cell = {
            'cell': i * 7 + j
          };
          day = cell.cell - startDoW + 1;
          if ((1 <= day && day <= daysInM)) {
            cell['date'] = new Date(year, month, day);
            cell['schedule'] = schedules[strfdate(cell.date)];
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
        var m;
        $scope.data = data;
        $scope.schedules = $scope.getSchedules(data);
        $scope.calendars = (function() {
          var k, results;
          results = [];
          for (m = k = 0; k < 3; m = ++k) {
            results.push({
              'year': 2015,
              'month': $scope.MONTHS[m],
              'table': $scope.getCalendar(2015, m, $scope.schedules)
            });
          }
          return results;
        })();
        return $scope.loaded = true;
      });
    };
  }
]);
