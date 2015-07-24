angular.module('Sportomatics').controller('ClubHomeController', function($scope, $location, $http, HighchartsFactory) {
  $scope.clubMatchApi = document.getElementById('club-match-api').value;
  $scope.clubPk = document.getElementById('team-id').value;
  $scope.params = $location.search();
  $scope.clubLogo = document.getElementById('club-logo').value;
  $scope.createVisitorsChart = function() {
    var params;
    params = '';
    params += '?club=' + $scope.clubPk;
    params += '&season=19';
    $scope.loaded = false;
    return $http.get($scope.clubMatchApi + params).success(function(data) {
      var clubGamesChart, seriesClub, seriesOpponent, visitorsObject;
      $scope.games = _.filter(_.sortBy(data, function(el) {
        return new Date(el).getTime();
      }).reverse(), function(game) {
        return game.is_home === true;
      });
      seriesClub = {};
      seriesOpponent = {};
      visitorsObject = {
        name: 'club',
        data: $scope.games.map(function(game, index) {
          return {
            x: index * 4.5,
            y: game.spectators,
            date: game.date,
            name: game.opponent.title_verbose,
            score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score),
            spectators: game.spectators + ' (' + parseInt(parseFloat(game.arena_capacity_rate).toFixed(2) * 100) + '%)',
            leftLogo: game.opponent.logo,
            rightLogo: $scope.clubLogo
          };
        }).filter(function(toFilter) {
          return toFilter != null;
        })
      };
      $scope.loaded = true;
      clubGamesChart = new HighchartsFactory.ArenaVisitorsChart('chartdiv', [visitorsObject], $scope.games[0].arena_capacity);
      return clubGamesChart.draw();
    });
  };
  $scope.createVisitorsChart();
});
