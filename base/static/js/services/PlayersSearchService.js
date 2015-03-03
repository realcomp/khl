angular.module('Sportomatics')
.service('PlayersSearchService', function($http) {
    this.loadCountries = function($scope, callback) {
        var url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url).success(function(data) {
                $scope.countries = data;
                if ($scope.countries.length) { // has countries
                    if (Array.isArray($scope.sparams.countriesSelected) &&
                        $scope.sparams.countriesSelected.length === 0) { // array is expected
                        $scope.sparams.countriesSelected = [String($scope.countries[0].pk)];
                    } else {
                        $scope.sparams.countriesSelected = $scope.countries[0].pk;
                    }
                    if ($scope.countries[0].league_set.length) { // has leagues
                        if (Array.isArray($scope.sparams.leaguesSelected) &&
                            $scope.sparams.leaguesSelected.length === 0) { // array is expected
                            $scope.sparams.leaguesSelected = [String($scope.countries[0].league_set[0].pk)];
                        } else {
                            $scope.sparams.leaguesSelected = $scope.countries[0].league_set[0].pk;
                        }
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

    this.getLeagues = function(countries, countriesSelected) {
        var result = [];
        $.each(countriesSelected, function() {
            var pk = this;
            $.each(countries, function() {
                if (this.pk == pk) {
                    result = result.concat(this.league_set);
                }
            });
        });
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
            if ($scope.params.order_by === order_by) { // same field -> reverse
                $scope.$location.search('reversed', !$scope.params.reversed);
            } else { // other field -> reset
                $scope.$location.search('reversed', false);
            }
            $scope.$location.search('order_by', order_by);
            this.search($scope);
        }
    };

    this.setPlaying = function($scope, is_playing) {
        if (!$scope.loader && $scope.params.is_playing !== is_playing) {
            $scope.$location.search('is_playing', is_playing);
            this.search($scope);
        }
    }

    this.setRatedBy = function($scope, rated_by) {
        if (!$scope.loader && $scope.params.rated_by !== rated_by) {
            $scope.$location.search('rated_by', rated_by);
            if (rated_by) { // by rating -> set ordering
                $scope.$location.search('order_by', 'rating');
                $scope.$location.search('reversed', true);
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
            citizenship = [], line = [], params = '';

            if ($('#isCitizenshipRussia').is(':checked')) {
                citizenship.push($('#citizenshipRussia').val());
            }
            if ($('#isCitizenshipOther').is(':checked')) {
                if ($('#citizenshipOther').val()) {
                    citizenship.push($('#citizenshipOther').val());
                } else {
                    $scope.$location.search('citizenship_other', true);
                }
            }
            $scope.$location.search('citizenship', citizenship);

            $.each($('[name="line"]:checked'), function() {
                line.push($(this).val());
            });
            $scope.$location.search('line', line);

            $scope.params = $scope.$location.search();

            params += '&order_by=' + ($scope.params.reversed ? '-' : '') +
                ($scope.params.order_by || '["%s_lastname","%s_name"]');

            $.each($scope.params.citizenship, function() {
                params += '&citizenship=' + this;
            });
            $.each($scope.params.line, function() {
                params += '&line=' + this;
            });
            if ($scope.params.citizenship_other) {
                params += '&citizenship_other=' + $scope.params.citizenship_other;
            }
            if ($scope.params.rated_by) {
                params += '&rated_by=' + $scope.params.rated_by;
            }
            if ($scope.params.is_playing) {
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
            $.each($scope.sparams.leaguesSelected, function() {
                params += '&league=' + this;
            });
            $scope.data = {};
            $scope.loader = true;
            $http.get(url + '?' + params).success(function(data) {
                $scope.data = data;
                $scope.loader = false;
            });
        };

        if (!$scope.countries) {
             this.loadCountries($scope, f);
        } else {
            f($scope);
        }
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
