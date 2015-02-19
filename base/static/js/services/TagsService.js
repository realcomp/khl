angular.module('Sportomatics').service('tags', function($q, $filter) {
    var clubs = [
        { "text": "Динамо Мск" },
        { "text": "СКА СПБ" },
        { "text": "Трактор (Челябинск)" },
        { "text": "Рубин (Краснодар)" },
        { "text": "Спартак Мск" },
        { "text": "Терек" },
        { "text": "Цверна Звезда" }
    ];
    var countries = [
        { "text" : "Россия" },
        { "text" : "США" },
        { "text" : "Канада" },
        { "text" : "Германия" }
    ];
    this.getClubs = function (sport) {
        //TODO: get clubs by selected sport in selected countries
    };

    this.loadCountries = function(query) {
        var deferred = $q.defer();
        deferred.resolve($filter('filter')(countries, { text: query}));
        return deferred.promise;
    };
    this.loadClubs = function(query) {
        var deferred = $q.defer();
            deferred.resolve($filter('filter')(clubs, { text: query}));
            return deferred.promise;
    };
});