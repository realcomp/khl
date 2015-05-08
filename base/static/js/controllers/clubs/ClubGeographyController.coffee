angular.module('Sportomatics').controller 'ClubGeographyController', ($http, MapService) ->
    clubTeamApi = document.getElementById("club-team-api").value
    loader = $('.loader')
    loader.addClass('active')
    $http.get(clubTeamApi + '?season=19')
        .success (data) ->
            if MapService.isRendered() is true then MapService.remove()
            MapService.createClubsMap(data.all_players, 'players').then(() ->
                loader.removeClass('active')
            )
            #loader.removeClass('active')
    return
