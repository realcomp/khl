angular.module('Sportomatics')
.service('PlayersSearchService', function($http) {
    this.loadCountries = function($scope, callback) {
        var url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url).success(function(data) {
                $scope.countries = data;
                if ($scope.countries.length) { // has countries
                    if (Array.isArray($scope.params.countriesSelected) &&
                        $scope.params.countriesSelected.length === 0) { // array is expected
                        $scope.params.countriesSelected = [String($scope.countries[0].pk)];
                    } else {
                        $scope.params.countriesSelected = $scope.countries[0].pk;
                    }
                    if ($scope.countries[0].league_set.length) { // has leagues
                        if (Array.isArray($scope.params.leaguesSelected) &&
                            $scope.params.leaguesSelected.length === 0) { // array is expected
                            $scope.params.leaguesSelected = [String($scope.countries[0].league_set[0].pk)];
                        } else {
                            $scope.params.leaguesSelected = $scope.countries[0].league_set[0].pk;
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
        return ($scope.params.ratedBy === 'goals_average' ||
            $scope.params.ratedBy === 'assists_average' ||
            $scope.params.ratedBy === 'points_average' ||
            $scope.params.ratedBy === 'plus_minus_average')
    }

    this.setOrderBy = function($scope, orderBy) {
        if (!$scope.loader) {
            if ($scope.params.orderBy === orderBy) { // same field -> reverse
                $scope.params.orderByReversed = !$scope.params.orderByReversed;
            } else { // other field -> reset
                $scope.params.orderByReversed = false;
            }
            $scope.params.orderBy = orderBy;
            this.search($scope);
        }
    };

    this.setPlaying = function($scope, isPlaying) {
        if (!$scope.loader && $scope.params.isPlaying !== isPlaying) {
            $scope.params.isPlaying = isPlaying;
            this.search($scope);
        }
    }

    this.setRatedBy = function($scope, ratedBy) {
        if (!$scope.loader && $scope.params.ratedBy !== ratedBy) {
            $scope.params.ratedBy = ratedBy;
            if (ratedBy) {
                $scope.params.orderBy = 'rating';
                $scope.params.orderByReversed = true;
                this.search($scope);
            } else {
                this.setOrderBy($scope, '[%22%s_lastname%22,%22%s_name%22]');
            }
        }
    };

    this.setAlphabetFilter = function($scope, alphabetFilter) {
        if (!$scope.loader && $scope.params.alphabetFilter !== alphabetFilter) {
            $scope.params.alphabetFilter = alphabetFilter;
            this.search($scope);
        }
    };

    this.setPlayersFilter = function($scope, obj) {
        var value;
        if (obj) {
            value = obj.originalObject;
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.playersFilter !== value) {
            $scope.params.playersFilter = value;
            this.search($scope);
        }
    };

    this.setClubsFilter = function($scope, obj) {
        var value;
        if (obj) {
            value = obj.originalObject;
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.clubsFilter !== value) {
            $scope.params.clubsFilter = value;
            this.search($scope);
        }
    };

    this.search = function($scope) {
        var f = function() {
            var url = $('#PlayersSearchLink').attr('href'),
            params = $('#PlayersSearchForm').serialize();
            params += '&order_by=' + ($scope.params.orderByReversed ? '-' : '') + $scope.params.orderBy;
            if ($scope.params.ratedBy) {
                params += '&rated_by=' + $scope.params.ratedBy;
            }
            if ($('#isCitizenshipRussia').is(':checked')) {
                params += '&citizenship=' + $('#citizenshipRussia').val();
            }
            if ($('#isCitizenshipOther').is(':checked')) {
                if ($('#citizenshipOther').val()) {
                    params += '&citizenship=' + $('#citizenshipOther').val();
                } else {
                    params += '&citizenship_other=true';
                }
            }
            if ($scope.params.isPlaying) {
                params += '&is_playing=true';
            }
            if ($scope.params.alphabetFilter) {
                params += '&%s_lastname__startswith=' + $scope.params.alphabetFilter;
            }
            if ($scope.params.clubsFilter) {
                params += '&club=' + $scope.params.clubsFilter.pk;
            }
            if ($scope.params.playersFilter) {
                params += '&player=' + $scope.params.playersFilter.pk;
            }
            $.each($scope.params.leaguesSelected, function() {
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
