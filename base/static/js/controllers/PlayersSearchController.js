var app = angular.module('Sportomatics');

app.config(function($routeProvider) {
    $routeProvider
    .when('/rated_by/:ratedBy/', {
        controller: 'PlayersSearchController'
    });
});

app.controller('PlayersSearchController', [
    '$route', '$http', '$scope',
    function($route, $http, $scope) {
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

    this.data = {};
    this.order_by = '[%22%s_lastname%22,%22%s_name%22]';
    this.order_by_reversed = false;
    this.ratedBy = '';
    this.alphabetFilter = null;
    this.isPlaying = true;
    this.playersFilter = null;
    this.clubsFilter = null;

    this.loader = false;
    this.countries_selected = [];
    this.leagues_selected = [];

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

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

    this.search = function(order_by) {
        var params = $('#PlayersSearchForm').serialize();
        if (order_by) {
            if (self.order_by === order_by) { // same field -> reverse
                self.order_by_reversed = !self.order_by_reversed;
            } else { // other field -> reset
                self.order_by_reversed = false;
            }
            self.order_by = order_by;
        }
        params += '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
        if (self.ratedBy) {
            params += '&rated_by=' + self.ratedBy;
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
        if (self.isPlaying) {
            params += '&is_playing=true';
        }
        if (self.alphabetFilter) {
            params += '&%s_lastname__startswith=' + self.alphabetFilter;
        }
        if (self.clubsFilter) {
            params += '&club=' + self.clubsFilter.pk;
        }
        if (self.playersFilter) {
            params += '&player=' + self.playersFilter.pk;
        }
        $.each(self.leagues_selected, function() {
            params += '&league=' + this;
        });
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.setPlaying = function(isPlaying) {
        if (!this.loader) {
            this.isPlaying = isPlaying;
            this.search();
        }
    }

    this.setRatedBy = function(ratedBy) {
        if (!this.loader) {
            this.ratedBy = ratedBy;
            if (ratedBy) {
                this.order_by = 'rating';
                this.order_by_reversed = true;
                this.search();
            } else {
                this.search('[%22%s_lastname%22,%22%s_name%22]');
            }
        }
    };

    this.setAlphabetFilter = function(alphabetFilter) {
        if (!this.loader) {
            this.alphabetFilter = alphabetFilter;
            this.search();
        }
    };

    this.setPlayersFilter = function(obj) {
        if (obj) {
            self.playersFilter = obj.originalObject;
        } else {
            self.playersFilter = null;
        }
        self.search();
    };

    this.setClubsFilter = function(obj) {
        if (obj) {
            self.clubsFilter = obj.originalObject;
        } else {
            self.clubsFilter = null;
        }
        self.search();
    };

    this.next = next($http);

    this.getCountries(this.search);
}])

var next = function($http) {
    return function(isAll) {
        var self = this,
            url = self.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + self.data.count);
        }
        self.loader = true;
        $http.get(url)
            .success(function(data) {
                if (isAll) {
                    self.data = data;
                } else {
                    self.data.next = data.next;
                    self.data.results = self.data.results.concat(data.results);
                }
                self.loader = false;
            });
    };
}

var getCountries = function($http) {
    return function(callback) {
        var self = this,
            url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
                    self.countries = data;
                    if (self.countries.length) { // has countries
                        if (Array.isArray(self.countries_selected) &&
                            self.countries_selected.length === 0) { // array is expected
                            self.countries_selected = [String(self.countries[0].pk)];
                        } else {
                            self.countries_selected = self.countries[0].pk;
                        }
                        if (self.countries[0].league_set.length) { // has leagues
                            if (Array.isArray(self.leagues_selected) &&
                                self.leagues_selected.length === 0) { // array is expected
                                self.leagues_selected = [String(self.countries[0].league_set[0].pk)];
                            } else {
                                self.leagues_selected = self.countries[0].league_set[0].pk;
                            }
                        }
                    }
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
        }
    };
}

var getLeagues = function(countries, countries_selected) {
    var result = [];
    $.each(countries_selected, function() {
        var pk = this;
        $.each(countries, function() {
            if (this.pk == pk) {
                result = result.concat(this.league_set);
            }
        });
    });
    return result;
}
