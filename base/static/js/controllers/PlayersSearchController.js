angular.module('Sportomatics')
.controller('PlayersSearchController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#PlayersSearchForm').attr('action'),
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

    this.data = {};
    this.order_by = '[%22%s_lastname%22,%22%s_name%22]';
    this.order_by_reversed = false;
    this.ratedBy = 'seasons';
    this.loader = false;
    this.countries_selected = [];
    this.leagues_selected = [];

    $scope.moreClubs = function(e) {
        $(e).closest('td').toggleClass('show-more-clubs')
    };

    $scope.lineCheck = function(e) {
        var defaultValue = '[0,1,2,3]',
            isDefault;
        isDefault = $(e).attr('value') === defaultValue;
        if ($(e).is(':checked')) {
            $('input[name="line"]').each(getUnchecker(isDefault, defaultValue));
        }
    };

    $scope.citizenshipCheck = function(e) {
        var isDefault = $(e).attr('name') === 'citizenship' && $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="citizenship"]').each(getUnchecker(isDefault, ''));
            $('input[name="citizenship_other_active"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.contractCheck = function(e) {
        var isDefault = $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="contract"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.showPopup = function(e) {
        var block = $(e).closest('.player-avatar-block');
        block.children('.player-avatar-block-popup').show();
    };

    this.getCountries = getCountries($http);
    this.getLeagues = getLeagues;

    this.search = function(order_by) {
        var params = $('#PlayersSearchForm').serialize();
        if (order_by) {
            if (self.order_by === order_by) { // same field -> reverse
                self.order_by_reversed = !self.order_by_reversed;
            } else { // other field -> reset
                self.order_by_reversed = false;
            }
            self.order_by = order_by;
        }
        params = params + '&order_by=' + (self.order_by_reversed ? '-' : '') + self.order_by;
        $.each(self.leagues_selected, function() {
            params += '&league=' + this;
        });
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
            });
    };

    this.setRatedBy = function(ratedBy) {
        if (!this.loader) {
            this.ratedBy = ratedBy;
            this.search();
        }
    };

    this.next = next($http);

    this.getCountries(this.search);
}])
