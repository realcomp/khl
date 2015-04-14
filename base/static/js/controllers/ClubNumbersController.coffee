angular.module('Sportomatics').controller('ClubNumbersController', [
    '$http', '$scope', '$location',
    ($http, $scope, $location) ->
        $scope.$location = $location

        $scope.data = {}
        $scope.params = $location.search()

        $scope.list = () ->
            $http.get($scope.url
            ).success((data) ->
                $scope.data = data
                return
            )
            return

        return

        $scope.list()
])
