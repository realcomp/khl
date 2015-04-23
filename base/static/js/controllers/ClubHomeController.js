angular.module('Sportomatics').controller('ClubHomeController', function($scope, $location, $http, HighchartsFactory) {
  $scope.clubMatchApi = document.getElementById('club-match-api').value;
  $scope.clubPk = document.getElementById('team-id').value;
  $scope.params = $location.search();
  $scope.createVisitorsChart = function() {
    var params;
    params = '';
    params += '?club=' + $scope.clubPk;
    params += '&season=19';
    return $http.get($scope.clubMatchApi + params).success(function(data) {
      var clubGamesChart, seriesClub, seriesOpponent, visitorsObject;
      $scope.games = _.filter(_.sortBy(data, function(el) {
        return new Date(el).getTime();
      }).reverse(), function(game) {
        return game.is_home === true;
      });
      console.log($scope.games);
      seriesClub = {};
      seriesOpponent = {};
      visitorsObject = {
        name: 'club',
        data: $scope.games.map(function(game, index) {
          return {
            x: index,
            y: game.spectators,
            date: game.date,
            name: game.opponent.title_verbose,
            score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score),
            spectators: game.spectators + ' (' + parseInt(parseFloat(game.arena_capacity_rate).toFixed(2) * 100) + '%)'
          };
        }).filter(function(toFilter) {
          return toFilter != null;
        })
      };
      console.log(parseFloat($scope.games[0].arena_capacity_rate).toFixed(2) * 100);
      clubGamesChart = new HighchartsFactory.ArenaVisitorsChart('chartdiv', [visitorsObject], $scope.games[0].arena_capacity);
      return clubGamesChart.draw();
    });
  };
  $scope.createVisitorsChart();
});
