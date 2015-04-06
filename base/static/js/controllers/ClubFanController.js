angular.module('Sportomatics').controller('ClubFanController', function($scope, MapService) {
  $scope.loaded = true;
  console.log($scope.loaded);
  if (MapService.isRendered()) {
    MapService.remove();
  }
  MapService.createClubsMap([], 'fans');
});
