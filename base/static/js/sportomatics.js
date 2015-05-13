'use strict';
angular.module('Sportomatics', [
    'angucomplete',
    'ngTagsInput',
    'ui.router',
    'ngResource',
    'ngCookies',
    'isteven-multi-select'])
.config(function($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('playersCoaches', {
            url: '/ru/hockey/players',
            templateUrl: ' ',
            controller: function($state){
                alert($state)
            }
        })
})

.directive('ngUpdateHidden', function() {
    return {
        'restrict': 'AE',
        'scope': {},
        'replace': true,
        'require': 'ngModel',
        'link': function($scope, elem, attr, ngModel) {
            $scope.$watch(ngModel, function(nv) {
                elem.val(nv);
            });
            elem.change(function() {
                $scope.$apply(function() {
                    ngModel.$setViewValue(elem.val());
                });
            });
        }
    };
});

/* better fps test
var body = document.body, timer;
window.addEventListener('scroll', function() {
  clearTimeout(timer);
  if(!body.classList.contains('disable-hover')) {
    body.classList.add('disable-hover')
  }
  timer = setTimeout(function(){
    body.classList.remove('disable-hover')
  }, 500);
}, false);
 better fps test */
var ALL_FIELDS = ["count", "goals", "assists", "points", "plus_minus", "penalty_time", "es_goals", "pp_goals", "ev_goals", "overtime_goals", "win_goals", "bullet_goals", "shots", "pis__avg", "shots__avg", "faceoff", "winfaceoff", "winfaceoff_p_avg", "gamingtime__avg", "change_count__avg", "shots_received", "loose_goals", "saves", "saves_p__avg", "sf__avg", "matches_win", "matches_lose", "zero_goals_matches", "bullet_matches", "position"];
var KHL_NEWEST_FIELDS = ['shots', 'pis__avg', 'shots__avg', 'faceoff', 'winfaceoff', 'winfaceoff_p__avg', 'gamingtime__avg', 'change_count__avg'];
var AVERAGE_AVAILABLE_FIELDS = ['goals', 'assists', 'points', 'plus_minus', 'penalty_time'];

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
Array.prototype.getIndexBy = function (name, value) {
    for (var i = 0; i < this.length; i++) {
        if (this[i][name] == value) {
            return i;
        }
    }
}
Date.prototype.yyyymmdd = function(delimiter){
    if(delimiter == null) delimiter = '';
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return yyyy + delimiter + (mm[1]?mm:"0"+mm[0]) + delimiter + (dd[1]?dd:"0"+dd[0]);
};
Date.prototype.yyyymmddFormatted = function(){
    var monthNames = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
        'августа', 'сентября', 'октября', 'ноября', 'декабря'];
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return dd + ' ' + monthNames[mm] + ' ' + yyyy;
}
Date.prototype.yyyymmddHHMMFormatted = function(){
    var monthNames = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
        'августа', 'сентября', 'октября', 'ноября', 'декабря'];
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return dd + ' ' + monthNames[mm] + ' ' + yyyy + ' в ' + this.getHours() + ':' + this.getMinutes();
}
Date.prototype.HHMM = function(){
    return this.getHours() + ':' + this.getMinutes();
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
function contains(array, field, value){
        for(var i = 0; i < array.length; i++) {
            if (array[i][field] === value) {
                return true;
            }
        }
        return false;
    }
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
function getParameterByName(string, name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(string);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
function toSeason(value){
    //TODO заменить
    //14/15
    if(value.indexOf('/') > -1 && value.length === 5){
        value = parseInt(value.substring(2, 5));
        if(value > 20){
            value = '19' + value;
        } else {
            value = '20' + value;
        }

    }
    var seasons = {
        s2002: 1,
        s2003: 2,
        s2001: 3,
        s2004: 4,
        s2000: 5,
        s1999: 6,
        s1998: 7,
        s2005: 8,
        s2006: 9,
        s1997: 10,
        s2007: 11,
        s2008: 12,
        s2009: 13,
        s2010: 14,
        s2011: 15,
        s2012: 16,
        s2013: 17,
        s2014: 18,
        s2015: 19
    }
    return seasons['s'+value];
}
function fromSeason(value){
    var seasons = {
        s1: 2002,
        s2: 2003,
        s3: 2001,
        s4: 2004,
        s5: 2000,
        s6: 1999,
        s7: 1998,
        s8: 2005,
        s9: 2006,
        s10: 1997,
        s11: 2007,
        s12: 2008,
        s13: 2009,
        s14: 2010,
        s15: 2011,
        s16: 2012,
        s17: 2013,
        s18: 2014,
        s19: 2015
    }
    return seasons['s'+value];
}
$.fn.textWidth = function(){
    var html_org = $(this).html();
    var html_calc = '<span>' + html_org + '</span>';
    $(this).html(html_calc);
    var width = $(this).find('span:first').width();
    $(this).html(html_org);
    return width;
};
