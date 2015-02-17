var app = angular.module('Sportomatics');

app.config(function($routeProvider) {
    $routeProvider
    .when('/rated_by/:ratedBy/', {
        controller: 'PlayersSearchController'
    });
});

app.service('PlayersSearchService', function($http) {
    this.loadCountries = function($scope) {
        var url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
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
                });
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

    this.search = function($scope) {
        var url = $('#PlayersSearchLink').attr('href'),
        params = $('#PlayersSearchForm').serialize();
        if (!$scope.countries) {
            this.loadCountries($scope);
        }
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

app.controller('PlayersSearchController', [
    '$route', '$http', '$scope', 'PlayersSearchService',
    function($route, $http, $scope, PlayersSearchService) {
    var self = this,
        url = $('#PlayersSearchForm').attr('action'),
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

    $scope.PlayersSearchService = PlayersSearchService;

    $scope.data = {};
    $scope.countries = null;
    $scope.loader = false;

    $scope.params = {
        orderBy: '[%22%s_lastname%22,%22%s_name%22]',
        orderByReversed: false,
        ratedBy: '',
        alphabetFilter: null,
        isPlaying: true,
        playersFilter: null,
        clubsFilter: null,
        countriesSelected: [],
        leaguesSelected: []
    };

    $scope.PlayerPartnersPopup = {
        data: null,
        isClubsVisible: false
    };
    $scope.PlayerPartnersPopupShow = function(e, event) {
        var popup = $('.player-partners-popup:hidden'),
        url = $('#PlayerCardLink').attr('href');
        if (popup.length) {
            $scope.PlayerPartnersPopup.data = null;
            $http.get(url.replace(0, this.player.pk))
            .success(function(data) {
                $scope.PlayerPartnersPopup.data = data;
            });
            $('.player-partners-popup:hidden').show(500).offset({
                left: event.pageX,
                top: event.pageY
            });
        }
    };

    $scope.moreClubs = function(e) {
        $(e).closest('td').toggleClass('show-more-clubs')
    };

    $scope.lineCheck = function(e) {
        var defaultValue = '[0,1,2,3]',
            isDefault;
        isDefault = $(e).attr('value') === defaultValue;
        if ($(e).is(':checked')) {
            $('input[name="line"]').each(getUnchecker(isDefault, defaultValue));
        }
    };

    $scope.setCitizenship = function(event) {
        if (event.target.id === 'isCitizenshipAll' && event.target.checked) {
            $('#isCitizenshipRussia').attr('checked', false);
            $('#isCitizenshipOther').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipRussia' && event.target.checked) {
            $('#isCitizenshipAll').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipOther' && event.target.checked) {
            self.isCitizenshipOther = event.target.checked;
            self.isCitizenshipAll = false;
            $('#isCitizenshipAll').attr('checked', false);
        }
    }

    $scope.contractCheck = function(e) {
        var isDefault = $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="contract"]').each(getUnchecker(isDefault, ''));
        }
    };

    this.setPlaying = function(isPlaying) {
        if (!$scope.loader && $scope.params.isPlaying !== isPlaying) {
            $scope.params.isPlaying = isPlaying;
            PlayersSearchService.search($scope);
        }
    }

    this.setRatedBy = function(ratedBy) {
        if (!$scope.loader && $scope.params.ratedBy !== ratedBy) {
            $scope.params.ratedBy = ratedBy;
            if (ratedBy) {
                $scope.params.orderBy = 'rating';
                $scope.params.orderByReversed = true;
                PlayersSearchService.search($scope);
            } else {
                this.setOrderBy('[%22%s_lastname%22,%22%s_name%22]');
            }
        }
    };

    this.setAlphabetFilter = function(alphabetFilter) {
        if (!$scope.loader && $scope.params.alphabetFilter !== alphabetFilter) {
            $scope.params.alphabetFilter = alphabetFilter;
            PlayersSearchService.search($scope);
        }
    };

    this.setPlayersFilter = function(obj) {
        var value;
        if (obj) {
            value = obj.originalObject;
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.palyersFilter !== value) {
            $scope.params.palyersFilter !== value
            PlayersSearchService.search($scope);
        }
    };

    this.setClubsFilter = function(obj) {
        var value;
        if (obj) {
            value = obj.originalObject;
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.clubsFilter !== value) {
            $scope.params.clubsFilter !== value
            PlayersSearchService.search($scope);
        }
    };

    this.isMatchesTotalVisible = function() {
        return (self.ratedBy === 'goals_average' ||
            self.ratedBy === 'assists_average' ||
            self.ratedBy === 'points_average' ||
            self.ratedBy === 'plus_minus_average')
    }

    this.setOrderBy = function(orderBy) {
        if (!$scope.loader) {
            if ($scope.params.orderBy === orderBy) { // same field -> reverse
                $scope.params.orderByReversed = !$scope.params.orderByReversed;
            } else { // other field -> reset
                $scope.params.orderByReversed = false;
            }
            $scope.params.orderBy = orderBy;
            PlayersSearchService.search($scope);
        }
    }

    PlayersSearchService.search($scope);
}]);
