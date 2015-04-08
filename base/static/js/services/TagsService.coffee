angular.module('Sportomatics').service('tags', ($http, $q, $filter) ->
    @loadCountries = (url, query) ->
        return $http.get(url + '?s=' + query)

    @loadClubs = (url, query) ->
        return $http.get(url + '?s=' + query)

    return
)
