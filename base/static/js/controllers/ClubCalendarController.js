angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', function($scope, $http, $location) {
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
    $scope.getCalendar = function(year, month) {
      var cell, date, day, daysInM, i, j, k, result, row, startDoW;
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
          cell = i * 7 + j;
          day = cell - startDoW + 1;
          date = null;
          if ((1 <= day && day <= daysInM)) {
            date = new Date(year, month, day);
          }
          row.push({
            'cell': cell,
            'date': date
          });
        }
        result.push(row);
        i += 1;
      }
      return result;
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
        $scope.calendars = (function() {
          var k, results;
          results = [];
          for (m = k = 0; k < 3; m = ++k) {
            results.push({
              'year': 2015,
              'month': $scope.MONTHS[m],
              'table': $scope.getCalendar(2015, m)
            });
          }
          return results;
        })();
        return $scope.loaded = true;
      });
    };
  }
]);
