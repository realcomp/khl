(function() {
    var app = angular.module('Sportomatics', []);

    app.controller('UserVersionController', ['$http', function($http) {
        this.user = {};
        this.csrf_token = null;

        this.setVersion = function(version) {
            var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': this.csrf_token
                }
            };
            self.user.version = version;
            // TODO: replace url
            $http.patch(
                '/en/accounts/api/user/version/',
                self.user, config)
            .success(function(data) {
                self.user = data;
            });
        };
    }]);

})();
