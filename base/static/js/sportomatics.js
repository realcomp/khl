'use strict';
angular.module('Sportomatics', ['angucomplete'])

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
//TODO: make expressions to check if already scrolled (for performance)
$(function() {
    var top = null;
    var topSecondary = null;
    var topThird = null;
    var breadcrumbWidth = null;
    var teamNameWidth = null;
    if($('.breadcrumbs').length){
        top = $('.breadcrumbs').offset().top;
        if($('.breadcrumb').length)
        breadcrumbWidth = $('.breadcrumb').first().css('width').substr(0, $('.breadcrumb').first().css('width').length -2);
    }
    if($('.team-info').length){
        topSecondary = $('.team-info').offset().top;
        teamNameWidth = parseInt($('#team-name').css('width').substr(0, $('#team-name').css('width').length-2));
    }
    if($('.page-menu').length){
        topThird = $('.page-menu').offset().top - 40;
    }
    $(window).scroll(function(event) {
        var y = $(window).scrollTop();
        if (top && y >= top) {
            if($('.team-info').length) {
                $('.team-info').css('margin-top', '52px');
            } else {($('.page-container').css('margin-top', '42px'))}
            $('.breadcrumbs').addClass('fixed');//.css('border-bottom', '1px solid #f2f2f2');
        } else if(top && y < top) {
            $('.breadcrumbs').removeClass('fixed');//.css('border-bottom', 'none');
            if($('.team-info').length) {
                $('.team-info').css('margin-top', '0px');
            } else {($('.page-container').css('margin-top', '0px'))}
        }
        if (topSecondary && y >= topSecondary){
            $('.team-info').css('margin-top', '106px');
            $('.my-team-btn').css('margin-top', '4px');
            $('.breadcrumb').after($('#team-logo'));
            $("#team-logo").after($('#team-name'));
            $('#team-name').addClass('team-name-inner inline-block');
            $('.breadcrumb').addClass('inline-block breadcrumb-inner');
            $('#team-logo').addClass('team-logo-inner inline-block');
            $('#team-logo').css('margin-left', (1000 - breadcrumbWidth*2 - (25+teamNameWidth))/2 + 'px', 'important');
        } else if (topSecondary && y < topSecondary){
            $('.my-team-btn').after($('#team-logo'));
            $('.my-team-btn').css('margin-top', '10px');
            $('#team-logo').after($('#team-name'));
            $('#team-logo').css('margin-left', '0px');
            $('.breadcrumb').removeClass('inline-block breadcrumb-inner');
            $('#team-logo').removeClass('team-logo-inner inline-block');
            $('#team-name').removeClass('team-name-inner inline-block');
        }
        if (topThird && y >= topThird){
            $('.team-info').css('margin-top', '150px', 'important')
            $('.search-block').after($('.page-menu'));
            $('.page-menu').css('margin-left', '5px', 'important');
            $('.page-menu').css('margin-right', '5px', 'important');
        } else if (topThird && y < topThird){
            $('.page-menu').removeClass('fixed');
            $('.page-inner-container').before($('.page-menu'));
            $('.page-menu').css('margin-left', '0px', 'important');
            $('.page-menu').css('margin-right', '0px', 'important');
        }
    });
    var y = $(window).scrollTop();
    if (topThird && y >= topThird){
        $('.team-info').css('margin-top', '150px', 'important')
        $('.search-block').after($('.page-menu'));
        $('.page-menu').css('margin-left', '5px', 'important');
        $('.page-menu').css('margin-right', '5px', 'important');
    } else if (topThird && y < topThird){
        $('.page-menu').removeClass('fixed');
        $('.page-inner-container').before($('.page-menu'));
        $('.page-menu').css('margin-left', '0px', 'important');
        $('.page-menu').css('margin-right', '0px', 'important');
    }
    if (topSecondary && y >= topSecondary){
        $('.team-info').css('margin-top', '106px');
        $('.my-team-btn').css('margin-top', '4px');
        $('.breadcrumb').after($('#team-logo'));
        $("#team-logo").after($('#team-name'));
        $('#team-name').addClass('team-name-inner inline-block');
        $('.breadcrumb').addClass('inline-block breadcrumb-inner');
        $('#team-logo').addClass('team-logo-inner inline-block');
        $('#team-logo').css('margin-left', (1000 - breadcrumbWidth*2 - (25+teamNameWidth))/2 + 'px', 'important');
    } else if (topSecondary && y < topSecondary){
        $('.my-team-btn').after($('#team-logo'));
        $('.my-team-btn').css('margin-top', '10px');
        $('#team-logo').after($('#team-name'));
        $('#team-logo').css('margin-left', '0px');
        $('.breadcrumb').removeClass('inline-block breadcrumb-inner');
        $('#team-logo').removeClass('team-logo-inner inline-block');
        $('#team-name').removeClass('team-name-inner inline-block');
    }
    if (top && y >= top) {
        if($('.team-info').length) {
            $('.team-info').css('margin-top', '52px');
        } else {($('.page-container').css('margin-top', '42px'))}
        $('.breadcrumbs').addClass('fixed');
    } else if(top && y < top) {
        $('.breadcrumbs').removeClass('fixed');
        if($('.team-info').length) {
            $('.team-info').css('margin-top', '0px');
        } else {($('.page-container').css('margin-top', '0px'))}
    }
});
/*$(function(){
    if($('.breadcrumb').length){
        ($('.breadcrumb').first().find($('.section').last()).css('text-decoration', 'none'));
    }
});*/
