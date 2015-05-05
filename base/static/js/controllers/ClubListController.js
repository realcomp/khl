angular.module('Sportomatics')
.controller('ClubListController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'MapService',
    function($http, $scope, $location, PlayersSearchService, MapService) {
    var url = $('#ClubListForm').attr('action');
    this.map = true;

    $scope.$location = $location;
    $scope.PlayersSearchService = PlayersSearchService;

    $scope.countries = {};
    $scope.sparams = {};

    $scope.params = $location.search();
    $scope.params.league = '';

    // if ($scope.params.season) {
    //     $('[name="season"]').attr('value', $scope.params.season);
    // }

    $scope.setSeason = function(season) {
        $location.search('season', season);
        $location.search('league', '');
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
        if (!$scope.isCountryActive(country)) {
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

    $scope.isCountryActive = function(country) {
        if ($scope.params.country) {
            return $scope.params.country == country;
        } else {
            return country == 1;
        }
    };

    $scope.isLeagueActive = function(league) {
        if ($scope.data && $scope.data.league) {
            if ($scope.data.league.pk) { // selected league
                return $scope.data.league.pk === league;
            } else { // all leagues
                return league === null;
            }
        } else {
            return false;
        }
    };

    $scope.list = function(all) {
        var params = ''; //$('#ClubListForm').serialize();

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

        if ($scope.params.season || $scope.season) {
            params += '&season=' + ($scope.params.season || $scope.season);
        }
        if ($scope.params.league !== undefined) {
            params += '&league=' + ($scope.params.league || '');
        }
        params += '&country=' + ($scope.params.country || 1);

        $scope.params = $location.search();
        $scope.data = {};
        $scope.loaded = false;
        $http.get(url + '?' + params
        ).success(function(data) {
            $scope.leagues = data.leagues;
            $scope.data = data;
            $scope.clubs = data.results;
            $scope.loaded = true;
        }).then(function(){
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap($scope.clubs, 'clubs');
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
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap($scope.clubs, 'clubs');
        });
    };

    PlayersSearchService.loadCountries($scope, $location, function(){});

    $scope.list();
}]);
