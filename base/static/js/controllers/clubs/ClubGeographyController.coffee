angular.module('Sportomatics').controller 'ClubGeographyController', ($http, MapService) ->
    clubTeamApi = document.getElementById("club-team-api").value
    $http.get(clubTeamApi + '?season=19')
        .success (data) ->
            if MapService.isRendered() is true then MapService.remove()
            MapService.createClubsMap(data.all_players, 'players')
    return
