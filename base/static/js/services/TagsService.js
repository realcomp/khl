angular.module('Sportomatics').service('tags', function($q, $filter) {
    var clubs = [
        { "pk": 1, "title": "Динамо Мск" },
        { "pk": 2, "title": "СКА СПБ" },
        { "pk": 3, "title": "Трактор (Челябинск)" },
        { "pk": 4, "title": "Рубин (Краснодар)" },
        { "pk": 5, "title": "Спартак Мск" },
        { "pk": 6, "title": "Терек" },
        { "pk": 7, "title": "Цверна Звезда" }
    ];
    var countries = [
        { "pk": 1, "title" : "Россия" },
        { "pk": 2, "title" : "США" },
        { "pk": 3, "title" : "Канада" },
        { "pk": 4, "title" : "Германия" }
    ];
    this.getClubs = function (sport) {
        //TODO: get clubs by selected sport in selected countries
    };
    this.loadCountries = function(query) {
        var deferred = $q.defer();
        deferred.resolve($filter('filter')(countries, { title: query}));
        return deferred.promise;
    };
    this.loadClubs = function(query) {
        var deferred = $q.defer();
        deferred.resolve($filter('filter')(clubs, { title: query}));
        return deferred.promise;
    };
});
