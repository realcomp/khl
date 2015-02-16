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
    this.leagues_selected = 1;

    $scope.setSeason = function(e) {
        // turn missing braces back
        $(e).attr('value', '[' + $(e).val() + ']');
        self.list();
    };

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

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
        // if(self.leagues_selected === null && !all) self.leagues_selected = 1; // to avoid waiting for getCountries league set
        params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
        if (self.leagues_selected) {
            params += '&league=' + self.leagues_selected;
        }
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.setCountry = function(country) {
        if (this.countries_selected[0] != country) {
            this.countries_selected = [country];
            this.leagues_selected = null;
            this.list();
        }
    };

    this.setLeague = function(league) {
        if (self.leagues_selected != league) {
            self.leagues_selected = league;
            self.list();
        }
    };

    this.next = next($http);
    this.getCountries();
    this.list();

}]);
