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

.factory('AmChartsFactory', function ($q, $rootScope, $document) {
    var deferred = $q.defer();

    AmCharts.ready(function(){
        $rootScope.$apply(deferred.resolve);
    });

    return {
        ready: function () {
            return deferred.promise;
        }
    };
})
.run(function (AmChartsFactory) {});

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
//TODO: make expressions to check if already scrolled (for performance)
/*
$(function() {
    var top = null;
    var topSecondary = null;
    var topThird = null;
    var topPlayer = null;
    var breadcrumbWidth = null;
    var teamNameWidth = null;
    var teamLogoMargin = null;
    var playerNameWidth = null;
    var scrolledAfterPlayer = false;
    var scrolledAfterBreadcrumbs = false;
    var scrolledAfterTeamInfo = false;
    var scrolledAfterGreenMenu = false;
    //jquery elements
    if($('.breadcrumbs').length){
        top = $('.breadcrumbs').offset().top;
        if($('.breadcrumb').length)
        breadcrumbWidth = $('.breadcrumb').first().css('width').substr(0, $('.breadcrumb').first().css('width').length -2);
    }
    if($('.team-info').length){
        topSecondary = $('.team-info').offset().top + 60;
        teamNameWidth = parseInt($('#team-name').css('width').substr(0, $('#team-name').css('width').length-2));
    }
    if($('.page-menu').length){
        topThird = $('.page-menu').offset().top - 40;
    }
    if($('.player-card-block').length){
        topPlayer = $('.breadcrumbs').next().offset().top + 132;
        playerNameWidth = $('#player-card-name').textWidth();
    }
    if(breadcrumbWidth && teamNameWidth){
        teamLogoMargin = (1000 - breadcrumbWidth*2 - (25+teamNameWidth))/2;
    }
    $(window).scroll(function(event) {
        var y = $(window).scrollTop();
        if (top && y >= top) {
            if($('.team-info').length) {
                $('.team-info').css('margin-top', '52px'); // club page
            } else {
                if($('.player-card-block').length){ // players-page
                    if($('.breadcrumbs').length){
                        $('.breadcrumbs').next().css('margin-top', '42px')
                    }
                } else ($('.page-container').css('margin-top', '42px')) // clubs page
            }
            if(!$('.sm-logo').length) $('.breadcrumb').before($("<img class='sm-logo' style='vertical-align: middle; margin-right: 5px; float: left;' src='/static/images/sm_micro.png'>"));
            $('.breadcrumbs').addClass('fixed');
        } else if(top && y < top) {
            $('.breadcrumbs').removeClass('fixed');
            if($('.sm-logo').length) $('.sm-logo').remove();
            if($('.team-info').length) {
                $('.team-info').css('margin-top', '0px');
            } else {
                if($('.player-card-block').length){
                    if($('.breadcrumbs').length){
                        $('.breadcrumbs').next().css('margin-top', '0px')
                    }
                } else ($('.page-container').css('margin-top', '0px'))
            }
        }
        //player card
        if(topPlayer && y >= topPlayer && !scrolledAfterPlayer){
            //console.log('player call ');
            $('.breadcrumb').after($("<div class='inline-block min-photo-container'></div>"));
            $('#player-card-avatar').addClass('clipped-img');
            $('#player-card-avatar').detach().appendTo($('.min-photo-container').css('margin-left', (1000 - 110 - breadcrumbWidth*2 - playerNameWidth)/2 + 'px', 'important'));
            $('.min-photo-container').after($('#player-card-name').addClass('inline-block player-card-name-inner'));
            $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important').css('box-shadow', '0 4px 2px -2px gray','important'));
            $('.page-container').css('margin-top', '68px');
            scrolledAfterPlayer = true;
        } else if (topPlayer && y < topPlayer && scrolledAfterPlayer){
            //console.log('player reverse call ');
            $('#player-card-amplua').before($('#player-card-name').removeClass('inline-block player-card-inner'));
            $('#player-card-desc').before($('#player-card-avatar').removeClass('clipped-img').css('margin-left', '0'));
            $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important').css('box-shadow', '0','important'));
            $('.page-container').css('margin-top', '0px');
            $(".min-photo-container").remove();
            scrolledAfterPlayer = false;
        }
        //team card
        if (topSecondary && y >= topSecondary && !scrolledAfterTeamInfo && !$('#player-card-block').length){
            //console.log('team info call ');
            $('.page-container').css('margin-top', '114px');
            $('.my-team-btn').css('margin-top', '4px');
            $('.breadcrumb').after($('#team-logo')).addClass('inline-block breadcrumb-inner');
            $("#team-logo").after($('#team-name')).addClass('team-logo-inner inline-block').css('margin-left', teamLogoMargin + 'px', 'important');
            $('#team-name').addClass('team-name-inner inline-block');
            $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important').css('box-shadow', '0 4px 2px -2px gray','important'));
            scrolledAfterTeamInfo = true;
        } else if (topSecondary && y < topSecondary && scrolledAfterTeamInfo){
            //console.log('team info reverse call ');
            $('.my-team-btn').after($('#team-logo')).css('margin-top', '10px');
            $('.breadcrumb').removeClass('inline-block breadcrumb-inner');
            $('#team-logo').after($('#team-name')).removeClass('team-logo-inner inline-block').css('margin-left', '0px');
            $('#team-name').removeClass('team-name-inner inline-block');
            $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important').css('box-shadow', '0','important'));
            $('.page-container').css('margin-top', '0px');
            scrolledAfterTeamInfo = false;
        }
    });
    var y = $(window).scrollTop();
    //player card
    if(topPlayer && y >= topPlayer && !scrolledAfterPlayer){
        //console.log('player call ');
        $('.breadcrumb').after($("<div class='inline-block min-photo-container'></div>"));
        $('#player-card-avatar').addClass('clipped-img');
        $('#player-card-avatar').detach().appendTo($('.min-photo-container').css('margin-left', (1000 - 110 - breadcrumbWidth*2 - playerNameWidth)/2 + 'px', 'important'));
        $('.min-photo-container').after($('#player-card-name').addClass('inline-block').css('font-weight', '700', 'important'));
        $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important'));
        $('.page-container').css('margin-top', '68px');
        scrolledAfterPlayer = true;
    } else if (topPlayer && y < topPlayer && scrolledAfterPlayer){
        //console.log('player reverse call ');
        $('#player-card-amplua').before($('#player-card-name').removeClass('inline-block').css('margin-left', 0 + 'px', 'important').css('font-weight', '400', 'important'));
        $('#player-card-desc').before($('#player-card-avatar').removeClass('clipped-img').css('margin-left', '0'));
        $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important'));
        $('.page-container').css('margin-top', '0px');
        $(".min-photo-container").remove();
        scrolledAfterPlayer = false;
    }
    //team card
    if (topSecondary && y >= topSecondary && !scrolledAfterTeamInfo && !$('#player-card-block').length){
        //console.log('team info call ');
        $('.page-container').css('margin-top', '114px');
        $('.my-team-btn').css('margin-top', '4px');
        $('.breadcrumb').after($('#team-logo')).addClass('inline-block breadcrumb-inner');
        $("#team-logo").after($('#team-name')).addClass('team-logo-inner inline-block').css('margin-left', teamLogoMargin + 'px', 'important');
        $('#team-name').addClass('team-name-inner inline-block');
        $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important'));
        scrolledAfterTeamInfo = true;
    } else if (topSecondary && y < topSecondary && scrolledAfterTeamInfo){
        //console.log('team info reverse call ');
        $('.my-team-btn').after($('#team-logo')).css('margin-top', '10px');
        $('.breadcrumb').removeClass('inline-block breadcrumb-inner');
        $('#team-logo').after($('#team-name')).removeClass('team-logo-inner inline-block').css('margin-left', '0px');
        $('#team-name').removeClass('team-name-inner inline-block');
        $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important'));
        $('.page-container').css('margin-top', '0px');
        scrolledAfterTeamInfo = false;
    }
    if (top && y >= top) {
        if($('.team-info').length) {
            $('.team-info').css('margin-top', '52px'); // club page
        } else {
            if($('.player-card-block').length){ // players-page
                if($('.breadcrumbs').length){
                    $('.breadcrumbs').next().css('margin-top', '42px')
                }
            } else ($('.page-container').css('margin-top', '42px')) // clubs page
        }
        if(!$('.sm-logo').length) $('.breadcrumb').before($("<img class='sm-logo' style='vertical-align: middle; margin-right: 5px; float: left;' src='/static/images/sm_micro.png'>"));
        $('.breadcrumbs').addClass('fixed');
    } else if(top && y < top) {
        $('.breadcrumbs').removeClass('fixed');
        if($('.sm-logo').length) $('.sm-logo').remove();
        if($('.team-info').length) {
            $('.team-info').css('margin-top', '0px');
        } else {
            if($('.player-card-block').length){
                if($('.breadcrumbs').length){
                    $('.breadcrumbs').next().css('margin-top', '0px')
                }
            } else ($('.page-container').css('margin-top', '0px'))
        }
    }
});*/
/*$(function(){
    if($('.breadcrumb').length){
        ($('.breadcrumb').first().find($('.section').last()).css('text-decoration', 'none'));
    }
});*/
$.fn.textWidth = function(){
    var html_org = $(this).html();
    var html_calc = '<span>' + html_org + '</span>';
    $(this).html(html_calc);
    var width = $(this).find('span:first').width();
    $(this).html(html_org);
    return width;
};
