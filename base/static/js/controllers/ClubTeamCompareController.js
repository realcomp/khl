angular.module('Sportomatics').controller('ClubTeamCompareController', function($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory, $timeout) {
  var averageClubPlayerIndicatorsChart, self;
  self = this;
  this.url = document.getElementById('api-player-indicators').value;
  averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart();
  $scope.localeObject = LocaleFactory.selectedLocale;
  $scope.setField = averageClubPlayerIndicatorsChart.setField;
  $scope.field = averageClubPlayerIndicatorsChart.getField();
  $scope.dataType = averageClubPlayerIndicatorsChart.getDataType();
  $scope.clubs = [];
  $scope.offenders = true;
  $scope.defenders = true;
  $scope.params = {
    professional: false
  };
  $scope.setParams = function() {
    $('#regularParams').toggleClass('display-none');
    $('#professionalParams').toggleClass('display-none');
    $('.ui.checkbox-regular').checkbox('uncheck');
    $('.ui.checkbox-professional').checkbox('check');
    return null;
  };
  this.clubPk = document.getElementById('team-id').value;
  $scope.$watch('field', function() {
    if ($scope.clubs.length > 0) {
      return $scope.listAveragePlayer();
    }
  });
  $scope.showPersonalList = function() {
    $('.overlay-black').removeClass('hidden');
    $('#personal-list').removeClass('hidden');
    return null;
  };
  $scope.getActiveState = function(array) {
    if (_.contains(array, $scope.field)) {
      return 'active';
    } else {
      return '';
    }
  };
  $scope.setSeason = function(season) {
    $scope.season = season;
    return console.log($scope.season);
  };
  $scope.setSelectedPlayer = function(obj) {
    if ((obj != null) && (obj.originalObject != null)) {
      return $scope.selectedPlayer = obj.originalObject;
    }
  };
  $scope.addAverageClubPlayerData = function(clubPk) {
    var pk, url;
    if (($scope.selectedClub == null) && (clubPk == null)) {
      return;
    }
    if (($scope.selectedClub != null) && ($scope.selectedClub.originalObject != null)) {
      pk = $scope.selectedClub.originalObject.pk;
      console.log(pk);
    }
    if (pk == null) {
      if (clubPk != null) {
        pk = clubPk;
        $scope.selectedClub = {
          originalObject: {
            title: document.getElementById('team-name-hidden').value,
            pk: clubPk,
            color: null,
            logo: document.getElementById('club-logo').value
          }
        };
      } else {
        return;
      }
    }
    url = $('#club-team-api').val().replace(/(\/)([0-9]+)(\/)/, '/') + pk;
    if ($scope.season != null) {
      url += '?season=' + $scope.season;
    } else {
      $scope.season = 19;
    }
    $http.get(url).success(function(data, status, headers) {
      var players, queries;
      LocaleFactory.setLocale(headers()['content-language']);
      players = data.all_players = _.filter(data.all_players, function(player) {
        return player.line > 1;
      });
      queries = [];
      _.each(players, function(player) {
        player.selected = true;
        queries.push($http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season'));
      });
      $scope.loader = true;
      $q.all(queries).then(function(results) {
        var clubObject, seasonResult;
        $scope.loader = false;
        seasonResult = _.find(results[0].data.results, function(result) {
          return result.season.pk.toString() === $scope.season;
        });
        if (seasonResult == null) {
          seasonResult = _.last(results[0].data.results);
        }
        clubObject = {
          all_players: data.all_players,
          offender_players: data.offender_players,
          defender_players: data.defender_players,
          title: data.title,
          color: data.main_color || getRandomColor(),
          id: data.pk,
          logo: data.logo,
          address: data.address,
          dataBySeason: {
            results: [
              {
                season: seasonResult['season']
              }
            ]
          },
          results: results,
          seasonResult: seasonResult['season']
        };
        $scope.clubs.push(clubObject);
        $timeout(function() {
          return $scope.listAveragePlayer();
        }, 100);
      });
    });
  };
  $scope.addPlayerToClub = function(title) {
    var club;
    club = _.findWhere($scope.clubs, {
      title: title
    });
    return $q.all([$http.get(self.url.replace('/0/', '/' + $scope.selectedPlayer.pk + '/') + '?group_by=season')]).then(function(results) {
      $scope.selectedPlayer.selected = true;
      $scope.selectedPlayer.added = true;
      club.all_players.push($scope.selectedPlayer);
      club.results.push(results[0]);
      return $scope.listAveragePlayer();
    });
  };
  $scope.togglePlayerSelection = function(title, index) {
    var club, player;
    club = _.findWhere($scope.clubs, {
      title: title
    });
    player = club.all_players[index];
    player.selected = !player.selected;
    $('#player_' + index).attr('checked', !$('#player_' + index).attr('checked'));
    return $scope.listAveragePlayer();
  };
  $scope.listAveragePlayer = function() {
    var newPlayerIndicatorsData;
    newPlayerIndicatorsData = [];
    _.each($scope.clubs, function(club) {
      var averageData, clubObject, key, selectedPlayers;
      selectedPlayers = _.countBy(_.filter(club.all_players, function(player) {
        return player.line === 3 && $scope.offenders === true || player.line === 2 && $scope.defenders === true;
      }), {
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
            player.result = _.find(result.data.results, function(result) {
              return result.season.pk.toString() === club.seasonResult.pk.toString();
            })[$scope.field];
            if (player.line === 3 && !$scope.offenders || player.line === 2 && !$scope.defenders) {
              return;
            }
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
        stack: club.id,
        logo: club.logo
      };
      return newPlayerIndicatorsData.push(clubObject);
    });
    averageClubPlayerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData);
    averageClubPlayerIndicatorsChart.setContext($scope);
    averageClubPlayerIndicatorsChart.setPeriod(30);
    averageClubPlayerIndicatorsChart.draw();
    return self.chart = $('#chartdiv').highcharts();
  };
  $scope.addAverageClubPlayerData(this.clubPk);
});
