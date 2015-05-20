angular.module('Sportomatics').controller('ClubTeamController', [
  '$http', '$scope', '$timeout', 'MapService', function($http, $scope, $timeout, MapService) {
    var popup, url;
    url = document.getElementById("club-team-api").value;
    popup = null;
    $scope.type = 'all';
    $scope.cache_players = null;
    $scope.cache_clubs = null;
    $scope.notplaying_players = null;
    $scope.state = 'fio';
    $scope.order_by = 'lastname';
    $scope.season = 19;
    $scope.seasons = [];
    $scope.setOrderBy = function(order_by) {
      if ($scope.order_by === order_by) {
        if ($scope.order_by.indexOf('-') > -1) {
          $scope.order_by = $scope.order_by.replace('-', '');
        } else {
          $scope.order_by = '-' + $scope.order_by;
        }
      } else {
        $scope.order_by = order_by;
      }
    };
    $scope.setType = function(type) {
      $scope.type = type;
      $scope.unMakeTransferArrows();
    };
    $scope.setState = function(state) {
      $scope.state = state;
      $scope.getFromCache();
    };
    $scope.playerFilter = function(value) {
      if ($scope.state === 'coaches') {
        return false;
      }
      return value[$scope.state] !== false;
    };
    $scope.go = function(path) {
      window.location.href = path;
    };
    $scope.PlayerPartnersPopup = {
      'data': null,
      'isClubsVisible': true
    };
    $scope.PlayerPartnersPopupShow = function(e, event) {
      var pk;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length && this.cell_id[0] !== 'trainer') {
        pk = $scope.getCell(self.players, this.cell_id).pk;
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, pk)).success(function(data) {
          return $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
    $scope.players = {};
    $scope.clubs = {
      'getLastClub': function() {
        if ($scope.clubs.length) {
          return $scope.clubs[$scope.clubs.length - 1];
        }
      },
      'clubs': []
    };
    $scope.setSeason = function(season, push) {
      $scope.season = season;
      $scope.list(push);
    };
    $scope.getCell = function(table, cell_id) {
      var group;
      if (table.table && cell_id && Array.isArray(cell_id) && cell_id[1] !== null) {
        group = table.table[cell_id[0]];
        if (group) {
          return group[cell_id[1]];
        }
      }
    };
    $scope.isPersonVisible = function(table, cell_id) {
      var cell;
      cell = $scope.getCell(table, cell_id);
      if (cell) {
        switch (self.players.status) {
          case 'joined':
            return cell.is_joined;
          case 'left':
            return cell.is_left;
          case 'legionnaire':
            return cell.is_legionnaire;
          case 'home':
            return cell.is_home;
          default:
            return true;
        }
      }
      return false;
    };
    $scope.isPersonInCell = function(table, cell_id) {
      var cell;
      cell = $scope.getCell(table, cell_id);
      return cell;
    };
    $scope.list = function(push) {
      var params;
      params = 'season=' + $scope.season;
      $scope.loaded = false;
      $http.get(url + '?' + params).success(function(data) {
        var title;
        if (push) {
          title = '';
          if (document.getElementById('season_' + $scope.season) !== null) {
            title = document.getElementById('season_' + $scope.season).value;
          }
          $scope.seasons.push({
            'players': data,
            'season': $scope.season,
            'title': title
          });
        } else {
          title = '';
          if (document.getElementById('season_' + $scope.season) !== null) {
            title = document.getElementById('season_' + $scope.season).value;
          }
          $scope.seasons = [
            {
              'players': data,
              'season': $scope.season,
              'title': title
            }
          ];
        }
        $scope.players = data;
        $scope.loaded = true;
      });
    };
    $scope.compare = function(arg) {
      var club, params;
      url = $('#ClubTeamCompareLink').attr('href');
      club = self.clubs.getLastClub();
      if (club) {
        params = 'source_season=' + club.data.season.pk;
        params += '&season=' + club.data.prev_season.pk;
      } else {
        params = 'source_season=' + $scope.players.data.season.pk;
        params += '&season=' + $scope.players.data.prev_season.pk;
      }
      $scope.clubs.loader = true;
      return $http.get(url + '?' + params).success(function(data) {
        var clubRows, clubs, clubsInRow, clubsObject;
        if (data.leagues.length) {
          clubRows = [];
          clubsInRow = [];
          clubs = [];
          $scope.clubplayers = [];
          _.each(data.leagues, function(league, index) {
            clubs = clubs.concat(league.clubs);
            $scope.clubplayers = $scope.clubplayers.concat(league.clubplayers);
          });
          _.each(clubs, function(club, index) {
            if (clubsInRow.length < 7) {
              clubsInRow.push(club);
            }
            if (index === clubs.length(-1 || (index + 1) % 7 === 0)) {
              clubRows.push(clubsInRow);
              clubsInRow = [];
            }
          });
          clubsObject = {
            'data': data,
            'table': {
              'club': data.leagues[0].clubs
            },
            'league': data.leagues[0],
            'clubRows': clubRows
          };
          self.clubs.clubs.push(clubsObject);
        }
        $scope.clubs.loader = false;
      });
    };
    $scope.getFromCache = function() {
      if ($scope.cache_players) {
        $scope.players = $scope.cache_players;
        $scope.clubs = $scope.cache_clubs;
      }
    };
    $scope.makeTransferArrows = function() {
      $scope.getFromCache();
      _.each($scope.clubplayers, function(clubplayer) {
        createTransferArrow('#club_' + clubplayer.club, '#player_' + clubplayer.player, clubplayer.pk);
      });
      return $('.player-item').each(function() {
        var id;
        if (!_.findWhere($scope.clubplayers, {
          'player': parseInt($(this).attr('id').split('_')[1])
        })) {
          $(this).addClass('opacity-30');
        } else {
          id = $(this).attr('id');
          $(this).hover(function() {
            return $('canvas').each(function() {
              if ($(this).attr('player') !== id) {
                $(this).addClass('opacity-10');
              }
            });
          }, function() {
            return $("canvas").each(function() {
              $(this).removeClass("opacity-10");
            });
          });
        }
      });
    };
    $scope.unMakeTransferArrows = function() {
      $scope.getFromCache();
      $('canvas').remove();
      return $('.player-item').each(function() {
        return $(this).removeClass("opacity-30");
      });
    };
    $scope.notPlayingNow = function(callback, callbackArg) {
      $scope.setState('fio');
      $scope.unMakeTransferArrows();
      $scope.players.loader = true;
      if ($scope.notplaying_players) {
        $scope.players = $scope.notplaying_players;
      } else {
        $http.get(url + '?notplaying=1').success(function(data) {
          $scope.cache_players = $scope.players;
          $scope.cache_clubs = $scope.clubs;
          $scope.players = data;
          $scope.players.data = data;
          $scope.players.table = {
            'goalkeeper': data.goalkeeper_players,
            'defender': data.defender_players,
            'forward': data.offender_players,
            'trainer': data.coaches
          };
          return $scope.notplaying_players = $scope.players;
        });
      }
      $scope.workWithData($scope.players);
      $scope.players.loader = false;
      if (typeof callback === 'function') {
        return callback(callbackArg);
      }
    };
    $scope.list();
    $('.b-tabs-content').visibility({
      'once': false,
      'observeChanges': true,
      'onBottomVisible': function() {
        var newSeason;
        newSeason = 1;
        if ($scope.seasons.length > 0 && fromSeason($scope.season) !== 1997) {
          return $scope.setSeason(toSeason(fromSeason($scope.season) - 1), true);
        }
      }
    });
  }
]);
