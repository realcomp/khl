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
        var url = $('#PlayersSearchForm').attr('action');
        this.data = {};
        this.order_by = '%s_fio';
        this.order_by_reversed = false;
        this.loader = false;

        $scope.moreClubs = function(e) {
            $(e).closest('td').toggleClass('show-more-clubs')
        };

        $scope.lineCheck = function(e) {
            var isAll = $(e).attr('value') === '[0,1,2,3]',
            uncheck = function() {
                if ((isAll && $(this).attr('value') !== '[0,1,2,3]') ||
                    (!isAll && $(this).attr('value') === '[0,1,2,3]')) {
                    $(this).attr('checked', false);
                }
            };
            if ($(e).is(':checked')) {
                $('input[name="line"]').each(uncheck);
            }
        }

        $scope.citizenshipCheck = function(e) {
            var isAll = $(e).attr('name') === 'citizenship' && $(e).attr('value') === '',
            uncheck = function() {
                if ((isAll && $(this).attr('value') !== '') ||
                    (!isAll && $(this).attr('value') === '')) {
                    $(this).attr('checked', false);
                }
            };
            if ($(e).is(':checked')) {
                $('input[name="citizenship"]').each(uncheck);
                $('input[name="citizenship_other_active"]').each(uncheck);
            }
        }

        this.search = function(order_by) {
            var self = this,
            params = $('#PlayersSearchForm').serialize();
            if (order_by) {
                if (self.order_by === order_by) { // same field -> reverse
                    self.order_by_reversed = !self.order_by_reversed;
                } else { // other field -> reset
                    self.order_by_reversed = false;
                }
                self.order_by = order_by;
            }
            params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
            self.data = {};
            self.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
        };

        this.next = next($http);

        this.search();
    }]);

    app.controller('ClubListController', ['$http', function($http) {
        var self = this,
        url = $('#ClubListForm').attr('action');
        this.data = {};
        this.order_by = '%s_title';
        this.order_by_reversed = false;
        this.loader = false;

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
            params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
            self.data = {};
            self.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
        };

        this.next = next($http);

        this.list();
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
