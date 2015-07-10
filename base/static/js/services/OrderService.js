angular.module('Sportomatics').service('OrderService', function() {
  this.setOrderBy = function($scope, order_by) {
    var isDefault, isSame;
    if ($scope.loaded) {
      isDefault = !$scope.params.order_by && !order_by;
      isSame = $scope.params.order_by === order_by;
      if (isSame || isDefault) {
        if ($scope.params.reversed) {
          $scope.$location.search('reversed', null);
        } else {
          $scope.$location.search('reversed', true);
        }
      } else {
        $scope.$location.search('reversed', null);
        $scope.$location.search('order_by', order_by || null);
      }
      $scope.params = $scope.$location.search();
    }
  };
});
