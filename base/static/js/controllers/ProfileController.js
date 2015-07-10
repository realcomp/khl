angular.module('Sportomatics').controller('ProfileController', [
  '$http', '$scope', 'tags', function($http, $scope, tags) {
    $scope.tags = tags;
    $scope.user = {};
    $scope.config = {
      'headers': {
        'X-CSRFToken': null
      }
    };
    $scope.loadCountries = function(query) {
      return $scope.tags.loadCountries($scope.countriesURL, query);
    };
    $scope.loadClubs = function(query) {
      return $scope.tags.loadClubs($scope.clubsURL, query);
    };
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
      var club, country;
      $scope.user.clubs = (function() {
        var i, len, ref, results;
        ref = $scope.clubs;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          club = ref[i];
          results.push(club.pk);
        }
        return results;
      })();
      $scope.user.countries = (function() {
        var i, len, ref, results;
        ref = $scope.countries;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          country = ref[i];
          results.push(country.pk);
        }
        return results;
      })();
      $http.patch($scope.profileURL, $scope.user, $scope.config).success(function(data) {
        $scope.user = data;
      });
    };
    $scope.confirmEmail = function() {
      $http.post($scope.emailConfirmationURL, {}, $scope.config).success(function(data) {});
    };
  }
]);
