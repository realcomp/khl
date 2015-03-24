angular.module('Sportomatics')
.service('PlayersSearchService', function($http) {
    this.loadCountries = function($scope, $location, callback) {
        var url = $('#LeagueListLink').attr('href'),
        country;
        if (url) {
            $http.get(url).success(function(data) {
                $scope.countries = data;
                if ($scope.countries.length) {
                    country = $scope.countries[0];
                    if (!$location.search().country) {
                        $location.search('country', String(country.pk));
                        $scope.params = $location.search();
                    }
                    if (country.league_set.length &&
                            !$location.search().league &&
                            $location.search().league !== '') {
                        $location.search('league', String(country.league_set[0].pk));
                        $scope.params = $location.search();
                    }
                }
                if (callback && typeof callback === 'function') {
                    callback($scope);
                }
            });
        } else if (callback && typeof callback === 'function') {
            callback($scope);
        }
    };

    this.getLeagues = function(countries, selected) {
        var result = [];
        if (selected) {
            if (Array.isArray(selected)) {
                $.each(selected, function() {
                    var pk = this;
                    $.each(countries, function() {
                        if (this.pk == pk) {
                            result = result.concat(this.league_set);
                        }
                    });
                });
            } else {
                $.each(countries, function() {
                    if (this.pk == selected) {
                        result = result.concat(this.league_set);
                    }
                });
            }
        }
        return result;
    };

    this.isMatchesTotalVisible = function($scope) {
        return ($scope.params.rated_by === 'goals_average' ||
            $scope.params.rated_by === 'assists_average' ||
            $scope.params.rated_by === 'points_average' ||
            $scope.params.rated_by === 'plus_minus_average')
    }

    this.setOrderBy = function($scope, order_by) {
        if (!$scope.loader) {
            if ($scope.params.order_by === order_by ||
                    (!$scope.params.order_by && !order_by)) { // same field -> reverse
                if ($scope.params.reversed === 'true') {
                    $scope.$location.search('reversed', null);
                } else {
                    $scope.$location.search('reversed', 'true');
                }
            } else { // other field -> reset
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
    }

    this.setRatedBy = function($scope, rated_by) {
        if (!$scope.loader && $scope.params.rated_by !== rated_by) {
            $scope.$location.search('alphabet', null);
            $scope.$location.search('rated_by', rated_by || null);
            if (rated_by) { // by rating -> set ordering
                $scope.$location.search('order_by', 'rating');
                $scope.$location.search('reversed', 'true');
                this.search($scope);
            } else { // by alphabet -> reset ordering
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
        var f = function() {
            var url = $('#PlayersSearchLink').attr('href'),
            line = [], params = '', i;

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

            $.each($('[name="line"]:checked'), function() {
                var value = $(this).val();
                if (value) {
                    line.push(value);
                }
            });
            $scope.$location.search('line', line);

            if (!$scope.leaguesLoaded) {
                $scope.leaguesLoaded = true;
                if ($scope.params.league) {
                    if (Array.isArray($scope.params.league)) {
                        $scope.leaguesSelected = $scope.params.league;
                    } else {
                        $scope.leaguesSelected = [$scope.params.league];
                    }
                }
            }
            $scope.$location.search('league', $scope.leaguesSelected);

            $scope.params = $scope.$location.search();

            params += '&order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
            if ($scope.params.reversed) {
                params += '&reversed=true';
            }
            if ($scope.params.line.length) {
                $.each($scope.params.line, function() {
                    params += '&line=' + this;
                });
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
            if ($scope.params.league) {
                $.each($scope.params.league, function() {
                    params += '&league=' + this;
                });
            }
            $scope.data = {};
            $scope.loader = true;
            $http.get(url + '?' + params).success(function(data) {
                $scope.data = data;
                $scope.loader = false;
            });
        };

        // if (!$scope.countries) {
        //      this.loadCountries($scope, $scope.$location, f);
        // } else {
            f($scope);
        // }
    };

    this.next = function($scope, isAll) {
        var url = $scope.data.next;
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
            $scope.loader = false;
        });
    };
});
