(function() {
    var app = angular.module('Sportomatics', []);

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
        url = $('#PlayersSearchForm').attr('action');
        self.data = {};

        $scope.moreClubs = function(e) {
            $(e).closest('td').toggleClass('show-more-clubs')
        };

        this.search = function() {
            var self = this,
            params = $('#PlayersSearchForm').serialize();
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
            });
        };
        this.search();
    }]);

    app.controller('ClubListController', ['$http', function($http) {
        var self = this,
        url = $('#ClubListForm').attr('action');
        self.data = {};

        this.list = function() {
            var self = this,
            params = $('#ClubListForm').serialize();
            $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
            });
        };
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
