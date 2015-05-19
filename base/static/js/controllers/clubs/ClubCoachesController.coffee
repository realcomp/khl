angular.module('Sportomatics').controller 'ClubCoachesController', ($scope, $http, $location, SeasonsService) ->
    url = $('#club-coaches-api').val()

    $scope.$location = $location
    $scope.SeasonsService = SeasonsService

    $scope.params = $location.search()

    $scope.setSeason = (season) ->
        $location.search('season', season)
        $scope.params = $location.search()
        $scope.list()
        return

    $scope.list = () ->
        if $scope.params.season
            season = $scope.params.season
        else
            season = SeasonsService.getDefaultSeason()
        params = 'season=' + season

        $scope.data = []
        $scope.loaded = false

        $http.get(url + '?' + params
        ).success((data) ->
            $scope.data = [data]
            $scope.loaded = true
            return
        )
        return

    $scope.back = () ->
        params = 'season=' + $scope.data[$scope.data.length - 1].previous_season.pk

        $scope.loaded = false

        $http.get(url + '?' + params
        ).success((data) ->
            $scope.data.push(data)
            $scope.loaded = true
            return
        )
        return

    $scope.list()

    # $('.b-tabs-content').visibility({
    $('#footer').visibility({
        'once': false,
        'observeChanges': true,
        'onBottomVisible': () ->
            if $scope.data and $scope.data[$scope.data.length - 1].previous_season.pk
                $scope.back()
    })

    return
