angular.module('Sportomatics').controller('ClubTeamCompareController', function($scope) {
  $scope.$watch('selectedClub', function(newval) {
    return console.log(newval);
  });
  $scope.$on('$viewContentLoaded', function() {
    var PlayerIndicatorsController;
    PlayerIndicatorsController = angular.element(document.getElementById('scope')).scope();
    return console.log(PlayerIndicatorsController);
  });
});
