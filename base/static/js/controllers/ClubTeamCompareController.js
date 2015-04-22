angular.module('Sportomatics').controller('ClubTeamCompareController', function($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory) {
  var averageClubPlayerIndicatorsChart, self;
  self = this;
  this.url = document.getElementById('api-player-indicators').value;
  averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart();
  $scope.localeObject = LocaleFactory.selectedLocale;
  $scope.setField = averageClubPlayerIndicatorsChart.setField;
  $scope.field = averageClubPlayerIndicatorsChart.getField();
  $scope.dataType = averageClubPlayerIndicatorsChart.getDataType();
  $scope.loader = true;
  $scope.clubs = [];
  $scope.$watch('field', function() {
    if ($scope.clubs.length > 0) {
      return self.listAvergePlayer();
    }
  });
  $scope.addAverageClubPlayerData = function() {
    var pk, url;
    if ($scope.selectedClub == null) {
      return;
    }
    pk = $scope.selectedClub.originalObject.pk;
    if (pk == null) {
      return;
    }
    url = $('#club-team-api').val().replace('0/', '') + pk;
    $http.get(url).success(function(data, status, headers) {
      var players, queries;
      LocaleFactory.setLocale(headers()['content-language']);
      console.log(LocaleFactory.selectedLocale);
      players = data.all_players = _.filter(data.all_players, function(player) {
        return player.line_display.indexOf('Goalkeeper') === -1;
      });
      data.offender_players.map(function(el) {
        el.selected = true;
        return el;
      });
      data.defender_players.map(function(el) {
        el.selected = true;
        return el;
      });
      queries = [];
      _.each(players, function(player) {
        player.selected = true;
        queries.push($http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season'));
      });
      $q.all(queries).then(function(results) {
        var clubObject, lastSeasonResult;
        lastSeasonResult = _.last(results[0].data.results);
        clubObject = {
          all_players: data.all_players,
          offender_players: data.offender_players,
          defender_players: data.defender_players,
          title: $scope.selectedClub.originalObject.title,
          color: $scope.selectedClub.originalObject.main_color || getRandomColor(),
          id: $scope.selectedClub.originalObject.pk,
          dataBySeason: {
            results: [
              {
                season: lastSeasonResult['season']
              }
            ]
          },
          results: results
        };
        $scope.clubs.push(clubObject);
        self.listAvergePlayer();
      });
    });
  };
  $scope.offenderFilter = function(player) {
    return player.line_display === 'Offender';
  };
  $scope.defenderFilter = function(player) {
    return player.line_display === 'Defender';
  };
  $scope.calculateTeamData = function() {
    return _.each($scope.clubs, function(club) {
      var players;
      return players = _.filter(club.all_players, function(player) {
        return player.line_display.indexOf('Goalkeeper') === -1 && player.selected === true;
      });
    });
  };
  $scope.togglePlayerSelection = function(title, index) {
    var club, player;
    console.log(title);
    club = _.findWhere($scope.clubs, {
      title: title
    });
    player = club.all_players[index];
    player.selected = !player.selected;
    console.log(player.fio);
    $('#player_' + index).attr('checked', !$('#player_' + index).attr('checked'));
    return self.listAvergePlayer();
  };
  this.listAvergePlayer = function() {
    var newPlayerIndicatorsData;
    newPlayerIndicatorsData = [];
    _.each($scope.clubs, function(club) {
      var averageData, clubObject, key, selectedPlayers;
      selectedPlayers = _.countBy(club.all_players, {
        selected: true
      })['true'];
      for (key in _.last(club.results[0].data.results)) {
        if (_.contains(ALL_FIELDS, key)) {
          averageData = 0;
          _.each(club.results, function(result) {
            var player;
            player = _.findWhere(club.all_players, {
              pk: Number(result.config.url.match("players\/(.*)\/indicators")[1])
            });
            player.result = _.last(result.data.results)[$scope.field];
            if (player.selected === true) {
              averageData += parseFloat(_.last(result.data.results)[key]);
            }
          });
          averageData = parseFloat(averageData / selectedPlayers).toFixed(3);
          club.dataBySeason.results[0][key] = averageData;
        }
      }
      clubObject = {
        name: club.title,
        data: club.dataBySeason.results.map(function(el) {
          return {
            x: new Date(el.season.end_date.split('-')[0]).getTime(),
            y: parseFloat(el[$scope.field]),
            drilldown: el.season.end_date
          };
        }),
        color: club.color,
        stack: club.id
      };
      return newPlayerIndicatorsData.push(clubObject);
    });
    averageClubPlayerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData);
    averageClubPlayerIndicatorsChart.setContext($scope);
    averageClubPlayerIndicatorsChart.setPeriod(30);
    averageClubPlayerIndicatorsChart.draw();
    return self.chart = $('#chartdiv').highcharts();
  };
});
