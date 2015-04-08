angular.module('Sportomatics').service('tags', function($http, $q, $filter) {
  this.loadCountries = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
  this.loadClubs = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
});
