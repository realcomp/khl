var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').service('PlayersSearchService', function($http) {
  this.loadCountries = function($scope, $location, callback) {
    var url;
    url = $('#LeagueListLink').attr('href');
    if (url) {
      $http.get(url).success(function(data) {
        var country;
        $scope.countries = data;
        if ($scope.countries.length) {
          country = $scope.countries[0];
          if (!$location.search().country) {
            $scope.params = $location.search();
          }
          if (country.league_set.length && !$location.search().league && $location.search().league !== '') {
            $scope.params = $location.search();
          }
        }
        if (callback && typeof callback === 'function') {
          return callback($scope);
        }
      });
    } else if (callback && typeof callback === 'function') {
      callback($scope);
    }
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
    if (!$scope.loader) {
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
    if (!$scope.loader && $scope.params.is_playing !== is_playing) {
      if (is_playing === 'false') {
        $scope.$location.search('is_playing', is_playing);
      } else {
        $scope.$location.search('is_playing', null);
      }
      this.search($scope);
    }
  };
  this.setRatedBy = function($scope, rated_by) {
    if (!$scope.loader && $scope.params.rated_by !== rated_by) {
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
    if (!$scope.loader && $scope.params.alphabet !== alphabet) {
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
    if (!$scope.loader && $scope.params.player !== value) {
      $scope.$location.search('player', value);
      this.search($scope);
    }
  };
  this.setClubsFilter = function($scope, obj) {
    var value;
    if (obj) {
      value = String(obj.originalObject.pk);
    } else {
      value = null;
    }
    if (!$scope.loader && $scope.params.club !== value) {
      $scope.$location.search('club', value);
      this.search($scope);
    }
  };
  this.search = function($scope) {
    var age, d, e, league, line, params, url, x;
    url = $('#PlayersSearchLink').attr('href');
    params = '';
    if ($('#isCitizenshipRussia').is(':checked')) {
      $scope.$location.search('citizenship1', $('#citizenshipRussia').val());
    } else {
      $scope.$location.search('citizenship1', null);
    }
    if ($('#isCitizenshipOther').is(':checked')) {
      $scope.$location.search('citizenship_other', 'true');
      if ($scope.$location.search().citizenship2) {
        $('#citizenshipOther').val($scope.$location.search().citizenship2);
      }
      if ($('#citizenshipOther').val()) {
        $scope.$location.search('citizenship2', $('#citizenshipOther').val());
      }
    } else {
      $scope.$location.search('citizenship_other', null);
    }
    line = (function() {
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
    $scope.$location.search('line', line || []);
    $scope.$location.search('contract_type__isnull', $('[name="contractTypeNull"]').is(':checked') || null);
    $scope.$location.search('citizenship_reversed', $('[name="citizenshipReversed"]').is(':checked') || null);
    if ($scope.citizenship) {
      $scope.$location.search('citizenship', (function() {
        var i, len, ref, results;
        ref = $scope.citizenship;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push(x['pk']);
        }
        return results;
      })());
    } else {
      $scope.$location.search('citizenship', null);
    }
    if ($scope.number) {
      $scope.$location.search('number', $scope.number);
    }
    if ($('[name="age"]').length) {
      age = $('[name="age"]').val().split(';');
      $scope.$location.search('age__lte', age[0]);
      $scope.$location.search('age__gte', age[1]);
    }
    $scope.params = $scope.$location.search();
    params += 'order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
    if ($scope.params.reversed) {
      params += '&reversed=true';
    }
    if ($scope.params.line.length) {
      params += '&line=' + $scope.params.line.join('&line=');
    }
    if ($scope.params.citizenship1) {
      params += '&citizenship=' + $scope.params.citizenship1;
    }
    if ($scope.params.citizenship2) {
      params += '&citizenship=' + $scope.params.citizenship2;
    }
    if ($scope.params.citizenship_other === 'true') {
      params += '&citizenship_other=true';
    }
    if ($scope.params.rated_by) {
      params += '&rated_by=' + $scope.params.rated_by;
    }
    if ($scope.params.is_playing !== 'false') {
      params += '&is_playing=true';
    }
    if ($scope.params.alphabet) {
      params += '&%s_lastname__startswith=' + $scope.params.alphabet;
    }
    if ($scope.params.club) {
      params += '&club=' + $scope.params.club;
    }
    if ($scope.params.player) {
      params += '&player=' + $scope.params.player;
    }
    if ($scope.params.season) {
      params += '&season=' + $scope.params.season;
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
    if ($scope.params.number) {
      params += '&number=' + $scope.params.number;
    }
    if ($scope.params.contract_type) {
      params += '&contract_type=' + $scope.params.contract_type;
    }
    if ($scope.params.contract_to) {
      d = $scope.params.contract_to.split('/');
      params += '&contract_to=' + d[2] + '-' + d[0] + '-' + d[1];
    }
    if ($scope.params.height) {
      params += '&height=' + $scope.params.height;
    }
    if ($scope.params.weight) {
      params += '&weight=' + $scope.params.weight;
    }
    if ($scope.params.grip) {
      params += '&grip=' + $scope.params.grip;
    }
    if ($scope.params.contract_type__isnull) {
      params += '&contract_type__isnull=true';
    }
    if ($scope.params.age__lte) {
      params += '&age__lte=' + $scope.params.age__lte;
    }
    if ($scope.params.age__gte) {
      params += '&age__gte=' + $scope.params.age__gte;
    }
    if ($scope.params.citizenship_reversed) {
      params += '&citizenship_reversed=true';
    }
    if ($scope.params.citizenship) {
      params += ((function() {
        var i, len, ref, results;
        ref = $scope.citizenship;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&citizenship=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    $scope.data = {};
    $scope.loader = true;
    $http.get(url + '?' + params).success(function(data) {
      $scope.data = data;
      return $scope.loader = false;
    });
  };
  this.next = function($scope, isAll) {
    var url;
    url = $scope.data.next;
    if (isAll) {
      url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
    }
    $scope.loader = true;
    $http.get(url).success(function(data) {
      if (isAll) {
        $scope.data = data;
      } else {
        $scope.data.next = data.next;
        $scope.data.results = $scope.data.results.concat(data.results);
      }
      return $scope.loader = false;
    });
  };
});
