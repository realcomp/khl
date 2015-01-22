(function() {
    var app = angular.module('Sportomatics', []);

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
    };

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
    };

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
    };

    app.controller('ProfileController', ['$http', '$scope', function($http, $scope) {
        var self = this;

        self.user = {};
        self.csrf_token = null;

        $http.get('/en/accounts/api/profile/')
        .success(function(data) {
            self.user = data;
        });

        $scope.setAvatar = function(files, csrf_token) {
            var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': undefined
                },
                'withCredentials': true,
                'transformRequest': angular.identity
            },
            fd = new FormData();
            fd.append('avatar', files[0]);
            $http.patch('/en/accounts/api/profile/', fd, config)
            .success(function(data) {
                $('#id_avatar').attr('src', data.avatar);
                $('.user-avatar-hex2').css(
                    'background-image', 'url(' + data.avatar + ')');
            })
            .error(function(data) {
                // TODO: handle image upload errors
            });
        };

        this.save = function() {
            var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': this.csrf_token
                }
            };
            // TODO: replace url
            $http.patch('/en/accounts/api/profile/', {
                'fio': self.user.fio,
                'email': self.user.email
            }, config)
            .success(function(data) {
                self.user = data;
            });
        };
    }]);

    app.controller('PlayersSearchController', ['$http', '$scope', function($http, $scope) {
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
        this.loader = false;
        this.countries_selected = [];
        this.leagues_selected = [];

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

        $scope.citizenshipCheck = function(e) {
            var isDefault = $(e).attr('name') === 'citizenship' && $(e).attr('value') === '';
            if ($(e).is(':checked')) {
                $('input[name="citizenship"]').each(getUnchecker(isDefault, ''));
                $('input[name="citizenship_other_active"]').each(getUnchecker(isDefault, ''));
            }
        };

        $scope.contractCheck = function(e) {
            var isDefault = $(e).attr('value') === '';
            if ($(e).is(':checked')) {
                $('input[name="contract"]').each(getUnchecker(isDefault, ''));
            }
        };

        $scope.showPopup = function(e) {
            var block = $(e).closest('.player-avatar-block');
            block.children('.player-avatar-block-popup').show();
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
            params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
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

        this.next = next($http);

        this.getCountries(this.search);
    }]);

    app.controller('ClubListController', ['$http', '$scope', function($http, $scope) {
        var self = this,
        url = $('#ClubListForm').attr('action');
        this.data = {};
        this.order_by = '%s_title';
        this.order_by_reversed = false;
        this.loader = false;
        this.countries = {};
        this.countries_selected = [];
        this.leagues_selected = '';

        $scope.setSeason = function(e) {
            // turn missing braces back
            $(e).attr('value', '[' + $(e).val() + ']');
            self.list();
        };

        this.getCountries = getCountries($http);
        this.getLeagues = getLeagues;

        this.setCountry = function() {
            this.leagues_selected = '';
            this.list();
        };

        this.list = function(order_by) {
            var self = this,
            params = $('#ClubListForm').serialize();
            if (order_by) {
                if (self.order_by === order_by) { // same field -> reverse
                    self.order_by_reversed = !self.order_by_reversed;
                } else { // other field -> reset
                    self.order_by_reversed = false;
                }
                self.order_by = order_by;
            }
            params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by +
                '&league=' + self.leagues_selected;
            self.data = {};
            self.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
        };

        this.next = next($http);

        this.getCountries();
        this.list();
    }]);

    app.controller('ClubTeamController', ['$http', '$scope', function($http, $scope) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

        self.TABLE_INDEX = [ // table indexes, null is an empty filler
            // row 1
            [['defender', 0], ['defender', null], ['defender', 1], ['defender', null],
             ['defender', 2], ['defender', null], ['defender', 3],
             ['forward', null], ['forward', 0], ['forward', null],
             ['goalkeeper', 0]],
            // row 2
            [['defender', null], ['defender', 4], ['defender', null],
             ['forward', 1], ['forward', null], ['forward', 2], ['forward', null],
             ['forward', 3], ['forward', null], ['forward', 4],
             ['goalkeeper', null]],
            // row 3
            [['defender', 5], ['defender', null], ['defender', 6],
             ['forward', null], ['forward', 5], ['forward', null], ['forward', 6],
             ['forward', null], ['forward', 7], ['forward', null],
             ['goalkeeper', 1]],
            // row 4
            [['defender', null], ['defender', 7], ['defender', null],
             ['forward', 8], ['forward', null], ['forward', 9], ['forward', null],
             ['forward', 10], ['forward', null], ['forward', 11],
             ['goalkeeper', null]],
            // row 5
            [['defender', 8], ['defender', null], ['defender', 9],
             ['trainer', null], ['trainer', 0], ['trainer', null], ['trainer', 1],
             ['trainer', null], ['trainer', 2], ['trainer', null],
             ['goalkeeper', 2]],
            // row 6
            [['defender', null], ['defender', 10], ['defender', null],
             ['trainer', 3], ['trainer', null], ['trainer', 4], ['trainer', null],
             ['trainer', 5], ['trainer', null], ['trainer', 6],
             ['goalkeeper', null]],
        ];

        self.COMPARE_TABLE_INDEX = [ // table indexes, null is an empty filler
            // row 1
            [['club', 0], ['club', null], ['club', 1], ['club', null],
             ['club', 2], ['club', null], ['club', 3], ['club', null],
             ['club', 4], ['club', null], ['club', 5]],
            // row 1
            [['club', null], ['club', 6], ['club', null], ['club', 7],
             ['club', null], ['club', 8], ['club', null], ['club', 9],
             ['club', null], ['club', 10],  ['club', null]],
            // row 3
            [['club', 11], ['club', null], ['club', 12], ['club', null],
             ['club', 13], ['club', null], ['club', 14], ['club', null],
             ['club', 15], ['club', null], ['club', 16]],
            // row 4
            [['club', null], ['club', 17], ['club', null], ['club', 18],
             ['club', null], ['club', 19], ['club', null], ['club', 20],
             ['club', null], ['club', 21],  ['club', null]],
            // row 5
            [['club', 22], ['club', null], ['club', 23], ['club', null],
             ['club', 24], ['club', null], ['club', 25], ['club', null],
             ['club', 26], ['club', null], ['club', 27]],
            // row 6
            [['club', null], ['club', 28], ['club', null], ['club', 29],
             ['club', null], ['club', 30], ['club', null], ['club', 31],
             ['club', null], ['club', 32],  ['club', null]]
        ];

        self.current_season = {};
        self.previous_seasons = {
            'seasons': []
        };

        $scope.setSeason = function(e) {
            self.list(self.compare);
        }

        self.getPerson = function(season, cell) {
            if (season.table && cell && Array.isArray(cell)) {
                row = season.table[cell[0]];
                if (row) {
                    return season.table[cell[0]][cell[1]];
                }
            }
        }

        self.isVisible = function(season, cell) {
            var person = this.getPerson(season, cell);
            switch (self.status) {
                default:
                    return true;
                case 'joined':
                    return person.is_joined;
                case 'left':
                    return person.is_left;
                case 'legionnaire':
                    return person.is_legionnaire;
            }
        };

        self.getTable = function(data) {
            return {
                'goalkeeper': data.goalkeeper_players,
                'defender': data.defender_players,
                'forward': data.offender_players,
                'trainer': data.coaches
            }
        }

        self.list = function(callback) {
            var params = $('#ClubTeamForm').serialize();
            self.current_season = {};
            self.previous_seasons = {
                'seasons': []
            };
            self.current_season.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                self.current_season.data = data;
                self.current_season.table = self.getTable(data);
                self.current_season.loader = false;
                if (typeof callback === 'function') {
                    callback();
                }
            });
        };

        this.compare = function() {
            var url = $('#ClubTeamCompareLink').attr('href'),
            params, i;
            if (self.previous_seasons.seasons.length) {
                i = self.previous_seasons.seasons.length - 1;
                params = 'season=' + self.previous_seasons.seasons[i].data.prev_season.pk;
            } else {
                params = 'season=' + self.current_season.data.season.pk;
            }
            self.previous_seasons.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                var season = {};
                season.data = data;
                season.league = 'khl';
                season.table = {
                    'club': data.clubs
                };
                self.previous_seasons.seasons.push(season);
                self.previous_seasons.loader = false;
            });
        };

        this.isLastSeason = function() {
            if (self.previous_seasons.seasons.length) {
                i = self.previous_seasons.seasons.length - 1;
                return self.previous_seasons.seasons[i].data.prev_season === null;
            }
        };

        this.list(this.compare);
    }]);

    app.controller('MetricsPlayersController', ['$http', '$scope', function($http, $scope) {
        var self = this,
        url = $('#MetricsPlayersForm').attr('action');
        self.data = {};

        this.search = function() {
            var self = this,
            params = $('#MetricsPlayersForm').serialize();
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
            });
        };
        this.search();
    }]);

    app.controller('MetricsCompareController', ['$http', '$scope', function($http, $scope) {
        this.graph_type = 'linear';
        this.data = {};

        this.setGraphType = function(type) {
            this.graph_type = type;
        };
    }]);

})();
