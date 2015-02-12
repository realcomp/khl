angular.module('Sportomatics')
.controller('ClubListController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#ClubListForm').attr('action');
    this.data = {};
    this.order_by = '%s_title';
    this.order_by_reversed = false;
    this.loader = false;
    this.countries = {};
    this.countries_selected = [];
    this.leagues_selected = '';

    $scope.setSeason = function(e) {
        // turn missing braces back
        $(e).attr('value', '[' + $(e).val() + ']');
        self.list();
    };

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

    this.setCountry = function() {
        this.leagues_selected = '';
        this.list();
    };

    this.list = function(order_by, all) {
        var self = this,
            params = $('#ClubListForm').serialize();
        if (order_by) {
            if (self.order_by === order_by) { // same field -> reverse
                self.order_by_reversed = !self.order_by_reversed;
            } else { // other field -> reset
                self.order_by_reversed = false;
            }
            self.order_by = order_by;
        }
        if(self.leagues_selected === '' && !all) self.leagues_selected = 1; // to avoid waiting for getCountries league set
        params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by +
        '&league=' + self.leagues_selected;
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.next = next($http);
    this.getCountries();
    this.list();

}]);