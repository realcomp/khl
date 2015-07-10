angular.module('Sportomatics').controller('ProfileController', [
    '$http', '$scope', 'tags',
    ($http, $scope, tags) ->
        $scope.tags = tags

        $scope.user = {}
        $scope.config = {
            'headers': {
                'X-CSRFToken': null,
            },
        }

        $scope.loadCountries = (query) ->
            return $scope.tags.loadCountries($scope.countriesURL, query)

        $scope.loadClubs = (query) ->
            return $scope.tags.loadClubs($scope.clubsURL, query)

        $scope.setAvatar = (files, csrf_token) ->
            fd = new FormData()
            fd.append('avatar', files[0])
            config = {
                'headers': {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': undefined,
                },
                'withCredentials': true,
                'transformRequest': angular.identity,
            }
            $http.patch(this.profileURL, fd, config
            ).success((data) ->
                $('#id_avatar').attr('src', data.avatar)
                $('.user-avatar-hex2').css(
                    'background-image', 'url(' + data.avatar + ')')
                return
            ).error((data) ->
                # TODO: handle image upload errors
                return
            )
            return

        $scope.save = () ->
            $scope.user.clubs = (club.pk for club in $scope.clubs)
            $scope.user.countries = (country.pk for country in $scope.countries)
            $http.patch($scope.profileURL, $scope.user, $scope.config
            ).success((data) ->
                $scope.user = data
                return
            )
            return

        $scope.confirmEmail = () ->
            $http.post($scope.emailConfirmationURL, {}, $scope.config
            ).success((data) ->
                # TODO: notify
                return
            )
            return

        return
])
