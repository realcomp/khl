angular.module('Sportomatics').controller('ProfileController', [
  '$http', '$scope', function($http, $scope) {
    $scope.user = {};
    $scope.csrf_token = null;
    $scope.setAvatar = function(files, csrf_token) {
      var config, fd;
      fd = new FormData();
      fd.append('avatar', files[0]);
      config = {
        'headers': {
          'X-CSRFToken': csrf_token,
          'Content-Type': void 0
        },
        'withCredentials': true,
        'transformRequest': angular.identity
      };
      $http.patch(this.profileURL, fd, config).success(function(data) {
        $('#id_avatar').attr('src', data.avatar);
        $('.user-avatar-hex2').css('background-image', 'url(' + data.avatar + ')');
      }).error(function(data) {});
    };
    $scope.save = function() {
      var config, data;
      data = {
        'fio': $scope.user.fio,
        'email': $scope.user.email
      };
      config = {
        'headers': {
          'X-CSRFToken': $scope.csrf_token
        }
      };
      $http.patch($scope.profileURL, data, config).success(function(data) {
        $scope.user = data;
      });
    };
    $scope.confirmEmail = function() {
      var config;
      config = {
        'headers': {
          'X-CSRFToken': $scope.csrf_token
        }
      };
      $http.post($scope.emailConfirmationURL, {}, config).success(function(data) {});
    };
  }
]);
