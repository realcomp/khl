angular.module('Sportomatics').controller('ClubCalendarController', [
    '$scope', '$http', '$location',
    ($scope, $http, $location) ->
        $scope.data = {}
        $scope.params = $location.search()

        $scope.setType = (type) ->
            $location.search('type', type or null)
            $scope.params = $location.search()
            return

        if $scope.params.season
            $('[name="season"]').attr('value', $scope.params.season)

        $scope.setSeason = (e) ->
            $location.search('season', $(e).val())
            $scope.params = $location.search() # don't work
            $scope.list()
            return

        $scope.list = () ->
            params = ''
            $scope.data = {};
            $scope.loaded = false;
            $http.get($scope.url + '?' + params
            ).success((data) ->
                $scope.data = data
                $scope.loaded = true
            )
            return

        return
])
