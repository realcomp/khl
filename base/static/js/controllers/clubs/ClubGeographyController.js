angular.module('Sportomatics').controller('ClubGeographyController', function($http, MapService) {
  var clubTeamApi;
  clubTeamApi = document.getElementById("club-team-api").value;
  $http.get(clubTeamApi + '?season=19').success(function(data) {
    if (MapService.isRendered() === true) {
      MapService.remove();
    }
    return MapService.createClubsMap(data.all_players, 'players');
  });
});
