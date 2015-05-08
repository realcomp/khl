angular.module('Sportomatics').controller('ClubGeographyController', function($http, MapService) {
  var clubTeamApi, loader;
  clubTeamApi = document.getElementById("club-team-api").value;
  loader = $('.loader');
  loader.addClass('active');
  $http.get(clubTeamApi + '?season=19').success(function(data) {
    if (MapService.isRendered() === true) {
      MapService.remove();
    }
    return MapService.createClubsMap(data.all_players, 'players').then(function() {
      return loader.removeClass('active');
    });
  });
});
