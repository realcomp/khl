angular.module('Sportomatics')
.controller('ProfileController', ['$http', '$scope', function($http, $scope) {
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
}])