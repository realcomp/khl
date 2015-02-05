;(function() {
'use strict';
angular.module('Sportomatics', [])

var next = function($http) {
    return function(isAll) {
        var self = this,
            url = self.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + self.data.count);
        }
        self.loader = true;
        $http.get(url)
            .success(function(data) {
                if (isAll) {
                    self.data = data;
                } else {
                    self.data.next = data.next;
                    self.data.results = self.data.results.concat(data.results);
                }
                self.loader = false;
            });
    };
}

var getCountries = function($http) {
    return function(callback) {
        var self = this,
            url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
                    self.countries = data;
                    if (self.countries.length) { // has countries
                        if (Array.isArray(self.countries_selected) &&
                            self.countries_selected.length === 0) { // array is expected
                            self.countries_selected = [String(self.countries[0].pk)];
                        } else {
                            self.countries_selected = self.countries[0].pk;
                        }
                        if (self.countries[0].league_set.length) { // has leagues
                            if (Array.isArray(self.leagues_selected) &&
                                self.leagues_selected.length === 0) { // array is expected
                                self.leagues_selected = [String(self.countries[0].league_set[0].pk)];
                            } else {
                                self.leagues_selected = self.countries[0].league_set[0].pk;
                            }
                        }
                    }
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
        }
    };
}

var getLeagues = function(countries, countries_selected) {
    var result = [];
    $.each(countries_selected, function() {
        var pk = this;
        $.each(countries, function() {
            if (this.pk == pk) {
                result = result.concat(this.league_set);
            }
        });
    });
    return result;
}
Date.prototype.yyyymmdd = function(delimiter){
    if(delimiter == null) delimiter = '';
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return yyyy + delimiter + (mm[1]?mm:"0"+mm[0]) + delimiter + (dd[1]?dd:"0"+dd[0]);
}
Date.prototype.getWeekNumber = function(){
    var d = new Date(+this);
    d.setHours(0,0,0);
    d.setDate(d.getDate()+4-(d.getDay()||7));
    return Math.ceil((((d-new Date(d.getFullYear(),0,1))/8.64e7)+1)/7);
}
function getDateOfWeek(w, y) {
    var d = (1 + (w - 1) * 7); // 1st of January + 7 days for each week

    return new Date(y, 0, d);
}
})();
;(function() {
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

    this.list = function(order_by) {
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
}])
})();
;(function() {
angular.module('Sportomatics')
.controller('MetricsCompareController', ['$http', '$scope', function($http, $scope) {
    this.graph_type = 'linear';
    this.data = {};
    this.setGraphType = function(type) {
        this.graph_type = type;
    };
}])
})();
;(function() {
angular.module('Sportomatics')
.controller('MetricsPlayersController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#MetricsPlayersForm').attr('action');
    self.data = {};

    this.search = function() {
        var self = this,
            params = $('#MetricsPlayersForm').serialize();
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
            });
    };
    this.search();
}])
})();
;(function() {
angular.module('Sportomatics')
.controller('PlayerCardIndicatorsController', ['$http', '$scope', function($http, $scope) {
    var self = this,
        url = $('#IndicatorsLink').attr('href');

    this.indicators_type = 'graph';
    this.field = 'goals';
    this.club = null;
    this.coach = null;
    this.groupBy = 'month';
    this.data = {};
    this.graphData = {};
    function ObjectToGenerate() {
        return {
            bindto: '#chart',
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: function (value) {
                            var monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                                "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
                            if (self.groupBy === 'month') return monthNames[value.getMonth()] + ' ' + value.getDate() + ', ' + value.getFullYear();
                            if (self.groupBy === 'weeks') return value.getWeekNumber() + ' week, ' + value.getFullYear();
                            if (self.groupBy === 'season') return 'Сезон ' + (value.getFullYear()-1) + '-' + value.getFullYear();
                            return value;
                        }
                    }
                },
                y: {
                    min: -2,
                    label: self.field
                }
            },
            data: {
                xs: {},
                columns: [],
                colors: {

                },
                type: 'line'
            },
            point: {
                show: false
            },
            size: {
                width: 900
            },
            transition: {
            }, zoom: {
                //enabled: true,
                rescale: true
            },
            grid: {
                x: {
                    show: true
                },
                y: {
                    show: true
                }
            }

        }
    }
    this.createC3ArrayAndData = function(array, number, field, name){
        var resultArray = _.map(array, function(e){
                if(e['date'] == null){
                    console.log(e['season']['label'].substr(12,4));
                    console.log(new Date(e['season']['label'].substr(12, 4)).yyyymmdd('-'))
                    return new Date(e['season']['label'].substr(12,4)).yyyymmdd('-');
                }
                return new Date(e['date']).yyyymmdd('-');}
        ).sort(function(a,b){
                return new Date(a.substr(0, 4), a.substr(5, 2)-1, a.substr(8, 2)) - new Date(b.substr(0, 4),b.substr(5, 2)-1, b.substr(8, 2));
            });
        resultArray.unshift('x'+number);
        var resultArrayData = array.map(function(e){
            /*if( Object.prototype.toString.call( $scope.fieldMapping[field] ) === '[object Array]' ) {
             var sum = 0;
             _.each($scope.fieldMapping[field], function(fieldEntry){
             sum += e[fieldEntry];
             })
             return sum;
             } else*/ return e[field]; // wait for multiple players comparison
        });
        resultArrayData.unshift(name);
        return {
            array: resultArray,
            data: resultArrayData
        }
    }
    this.createFieldData = function(field, array){
        var result = [];
        var i = 0;
        //TODO: make this method accept multiple players
        var object = self.createC3ArrayAndData(array, i, field, 'Player ' + '1');
        result.push(object);
        return result;
    };

    this.setIndicatorsType = function(type) {
        this.indicators_type = type;
    };

    this.setField = function(field) {
        this.field = field;
        this.list();
    }

    this.setClub = function(club) {
        this.club = club;
        this.list();
    }

    this.setCoach = function(coach) {
        this.coach = coach;
        this.list();
    }
    this.setGraphResults = function(results) {

    }
    $scope.setGroupBy = function(groupby){
        console.log(groupby)
        self.groupBy = groupby;
        self.list();
    };
    var chart = null;
    $scope.addChart = function () {
        var params = 'group_by=season';
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                var fieldData = self.createFieldData(self.field, self.data.results);
                var objectToGenerate = new ObjectToGenerate();
                _.each(fieldData, function (c3ADObject) {
                    objectToGenerate.data.xs[c3ADObject.data[0]] = c3ADObject.array[0];
                    objectToGenerate.data.colors[c3ADObject.data[0]] = '#58cb73';
                    objectToGenerate.data.columns.push(c3ADObject.array);
                    objectToGenerate.data.columns.push(c3ADObject.data);
                    chart.flow({
                        columns: objectToGenerate.data.columns,
                        'xs.x1' : c3ADObject.array[0]
                    })
                });

            })
    };

    this.list = function(order_by) {
        var params = 'group_by=' + self.groupBy;
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        self.data = {};
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data) {
                self.data = data;
                self.loader = false;
                var fieldData = self.createFieldData(self.field, self.data.results);
                var objectToGenerate = new ObjectToGenerate();
                _.each(fieldData, function(c3ADObject){
                    objectToGenerate.data.xs[c3ADObject.data[0]] = c3ADObject.array[0];
                    objectToGenerate.data.colors[c3ADObject.data[0]] = '#58cb73';
                    objectToGenerate.data.columns.push(c3ADObject.array);
                    objectToGenerate.data.columns.push(c3ADObject.data);
                });
                chart = c3.generate(objectToGenerate);
            });
    };

    this.list();
}])
})();
;(function() {
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

var next = function($http) {
    return function(isAll) {
        var self = this,
            url = self.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + self.data.count);
        }
        self.loader = true;
        $http.get(url)
            .success(function(data) {
                if (isAll) {
                    self.data = data;
                } else {
                    self.data.next = data.next;
                    self.data.results = self.data.results.concat(data.results);
                }
                self.loader = false;
            });
    };
}

