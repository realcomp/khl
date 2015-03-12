angular.module('Sportomatics').service('ProfileService', function($http, $cookies) {
    this.setAvatar = function(files) {
        var url = '/en/accounts/api/profile/',
        fd = new FormData(),
        config = {
            'headers': {
                'X-CSRFToken': $cookies.csrftoken,
                'Content-Type': undefined
            },
            'withCredentials': true,
            'transformRequest': angular.identity
        };
        fd.append('avatar', files[0]);
        $http.patch(url, fd, config).success(function(data) {
            $('.user-avatar-hex2').css(
                'background-image', 'url(' + data.avatar + ')');
        }).error(function(data) {
            // TODO: handle image upload errors
        });
    };
});
