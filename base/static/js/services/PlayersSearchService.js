var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').service('PlayersSearchService', function($http, $timeout) {
  this.loadCountries = function($scope, $location, callback) {
    var url;
    url = $('#LeagueListLink').attr('href');
    if (url) {
      $http.get(url).success(function(data) {
        $scope.countries = data;
        $timeout(function() {
          return $('.ui.dropdown.leagues').dropdown();
        }, 0);
        if (callback && typeof callback === 'function') {
          return callback($scope);
        }
      });
    } else if (callback && typeof callback === 'function') {
      callback($scope);
    }
  };
  this.setCountries = function($scope, countries) {
    $scope.countriesSelected = countries;
    $scope.leaguesSelected = [];
    $scope.$location.search('country', countries || null);
    $scope.$location.search('league', null);
  };
  this.getLeagues = function(countries, selected) {
    var country, league_sets, x;
    if (countries && selected) {
      if (!Array.isArray(selected)) {
        selected = [selected];
      }
      selected = (function() {
        var i, len, results;
        results = [];
        for (i = 0, len = selected.length; i < len; i++) {
          x = selected[i];
          results.push(+x);
        }
        return results;
      })();
      league_sets = (function() {
        var i, len, ref, results;
        results = [];
        for (i = 0, len = countries.length; i < len; i++) {
          country = countries[i];
          if (ref = country.pk, indexOf.call(selected, ref) >= 0) {
            results.push(country.league_set);
          }
        }
        return results;
      })();
      return [].concat.apply([], league_sets);
    }
    return [];
  };
  this.isMatchesTotalVisible = function($scope) {
    var ref;
    return (ref = $scope.params.rated_by) === 'goals_average' || ref === 'assists_average' || ref === 'points_average' || ref === 'plus_minus_average';
  };
  this.setOrderBy = function($scope, order_by) {
    if ($scope.loaded) {
      if ($scope.params.order_by === order_by || (!$scope.params.order_by && !order_by)) {
        if ($scope.params.reversed === 'true') {
          $scope.$location.search('reversed', null);
        } else {
          $scope.$location.search('reversed', 'true');
        }
      } else {
        $scope.$location.search('reversed', null);
      }
      $scope.$location.search('order_by', order_by || null);
      this.search($scope);
    }
  };
  this.setPlaying = function($scope, is_playing) {
    if ($scope.loaded && $scope.params.is_playing !== is_playing) {
      if (is_playing === 'false') {
        $scope.$location.search('is_playing', is_playing);
      } else {
        $scope.$location.search('is_playing', null);
      }
      this.search($scope);
    }
  };
  this.setRatedBy = function($scope, rated_by) {
    if ($scope.loaded && $scope.params.rated_by !== rated_by) {
      $scope.$location.search('alphabet', null);
      $scope.$location.search('rated_by', rated_by || null);
      if (rated_by) {
        $scope.$location.search('order_by', 'rating');
        $scope.$location.search('reversed', 'true');
        this.search($scope);
      } else {
        this.setOrderBy($scope, '');
      }
    }
  };
  this.setAlphabetFilter = function($scope, alphabet) {
    if ($scope.loaded && $scope.params.alphabet !== alphabet) {
      $scope.$location.search('alphabet', alphabet);
      this.search($scope);
    }
  };
  this.setPlayersFilter = function($scope, obj) {
    var value;
    if (obj) {
      value = String(obj.originalObject.pk);
    } else {
      value = null;
    }
    if ($scope.loaded && $scope.params.player !== value) {
      $scope.$location.search('player', value);
      this.search($scope);
    }
  };
  this.setClubsFilter = function($scope, obj) {
    var value;
    if (obj) {
      value = [obj.originalObject];
    } else {
      value = null;
    }
    if ($scope.loaded && $scope.club !== value) {
      $scope.club = value;
      this.search($scope);
    }
  };
  this.search = function($scope) {
    var age, checkBox, contract_types, d, e, k, league, lineAll, lineChecked, lineUnchecked, multiSelect, params, relatedValue, url, x;
    checkBox = function($scope, search, name) {
      $scope.$location.search(search, $('[name="' + name + '"]').is(':checked') || null);
    };
    multiSelect = function($scope, search, value) {
      if (value && value.length) {
        $scope.$location.search(search, JSON.stringify(value));
      } else {
        $scope.$location.search(search, null);
      }
    };
    url = $('#players-search-api').val();
    params = '';
    if ($('#isCitizenshipRussia').is(':checked')) {
      $scope.$location.search('citizenship1', $('#citizenshipRussia').val());
    } else {
      $scope.$location.search('citizenship1', null);
    }
    if ($('#isCitizenshipOther').is(':checked')) {
      $scope.$location.search('citizenship_other', 'true');
    } else {
      $scope.$location.search('citizenship_other', null);
    }
    lineAll = (function() {
      var i, len, ref, results;
      ref = $('[name="line"]');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    lineChecked = (function() {
      var i, len, ref, results;
      ref = $('[name="line"]:checked');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    lineUnchecked = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineAll.length; i < len; i++) {
        e = lineAll[i];
        if (indexOf.call(lineChecked, e) < 0) {
          results.push(e);
        }
      }
      return results;
    })();
    $scope.$location.search('line', ((function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineChecked.length; i < len; i++) {
        e = lineChecked[i];
        if (+e > 0) {
          results.push(e);
        }
      }
      return results;
    })()) || []);
    $scope.$location.search('line', ((function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineUnchecked.length; i < len; i++) {
        e = lineUnchecked[i];
        if (+e < 0) {
          results.push(e);
        }
      }
      return results;
    })()) || []);
    contract_types = (function() {
      var i, len, ref, results;
      ref = $('[name="contract_types"]:checked');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    $scope.$location.search('contract_types', contract_types || []);
    checkBox($scope, 'contract_type__isnull', 'contractTypeNull');
    checkBox($scope, 'citizenship_reversed', 'citizenshipReversed');
    checkBox($scope, 'season_enabled', 'seasonEnabled');
    checkBox($scope, 'club_enabled', 'clubEnabled');
    checkBox($scope, 'league_enabled', 'league2Enabled');
    checkBox($scope, 'related_enabled', 'relatedEnabled');
    multiSelect($scope, 'citizenship', $scope.citizenship);
    multiSelect($scope, 'club', $scope.club);
    multiSelect($scope, 'league2', $scope.league2);
    multiSelect($scope, 'related_player', $scope.relatedPlayer);
    if ($scope.number) {
      $scope.$location.search('number', $scope.number);
    }
    if ($('[name="age"]').length) {
      age = $('[name="age"]').val().split(';');
      $scope.$location.search('age__lte', age[0]);
      $scope.$location.search('age__gte', age[1]);
    }
    if ($('[name="relatedValue"]').length) {
      relatedValue = $('[name="relatedValue"]').val().split(';');
      $scope.$location.search('related_value__gte', relatedValue[0]);
      $scope.$location.search('related_value__lte', relatedValue[1]);
    }
    $scope.params = $scope.$location.search();
    params += ((function() {
      var i, len, ref, results;
      ref = ['player', 'season', 'number', 'contract_type', 'height', 'height__gte', 'height__lte', 'weight', 'weight__gte', 'weight__lte', 'grip', 'match_count', 'rated_by', 'age__lte', 'age__gte', 'gamingtime', 'related_value__lte', 'related_value__gte'];
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        k = ref[i];
        if ($scope.params[k]) {
          results.push(k + '=' + $scope.params[k]);
        }
      }
      return results;
    })()).join('&');
    params += '&order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
    if ($scope.params.reversed) {
      params += '&reversed=true';
    }
    if (lineChecked.length) {
      params += ((function() {
        var i, len, results;
        results = [];
        for (i = 0, len = lineChecked.length; i < len; i++) {
          x = lineChecked[i];
          results.push('&line=' + Math.abs(+x));
        }
        return results;
      })()).join('');
    }
    if ($scope.params.contract_types) {
      params += ((function() {
        var i, len, ref, results;
        ref = $scope.params.contract_types;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&contract_types=' + x);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.citizenship1) {
      params += '&citizenship=' + $scope.params.citizenship1;
    }
    if ($scope.params.citizenship_other === 'true') {
      if ($scope.params.citizenship2) {
        params += '&citizenship=' + $scope.params.citizenship2;
      } else {
        params += '&citizenship_other=true';
      }
    }
    if ($scope.params.is_playing !== 'false') {
      params += '&is_playing=true';
    }
    if ($scope.params.alphabet) {
      params += '&%s_lastname__startswith=' + $scope.params.alphabet;
    }
    if (($scope.club_enabled || $scope.params.club_enabled) && $scope.params.club) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.club);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&club=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.league) {
      params += ((function() {
        var i, len, ref, results;
        ref = $scope.params.league;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          league = ref[i];
          results.push('&league=' + league);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.contract_to) {
      d = $scope.params.contract_to.split('/');
      params += '&contract_to=' + d[2] + '-' + d[0] + '-' + d[1];
    }
    if ($scope.params.contract_type__isnull) {
      params += '&contract_type__isnull=true';
    }
    if ($scope.params.citizenship_reversed) {
      params += '&citizenship_reversed=true';
    }
    if ($scope.params.citizenship) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.citizenship);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&citizenship=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.league_enabled && $scope.params.league2) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.league2);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&league=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.season_enabled) {
      if ($scope.params.season_start && $scope.params.season_end) {
        params += '&season_start=' + $scope.params.season_start + '&season_end=' + $scope.params.season_end;
      }
    }
    if ($scope.params.related_enabled && $scope.params.related_player && $scope.params.related_field) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.related_player);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&related_player=' + x['pk']);
        }
        return results;
      })()).join('');
      params += '&related_field=' + $scope.params.related_field;
    }
    $scope.data = {};
    $scope.loaded = false;
    $http.get(url + '?' + params).success(function(data) {
      $scope.data = data;
      return $scope.loaded = true;
    });
  };
  this.next = function($scope, isAll) {
    var url;
    url = $scope.data.next;
    if (isAll) {
      url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
    }
    $scope.loaded = false;
    $http.get(url).success(function(data) {
      if (isAll) {
        $scope.data = data;
      } else {
        $scope.data.next = data.next;
        $scope.data.results = $scope.data.results.concat(data.results);
      }
      return $scope.loaded = true;
    });
  };
});
