angular.module('Sportomatics')
.controller('ClubListController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'MapService',
    function($http, $scope, $location, PlayersSearchService, MapService) {
    var url = $('#ClubListForm').attr('action');
    this.map = true;

    $scope.$location = $location;
    $scope.PlayersSearchService = PlayersSearchService;

    $scope.countries = {};
    $scope.sparams = {}

    $scope.params = $location.search()

    if ($scope.params.season) {
        $('[name="season"]').attr('value', $scope.params.season);
    }

    $scope.setSeason = function(e) {
        // $(e).attr('value', $(e).val());
        $location.search('season', $(e).val());
        $scope.params = $location.search();
        $scope.list();
    };

    $scope.setOrderBy = function(order_by) {
        if ($scope.loaded) {
            if ($scope.params.order_by === order_by ||
                    (!$scope.params.order_by && !order_by)) { // same field -> reverse
                if ($scope.params.reversed === 'true') {
                    $scope.$location.search('reversed', null);
                } else {
                    $scope.$location.search('reversed', 'true');
                }
            } else { // other field -> reset
                $scope.$location.search('reversed', null);
            }
            $scope.$location.search('order_by', order_by);
            $scope.list($scope);
        }
    };

    $scope.setCountry = function(country) {
        if ($scope.params.country != country) {
            $location.search('country', country);
            $scope.params = $location.search();
            $scope.list();
        }
    };

    $scope.setLeague = function(league) {
        if ($scope.params.league != league) {
            $location.search('league', league);
            $scope.params = $location.search();
            $scope.list();
        }
    };

    $scope.list = function(all) {
        var params = $('#ClubListForm').serialize();

        params += '&order_by=' + ($scope.params.order_by || '%s_title');
        if ($scope.params.reversed) {
            params += '&reversed=true';
        }

        // if ($scope.sparams.leaguesSelected) {
        //     $location.search('league', $scope.sparams.leaguesSelected);
        // } else {
        //     $location.search('league', null);
        // }
        // if ($scope.sparams.contriesSelected) {
        //     $location.search('country', $scope.sparams.countriesSelected);
        // } else {
        //     $location.search('country', null);
        // }

        if ($scope.params.league) {
            params += '&league=' + $scope.params.league;
        }
        if ($scope.params.country) {
            params += '&country=' + $scope.params.country;
        }

        $scope.params = $location.search();
        $scope.data = {};
        $scope.loaded = false;
        $http.get(url + '?' + params)
            .success(function(data) {
                console.log(data)
                $scope.data = data;
                $scope.clubs = data.results;
                $scope.loaded = true;
            }).then(function(){
                if(MapService.isRendered()) MapService.remove();
                MapService.createClubsMap($scope.clubs, 'clubs');
            });
    };

    $scope.next = function(isAll) {
        var url = $scope.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
        }
        $scope.loaded = false;
        $http.get(url).success(function(data) {
            if (isAll) {
                $scope.data = data;
            } else {
                $scope.data.next = data.next;
                $scope.data.results = $scope.data.results.concat(data.results);
                $scope.clubs = $scope.clubs.concat(data.results);
            }
            $scope.loaded = true;
        }).then(function(){
            if(MapService.isRendered()) MapService.remove();
            MapService.createClubsMap($scope.clubs, 'clubs');
        });
    };

    PlayersSearchService.loadCountries($scope, $location, function(){});
}]);
