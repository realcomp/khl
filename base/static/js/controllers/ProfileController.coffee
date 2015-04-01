angular.module('Sportomatics').controller('ProfileController', [
    '$http', '$scope',
    ($http, $scope) ->

        $scope.user = {}
        $scope.config = {
            'headers': {
                'X-CSRFToken': null,
            },
        }

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
            data = {
                'fio': $scope.user.fio,
                'email': $scope.user.email
            }
            $http.patch($scope.profileURL, data, $scope.config
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
