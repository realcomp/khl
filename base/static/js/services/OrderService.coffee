angular.module('Sportomatics').service('OrderService', () ->
    @setOrderBy = ($scope, order_by) ->
        if $scope.loaded
            isDefault = not $scope.params.order_by and not order_by
            isSame = $scope.params.order_by == order_by
            if isSame or isDefault # same field -> reverse
                if $scope.params.reversed
                    $scope.$location.search('reversed', null)
                else
                    $scope.$location.search('reversed', true)
            else # other field -> reset
                $scope.$location.search('reversed', null)
                $scope.$location.search('order_by', order_by or null)
            $scope.params = $scope.$location.search()
            return

    return
)
