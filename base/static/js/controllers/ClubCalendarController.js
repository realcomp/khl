angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', function($scope, $http, $location) {
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
      params = '';
      $scope.calendar = $scope.getCalendar(2015, 0);
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        $scope.data = data;
        return $scope.loaded = true;
      });
    };
  }
]);