var getCountries = function($http) {
    return function(callback) {
        var self = this,
            url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url)
                .success(function(data) {
                    self.countries = data;
                    if (self.countries.length) { // has countries
                        if (Array.isArray(self.countries_selected) &&
                            self.countries_selected.length === 0) { // array is expected
                            self.countries_selected = [String(self.countries[0].pk)];
                        } else {
                            self.countries_selected = self.countries[0].pk;
                        }
                        if (self.countries[0].league_set.length) { // has leagues
                            if (Array.isArray(self.leagues_selected) &&
                                self.leagues_selected.length === 0) { // array is expected
                                self.leagues_selected = [String(self.countries[0].league_set[0].pk)];
                            } else {
                                self.leagues_selected = self.countries[0].league_set[0].pk;
                            }
                        }
                    }
                    if (typeof callback === 'function') {
                        callback();
                    }
                });
        }
    };
}

var getLeagues = function(countries, countries_selected) {
    var result = [];
    $.each(countries_selected, function() {
        var pk = this;
        $.each(countries, function() {
            if (this.pk == pk) {
                result = result.concat(this.league_set);
            }
        });
    });
    return result;
}

})();
;(function() {
angular.module('Sportomatics')
.controller('ProfileController', ['$http', '$scope', function($http, $scope) {
    var self = this;

    self.user = {};
    self.csrf_token = null;

    $http.get('/en/accounts/api/profile/')
        .success(function(data) {
            self.user = data;
        });

    $scope.setAvatar = function(files, csrf_token) {
        var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': csrf_token,
                    'Content-Type': undefined
                },
                'withCredentials': true,
                'transformRequest': angular.identity
            },
            fd = new FormData();
        fd.append('avatar', files[0]);
        $http.patch('/en/accounts/api/profile/', fd, config)
            .success(function(data) {
                $('#id_avatar').attr('src', data.avatar);
                $('.user-avatar-hex2').css(
                    'background-image', 'url(' + data.avatar + ')');
            })
            .error(function(data) {
                // TODO: handle image upload errors
            });
    };

    this.save = function() {
        var self = this,
            config = {
                'headers': {
                    'X-CSRFToken': this.csrf_token
                }
            };
        // TODO: replace url
        $http.patch('/en/accounts/api/profile/', {
            'fio': self.user.fio,
            'email': self.user.email
        }, config)
            .success(function(data) {
                self.user = data;
            });
    };
}])
})();