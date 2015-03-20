'use strict';
angular.module('Sportomatics', ['angucomplete', 'ngTagsInput', 'ui.router', 'ngResource', 'ngCookies'])
.config(["$stateProvider", "$urlRouterProvider", function($stateProvider, $urlRouterProvider){
    $stateProvider
        .state('playersCoaches', {
            url: '/ru/hockey/players',
            templateUrl: ' ',
            controller: ["$state", function($state){
                alert($state)
            }]
        })
}]);
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
        $('#player-card-amplua').before($('#player-card-name').removeClass('inline-block').css('margin-left', 0 + 'px', 'important'));
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
});
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

angular.module('Sportomatics')

angular.module('Sportomatics')
.value('zoomData', {
    startDate: 'a',
    endDate: 'a'
})
.factory('ChartFactory', ["$q", "$rootScope", "AmChartsFactory", "zoomData", "LocaleFactory", function($q, $rootScope, AmChartsFactory, zoomData, LocaleFactory){

    return {
        generateSerialChart: function(field, chartData, localeObject, graphs){
            // Method accepts
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                var data = chartData.data;

                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = data;//[{"date":"2010-06-30T00:00:00.000Z","values1":7,"count1":5,"percentage1":0.152,"values":9,"count":6,"percentage":0.173},{"date":"2011-06-30T00:00:00.000Z","values1":9,"count1":9,"percentage1":0.111,"values":6,"count":9,"percentage":0.067},{"date":"2012-06-30T00:00:00.000Z","values1":13,"count1":7,"percentage1":0.188,"values":7,"count":4,"percentage":0.206},{"date":"2013-06-30T00:00:00.000Z","values1":9,"count1":7,"percentage1":0.129,"values":11,"count":7,"percentage":0.177},{"date":"2014-06-30T00:00:00.000Z","values1":5,"count1":7,"percentage1":0.071,"values":9,"count":5,"percentage":0.22},{"date":"2015-06-30T00:00:00.000Z","values1":4,"count1":6,"percentage1":0.067,"values":3,"count":4,"percentage":0.094},{"date":"1998-06-30T00:00:00.000Z","values1":1,"count1":4,"percentage1":0.029},{"date":"1999-06-30T00:00:00.000Z","values1":6,"count1":5,"percentage1":0.146},{"date":"2000-06-30T00:00:00.000Z","values1":1,"count1":5,"percentage1":0.024},{"date":"2001-06-30T00:00:00.000Z","values1":6,"count1":6,"percentage1":0.109},{"date":"2002-06-30T00:00:00.000Z","values1":3,"count1":5,"percentage1":0.068},{"date":"2003-06-30T00:00:00.000Z","values1":2,"count1":5,"percentage1":0.043},{"date":"2004-06-30T00:00:00.000Z","values1":0,"count1":4,"percentage1":0},{"date":"2005-06-30T00:00:00.000Z","values1":6,"count1":6,"percentage1":0.105},{"date":"2006-06-30T00:00:00.000Z","values1":10,"count1":7,"percentage1":0.161},{"date":"2007-06-30T00:00:00.000Z","values1":4,"count1":5,"percentage1":0.082},{"date":"2008-06-30T00:00:00.000Z","values1":4,"count1":7,"percentage1":0.062},{"date":"2009-06-30T00:00:00.000Z","values1":2,"count1":4,"percentage1":0.05}];
                chart.categoryField = "date";
                chart.cursorColor = "#DADADA";
                chart.startDuration = 0.5;
                chart.startEffect = "easeOutSine";
                chart.addClassNames = true;
                chart.depth3D = 60;
                chart.angle = 30;
                chart.exportConfig = {
                    "menuTop":"45px",
                        "menuRight":"5px",
                        "menuItems": [{
                        "icon": 'http://www.amcharts.com/lib/3/images/export.png',
                        "format": 'png'
                    }]
                }

                // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener("dataUpdated", zoomChart);
                chart.addListener("zoomed", function (chart) {
                    zoomData.startDate = chart.startDate;
                    zoomData.endDate = chart.endDate;
                });
                // AXES
                // category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "MM"; // our data is daily, so we set minPeriod to DD
                //categoryAxis.minorGridEnabled = true;
                //categoryAxis.autoGridCount =  true;
                //categoryAxis.grudCount = 12;
                categoryAxis.equalSpacing = true;
                categoryAxis.minHorizontalGap = 40;
                categoryAxis.gridAlpha = 0; //categoryAxis.gridAlpha = 0.1;
                //categoryAxis.gridPosition = 'start';
                categoryAxis.boldPeriodBeginning = false;
                categoryAxis.axisColor = "#DADADA";
                //categoryAxis.twoLineMode = true;
                //categoryAxis.tickLength = 12;
                categoryAxis.markPeriodChange = false;
                categoryAxis.dateFormats = [{
                    period: 'fff',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'ss',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'mm',
                    format: 'JJ:NN'
                }, {
                    period: 'hh',
                    format: 'JJ:NN'
                }, {
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];
                categoryAxis.labelFunction = function(valueText, date, categoryAxis){
                    var value = new Date(date);
                    if(chartData.groupBy === 'season'){
                        var endDate = valueText.substr(2, 2);
                        var startDate = (endDate === '00') ? '99' : (parseInt(endDate)-1).toString();
                        if(startDate.length === 1) startDate = '0'+ startDate;
                        return startDate + '/'+ endDate;
                    }
                    if(valueText === 'Jan'){
                        return localeObject.monthNames[value.getMonth()] + '\u000A' + value.getFullYear();
                    }
                    return localeObject.monthNames[value.getMonth()];
                };

                var currMax = Math.max.apply(Math, data.map(function(e){ return e['values']}));
                var currMin = Math.min.apply(Math, data.map(function(e){ return e['values']}));

                // first value axis (on the left)
                var valueAxis1 = new AmCharts.ValueAxis();
                valueAxis1.axisColor = "#408e3a";
                valueAxis1.axisThickness = 1;
                valueAxis1.gridAlpha = 0.1;
                valueAxis1.maximum = (currMax === 0) ? +2 : (currMax/10 > 0) ? currMax+(currMax/10)*5: currMax + currMax%10;
                valueAxis1.minimum = (currMin === 0) ? -2 : (currMin/10 > 0) ? currMin-(currMin/10)*5 : currMin - Math.abs(currMin%10);
                valueAxis1.stackType = "3d";
                chart.addValueAxis(valueAxis1);

                // second value axis (on the right)
                var gamesAxis = new AmCharts.ValueAxis();
                gamesAxis.position = "right"; // this line makes the axis to appear on the right
                gamesAxis.axisColor = "#408e3a";
                gamesAxis.gridAlpha = 0;
                gamesAxis.axisThickness = 0;
                gamesAxis.stackType = "regular";
                gamesAxis.maximum = 5;
                chart.addValueAxis(gamesAxis);

                // third value axis (on the left, detached)
                var valueAxis3 = new AmCharts.ValueAxis();
                valueAxis3.offset = 50; // this line makes the axis to appear detached from plot area
                valueAxis3.gridAlpha = 0;
                valueAxis3.axisColor = "#B0DE09";
                valueAxis3.axisThickness = 2;
                chart.addValueAxis(valueAxis3);

                if(graphs && graphs.length){
                    _.each(graphs, function(graph){
                        graph.valueAxis = valueAxis1;
                        chart.addGraph(graph);
                    })
                } else {
                    // GRAPHS
                    var graph1 = new AmCharts.AmGraph();
                    graph1.id = "g2";
                    graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                    graph1.title = field;
                    graph1.valueField = "values";
                    graph1.bullet = "none";
                    graph1.hideBulletsCount = 30;
                    graph1.bulletBorderThickness = 1;
                    graph1.lineColor = "#408e3a";
                    graph1.fillColors = "#408e3a";
                    graph1.fillAlphas = 1;
                    graph1.lineThickness = 0;
                    //graph1.animationPlayed = true;
                    graph1.type = 'column';
                    if(field === 'goals' || field === 'assists' || field === 'points' || field === 'plus_minus' || field === 'penalty_time' )
                        graph1.balloonText = '<span style="text-align: left; float: left">'+localeObject.fieldNames[field].shortName + ': [[values]]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage]]</span>';
                    chart.addGraph(graph1);
                }



                var graph1Copy = new AmCharts.AmGraph();
                graph1Copy.id = "g2";
                graph1Copy.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                graph1Copy.title = field;
                graph1Copy.valueField = "values1";
                graph1Copy.bullet = "none";
                graph1Copy.hideBulletsCount = 30;
                graph1Copy.bulletBorderThickness = 1;
                graph1Copy.lineColor = "#FF3232";
                graph1Copy.fillColors = "#FF3232";
                graph1Copy.fillAlphas = 1;
                graph1Copy.lineThickness = 0;
                graph1Copy.type = 'column'
                //chart.addGraph(graph1Copy);

                var graph2 = new AmCharts.AmGraph();
                graph2.id = "g2";
                graph2.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                graph2.title = field;
                graph2.valueField = "values";
                graph2.bullet = "none";
                graph2.hideBulletsCount = 30;
                graph2.bulletBorderThickness = 1;
                graph2.lineColor = "#c0c0c0";
                graph2.lineThickness = 1;
                graph2.animationPlayed = true;
                graph2.type = 'line';
                graph2.balloonText = '';
                graph2.visibleInLegend = false;
                //chart.addGraph(graph2);

                // second graph
                var gamesGraph = new AmCharts.AmGraph();
                gamesGraph.valueField = "count";
                gamesGraph.title = "games";
                gamesGraph.type = "step";
                gamesGraph.fillAlphas = 0;
                gamesGraph.lineColor = "#408e3a";
                gamesGraph.alphaField = "alpha";
                gamesGraph.lineThickness = 0;
                gamesGraph.lineAlpha = 0.3;
                gamesGraph.balloonText = '';
                gamesGraph.visibleInLegend = false;
                gamesGraph.velueAxis = gamesAxis;
                if(field !== 'count')
                chart.addGraph(gamesGraph);

                // SCROLLBAR
                var chartScrollbar = new AmCharts.ChartScrollbar();
                if(field !== 'count')
                chartScrollbar.graph = gamesGraph;
                chartScrollbar.autoGridCount = true;
                chartScrollbar.color = "#000000";
                chart.addChartScrollbar(chartScrollbar);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);

                // LABEL
                chart.allLabels = [{
                    align: 'center',
                    y: 60,
                    alpha: 0.7,
                    bold: true,
                    text: localeObject.fieldNames[field].fullName.toUpperCase()
                }];

                // CURSOR
                var chartCursor = new AmCharts.ChartCursor();
                chartCursor.cursorAlpha = 1;
                chartCursor.cursorColor = "#8ebd5d";
                //chartCursor.avoidBalloonOverlapping = false;
                chartCursor.oneBalloonOnly = true;
                chartCursor.categoryBalloonFunction = function(value){
                    if(chartData.groupBy === 'month'){
                        return localeObject.monthNames[value.getMonth()] + ' ' + value.getFullYear();
                    } else {
                        return localeObject.words.season +  (value.getFullYear()-1).toString().substr(2, 2) + '/' + value.getFullYear().toString().substr(2, 2)
                    }
                };
                chart.addChartCursor(chartCursor);

                deferred.resolve(chart);
            });
            return deferred.promise; //метод возвращает промис и ждет когда выполнится resolve, а он выполнится после полного создания графика
        },
        generateSerialLineChart: function(field, chartData, localeObject, graphs){
            // Method accepts
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                var data = chartData;

                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = data;//[{"date":"2010-06-30T00:00:00.000Z","values1":7,"count1":5,"percentage1":0.152,"values":9,"count":6,"percentage":0.173},{"date":"2011-06-30T00:00:00.000Z","values1":9,"count1":9,"percentage1":0.111,"values":6,"count":9,"percentage":0.067},{"date":"2012-06-30T00:00:00.000Z","values1":13,"count1":7,"percentage1":0.188,"values":7,"count":4,"percentage":0.206},{"date":"2013-06-30T00:00:00.000Z","values1":9,"count1":7,"percentage1":0.129,"values":11,"count":7,"percentage":0.177},{"date":"2014-06-30T00:00:00.000Z","values1":5,"count1":7,"percentage1":0.071,"values":9,"count":5,"percentage":0.22},{"date":"2015-06-30T00:00:00.000Z","values1":4,"count1":6,"percentage1":0.067,"values":3,"count":4,"percentage":0.094},{"date":"1998-06-30T00:00:00.000Z","values1":1,"count1":4,"percentage1":0.029},{"date":"1999-06-30T00:00:00.000Z","values1":6,"count1":5,"percentage1":0.146},{"date":"2000-06-30T00:00:00.000Z","values1":1,"count1":5,"percentage1":0.024},{"date":"2001-06-30T00:00:00.000Z","values1":6,"count1":6,"percentage1":0.109},{"date":"2002-06-30T00:00:00.000Z","values1":3,"count1":5,"percentage1":0.068},{"date":"2003-06-30T00:00:00.000Z","values1":2,"count1":5,"percentage1":0.043},{"date":"2004-06-30T00:00:00.000Z","values1":0,"count1":4,"percentage1":0},{"date":"2005-06-30T00:00:00.000Z","values1":6,"count1":6,"percentage1":0.105},{"date":"2006-06-30T00:00:00.000Z","values1":10,"count1":7,"percentage1":0.161},{"date":"2007-06-30T00:00:00.000Z","values1":4,"count1":5,"percentage1":0.082},{"date":"2008-06-30T00:00:00.000Z","values1":4,"count1":7,"percentage1":0.062},{"date":"2009-06-30T00:00:00.000Z","values1":2,"count1":4,"percentage1":0.05}];
                chart.categoryField = "date";
                chart.cursorColor = "#DADADA";
                chart.addClassNames = true;

                // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener("dataUpdated", zoomChart);
                chart.addListener("zoomed", function (chart) {
                    zoomData.startDate = chart.startDate;
                    zoomData.endDate = chart.endDate;
                });
                // AXES
                // category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "MM"; // our data is daily, so we set minPeriod to DD
                categoryAxis.autoGridCount =  true;
                categoryAxis.equalSpacing = true;
                categoryAxis.minHorizontalGap = 40;
                categoryAxis.gridAlpha = 0.1; //categoryAxis.gridAlpha = 0.1;
                categoryAxis.boldPeriodBeginning = false;
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.gridPosition =  "start";
                categoryAxis.markPeriodChange = false;
                categoryAxis.dateFormats = [{
                    period: 'fff',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'ss',
                    format: 'JJ:NN:SS'
                }, {
                    period: 'mm',
                    format: 'JJ:NN'
                }, {
                    period: 'hh',
                    format: 'JJ:NN'
                }, {
                    period: 'DD',
                    format: 'DD'
                }, {
                    period: 'WW',
                    format: 'DD'
                }, {
                    period: 'MM',
                    format: 'MMM'
                }, {
                    period: 'YYYY',
                    format: 'YYYY'
                }];
                categoryAxis.labelFunction = function(valueText, date, categoryAxis){
                    var value = new Date(date);
                    if(chartData.groupBy === 'season'){
                        var endDate = valueText.substr(2, 2);
                        var startDate = (endDate === '00') ? '99' : (parseInt(endDate)-1).toString();
                        if(startDate.length === 1) startDate = '0'+ startDate;
                        return startDate + '/'+ endDate;
                    }
                    if(valueText === 'Jan'){
                        return  value.getFullYear();
                    }
                    return localeObject.monthNames[value.getMonth()];
                };

                var currMax = Math.max.apply(Math, data.map(function(e){ return e['values']}));
                var currMin = Math.min.apply(Math, data.map(function(e){ return e['values']}));

                // first value axis (on the left)
                var valueAxis1 = new AmCharts.ValueAxis();
                valueAxis1.axisColor = "#408e3a";
                valueAxis1.axisThickness = 1;
                valueAxis1.gridAlpha = 0.1;
                valueAxis1.reversed = true;
                valueAxis1.tickLength = 2;
                valueAxis1.maximum = 18;//(currMax === 0) ? +2 : (currMax/10 > 0) ? currMax+(currMax/10)*5: currMax + currMax%10;
                valueAxis1.minimum = 1;//(currMin === 0) ? -2 : (currMin/10 > 0) ? currMin-(currMin/10)*5 : currMin - Math.abs(currMin%10);
                valueAxis1.labelFunction = function(value){
                    if(value === 2 || value === 16){
                        return value + ' место'
                    }
                    return '';
                };
                chart.addValueAxis(valueAxis1);

                if(graphs && graphs.length){
                    _.each(graphs, function(graph){
                        console.log('a', graph.type);
                        graph.valueAxis = valueAxis1;
                        graph.visibleInLegend = false;
                        chart.addGraph(graph);
                    })
                }


                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);

                // LABEL
                chart.allLabels = [{
                    align: 'center',
                    y: 60,
                    alpha: 0.7,
                    bold: true,
                    text: localeObject.fieldNames[field].fullName.toUpperCase()
                }];




                // CURSOR
                var chartCursor = new AmCharts.ChartCursor();
                chartCursor.cursorAlpha = 1;
                chartCursor.cursorColor = "#8ebd5d";
                chartCursor.categoryBalloonFunction = function(value){
                    if(chartData.groupBy === 'month'){
                        return localeObject.monthNames[value.getMonth()] + ' ' + value.getFullYear();
                    } else {
                        return localeObject.words.season +  (value.getFullYear()-1).toString().substr(2, 2) + '/' + value.getFullYear().toString().substr(2, 2)
                    }
                };
                chart.addChartCursor(chartCursor);

                deferred.resolve(chart);
            });
            return deferred.promise; //метод возвращает промис и ждет когда выполнится resolve, а он выполнится после полного создания графика
        },
        generateRadarChart: function(data, graphs){
            // Method accepts
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {

                chart = new AmCharts.AmRadarChart();
                chart.dataProvider = data;
                chart.categoryField = "field";

                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.axisAlpha = 0.15;
                valueAxis.minimum = 0;
                valueAxis.maximum = 1;
                valueAxis.dashLength = 3;
                valueAxis.axisTitleOffset = 20;
                valueAxis.gridCount = 5;
                chart.addValueAxis(valueAxis);

                _.each(graphs, function(graph){
                    graph.valueAxis = valueAxis;
                    chart.addGraph(graph);
                });

                deferred.resolve(chart);
            });
            return deferred.promise;

        }
    }
}]);
var colors = ["#26A65B", "#CF000F", "#663399", "#F9690E"];

// this method is called when chart is first inited as we listen for "dataUpdated" event
function zoomChart() {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    //chart.zoomToIndexes(10, 20);
}
function generateGraph(i, title, axis){
        var graph = new AmCharts.AmGraph();
        graph.valueAxis = axis; // we have to indicate which value axis should be used
        graph.title = title;
        graph.valueField = 'value'+i;
        graph.bullet = "round";
        graph.hideBulletsCount = 30;
        graph.bulletBorderThickness = 1;
        graph.lineColor = colors[i]; //TODO: add more colors
        graph.lineThickness = 4;
        return graph;
}
function saveZoomParams(endDate, endIndex, endValue, startDate){

}
function makeGraph(id, title, color, field, valueAxis, localeObject){
    var graph = new AmCharts.AmGraph();
    graph.id = "gl"+id;
    graph.valueAxis = valueAxis; // we have to indicate which value axis should be used
    graph.title = title + ' ' + field;
    graph.valueField = "values" + id;
    graph.bullet = "none";
    graph.hideBulletsCount = 30;
    graph.bulletBorderThickness = 1;
    graph.lineColor = color;
    graph.fillColors = color;
    graph.fillAlphas = 1;
    graph.lineThickness = 0;
    graph.type = 'column';
    if(field === 'goals' || field === 'assists' || field === 'points' || field === 'plus_minus' || field === 'penalty_time' )
        graph.balloonText = '<span style="text-align: left; float: left">'+localeObject.fieldNames[field].shortName + ': [[values2]]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage2]]</span>';

    return graph;
}
angular.module('Sportomatics')
    .factory('LocaleFactory', ["$rootScope", function($rootScope){
        var chosen = 'ru';
        return {
            getFieldName: function(field, locale){
                var fieldNames = {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Плюс/Минус'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время, мин'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру'
                    },
                    change_count__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру'
                    },
                    shots_received: {
                        shortName: 'Бр',
                        fullName: 'Броски'
                    },
                    loose_goals: {
                        shortName: 'ПШ',
                        fullName: 'Пропущенные шайбы'
                    },
                    saves: {
                        shortName: 'ОШ',
                        fullName: 'Отраженные броски'
                    },
                    saves_p__avg: {
                        shortName: '%ОШ',
                        fullName: 'Процент отраженных бросков'
                    },
                    sf__avg: {
                        shortName: 'КН',
                        fullName: 'Коэффициент надежности'
                    },
                    matches_win: {
                        shortName: 'В',
                        fullName: 'Выигрыши'
                    },
                    matches_lose: {
                        shortName: 'П',
                        fullName: 'Проигрыши'
                    },
                    zero_goals_matches: {
                        shortName: 'И"0"',
                        fullName: '"Сухие игры"'
                    },
                    bullet_matches: {
                        shortName: 'ИБ',
                        fullName: 'Игры с буллитными сериями'
                    }
                };
                var fieldNamesEn = {
                    count: {
                        shortName: 'GP',
                        fullName: 'Games played'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game'
                    },
                    change_count__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game'
                    }
                };
                return (locale === 'en') ? fieldNamesEn[field]['fullName'] : fieldNames[field]['fullName'];
            },
            locale_ru: {
                fieldNames: {
                    count: {
                        shortName: 'И',
                        fullName: 'Количество проведенных игр'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Коэффициент полезности'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время, мин'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру, мин'
                    },
                    change_count__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру'
                    },
                    shots_received: {
                        shortName: 'Бр',
                        fullName: 'Броски'
                    },
                    loose_goals: {
                        shortName: 'ПШ',
                        fullName: 'Пропущенные шайбы'
                    },
                    saves: {
                        shortName: 'ОШ',
                        fullName: 'Отраженные броски'
                    },
                    saves_p__avg: {
                        shortName: '%ОШ',
                        fullName: 'Процент отраженных бросков'
                    },
                    sf__avg: {
                        shortName: 'КН',
                        fullName: 'Коэффициент надежности'
                    },
                    matches_win: {
                        shortName: 'В',
                        fullName: 'Выигрыши'
                    },
                    matches_lose: {
                        shortName: 'П',
                        fullName: 'Проигрыши'
                    },
                    zero_goals_matches: {
                        shortName: 'И"0"',
                        fullName: '"Сухие игры"'
                    },
                    bullet_matches: {
                        shortName: 'ИБ',
                        fullName: 'Игры с буллитными сериями'
                    },
                    position: {
                        shortName: '',
                        fullName: 'Место'
                    }
                },
                buttonNames: {
                    month: 'По месяцам',
                    season: 'По сезонам',
                    allSeasons: 'Все сезоны'
                },
                monthNames: ["Янв", "Фев", "Мар", "Апр", "Май", "Июн",
                    "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
                words: {
                    season: 'Сезон',
                    moths: 'Месяц'
                }
            },
            locale_en: {
                fieldNames: {
                    count: {
                        shortName: 'GP',
                        fullName: 'Games played'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game'
                    },
                    change_count__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game'
                    }
                },
                buttonNames: {
                    month: 'By month',
                    season: 'By season'
                },
                monthNames : ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
                words: {
                    season: 'Season',
                    moths: 'Month'
                }
            }
        }

    }])

angular.module('Sportomatics')
.service('PlayersSearchService', ["$http", function($http) {
    this.loadCountries = function($scope, $location, callback) {
        var url = $('#LeagueListLink').attr('href'),
        country;
        if (url) {
            $http.get(url).success(function(data) {
                $scope.countries = data;
                if ($scope.countries.length) {
                    country = $scope.countries[0];
                    if (!$location.search().country) {
                        $location.search('country', String(country.pk));
                        $scope.params = $location.search();
                    }
                    if (country.league_set.length &&
                            !$location.search().league &&
                            $location.search().league !== '') {
                        $location.search('league', String(country.league_set[0].pk));
                        $scope.params = $location.search();
                    }
                }
                if (callback && typeof callback === 'function') {
                    callback($scope);
                }
            });
        } else if (callback && typeof callback === 'function') {
            callback($scope);
        }
    };

    this.getLeagues = function(countries, selected) {
        var result = [];
        if (selected) {
            if (Array.isArray(selected)) {
                $.each(selected, function() {
                    var pk = this;
                    $.each(countries, function() {
                        if (this.pk == pk) {
                            result = result.concat(this.league_set);
                        }
                    });
                });
            } else {
                $.each(countries, function() {
                    if (this.pk == selected) {
                        result = result.concat(this.league_set);
                    }
                });
            }
        }
        return result;
    };

    this.isMatchesTotalVisible = function($scope) {
        return ($scope.params.rated_by === 'goals_average' ||
            $scope.params.rated_by === 'assists_average' ||
            $scope.params.rated_by === 'points_average' ||
            $scope.params.rated_by === 'plus_minus_average')
    }

    this.setOrderBy = function($scope, order_by) {
        if (!$scope.loader) {
            if ($scope.params.order_by === order_by ||
                    (!$scope.params.order_by && !order_by)) { // same field -> reverse
                if ($scope.params.reversed === 'true') {
                    $scope.$location.search('reversed', null);
                } else {
                    $scope.$location.search('reversed', 'true');
                }
            } else { // other field -> reset
                $scope.$location.search('reversed', null);
            }
            $scope.$location.search('order_by', order_by || null);
            this.search($scope);
        }
    };

    this.setPlaying = function($scope, is_playing) {
        if (!$scope.loader && $scope.params.is_playing !== is_playing) {
            if (is_playing === 'false') {
                $scope.$location.search('is_playing', is_playing);
            } else {
                $scope.$location.search('is_playing', null);
            }
            this.search($scope);
        }
    }

    this.setRatedBy = function($scope, rated_by) {
        if (!$scope.loader && $scope.params.rated_by !== rated_by) {
            $scope.$location.search('rated_by', rated_by || null);
            if (rated_by) { // by rating -> set ordering
                $scope.$location.search('order_by', 'rating');
                $scope.$location.search('reversed', 'true');
                this.search($scope);
            } else { // by alphabet -> reset ordering
                this.setOrderBy($scope, '');
            }
        }
    };

    this.setAlphabetFilter = function($scope, alphabet) {
        if (!$scope.loader && $scope.params.alphabet !== alphabet) {
            $scope.$location.search('alphabet', alphabet);
            this.search($scope);
        }
    };

    this.setPlayersFilter = function($scope, obj) {
        var value;
        if (obj) {
            value = String(obj.originalObject.pk);
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.player !== value) {
            $scope.$location.search('player', value);
            this.search($scope);
        }
    };

    this.setClubsFilter = function($scope, obj) {
        var value;
        if (obj) {
            value = String(obj.originalObject.pk);
        } else {
            value = null;
        }
        if (!$scope.loader && $scope.params.club !== value) {
            $scope.$location.search('club', value);
            this.search($scope);
        }
    };

    this.search = function($scope) {
        var f = function() {
            var url = $('#PlayersSearchLink').attr('href'),
            line = [], params = '', i;

            if ($('#isCitizenshipRussia').is(':checked')) {
                $scope.$location.search('citizenship1', $('#citizenshipRussia').val());
            } else {
                $scope.$location.search('citizenship1', null);
            }
            if ($('#isCitizenshipOther').is(':checked')) {
                $scope.$location.search('citizenship_other', 'true');
                if ($scope.$location.search().citizenship2) {
                    $('#citizenshipOther').val($scope.$location.search().citizenship2);
                }
                if ($('#citizenshipOther').val()) {
                    $scope.$location.search('citizenship2', $('#citizenshipOther').val());
                }
            } else {
                $scope.$location.search('citizenship_other', null);
            }

            $.each($('[name="line"]:checked'), function() {
                var value = $(this).val();
                if (value) {
                    line.push(value);
                }
            });
            $scope.$location.search('line', line);

            if (!$scope.leaguesLoaded) {
                $scope.leaguesLoaded = true;
                if ($scope.params.league) {
                    if (Array.isArray($scope.params.league)) {
                        $scope.leaguesSelected = $scope.params.league;
                    } else {
                        $scope.leaguesSelected = [$scope.params.league];
                    }
                }
            }
            $scope.$location.search('league', $scope.leaguesSelected);

            $scope.params = $scope.$location.search();

            params += '&order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
            if ($scope.params.reversed) {
                params += '&reversed=true';
            }
            if ($scope.params.line.length) {
                $.each($scope.params.line, function() {
                    params += '&line=' + this;
                });
            }
            if ($scope.params.citizenship1) {
                params += '&citizenship=' + $scope.params.citizenship1;
            }
            if ($scope.params.citizenship2) {
                params += '&citizenship=' + $scope.params.citizenship2;
            }
            if ($scope.params.citizenship_other === 'true') {
                params += '&citizenship_other=true';
            }
            if ($scope.params.rated_by) {
                params += '&rated_by=' + $scope.params.rated_by;
            }
            if ($scope.params.is_playing !== 'false') {
                params += '&is_playing=true';
            }
            if ($scope.params.alphabet) {
                params += '&%s_lastname__startswith=' + $scope.params.alphabet;
            }
            if ($scope.params.club) {
                params += '&club=' + $scope.params.club;
            }
            if ($scope.params.player) {
                params += '&player=' + $scope.params.player;
            }
            if ($scope.params.league) {
                $.each($scope.params.league, function() {
                    params += '&league=' + this;
                });
            }
            $scope.data = {};
            $scope.loader = true;
            $http.get(url + '?' + params).success(function(data) {
                $scope.data = data;
                $scope.loader = false;
            });
        };

        // if (!$scope.countries) {
        //      this.loadCountries($scope, $scope.$location, f);
        // } else {
            f($scope);
        // }
    };

    this.next = function($scope, isAll) {
        var url = $scope.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
        }
        $scope.loader = true;
        $http.get(url).success(function(data) {
            if (isAll) {
                $scope.data = data;
            } else {
                $scope.data.next = data.next;
                $scope.data.results = $scope.data.results.concat(data.results);
            }
            $scope.loader = false;
        });
    };
}]);

angular.module('Sportomatics').service('ProfileService',
    ["$http", "$cookies", function($http, $cookies) {
        this.setAvatar = function(files) {
            var url = '/en/accounts/api/profile/',
            fd = new FormData(),
            config = {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken,
                    'Content-Type': undefined
                },
                'withCredentials': true,
                'transformRequest': angular.identity
            };
            fd.append('avatar', files[0]);
            $http.patch(url, fd, config).success(function(data) {
                $('.user-avatar-hex2').css(
                    'background-image', 'url(' + data.avatar + ')');
            }).error(function(data) {
                // TODO: handle image upload errors
            });
        };
    }]
);

angular.module('Sportomatics').service('tags', ["$q", "$filter", function($q, $filter) {
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
}]);

angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.data = {};
    $scope.params = $location.search();
    $scope.setType = function(type) {
      $location.search('type', type || null);
      $scope.params = $location.search();
    };
    if ($scope.params.season) {
      $('[name="season"]').attr('value', $scope.params.season);
    }
    $scope.setSeason = function(e) {
      $location.search('season', $(e).val());
      $scope.params = $location.search();
      $scope.list();
    };
    $scope.getCalendar = function(year, month) {
      var cell, date, day, daysInM, i, j, k, result, row, startDoW;
      daysInM = new Date(year, month + 1, 0).getDate();
      startDoW = new Date(year, month, 1).getDay() - 1;
      if (startDoW < 0) {
        startDoW = 6;
      }
      result = [];
      i = 0;
      row = [];
      while (i * 7 < daysInM + startDoW && i <= 6) {
        row = [];
        for (j = k = 0; k < 7; j = ++k) {
          cell = i * 7 + j;
          day = cell - startDoW + 1;
          date = null;
          if ((1 <= day && day <= daysInM)) {
            date = new Date(year, month, day);
          }
          row.push({
            'cell': cell,
            'date': date
          });
        }
        result.push(row);
        i += 1;
      }
      return result;
    };
    $scope.list = function() {
      var params;
      params = '';
      $scope.calendar = $scope.getCalendar(2015, 0);
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        $scope.data = data;
        return $scope.loaded = true;
      });
    };
  }
]);

angular.module('Sportomatics')
.controller('ClubListController', [
    '$http', '$scope', '$location', 'PlayersSearchService',
    function($http, $scope, $location, PlayersSearchService) {
    var url = $('#ClubListForm').attr('action');

    $scope.$location = $location;
    $scope.PlayersSearchService = PlayersSearchService;

    $scope.countries = {};
    $scope.sparams = {}

    $scope.params = $location.search()

    if ($scope.params.season) {
        $('[name="season"]').attr('value', $scope.params.season);
    }

    $scope.setSeason = function(e) {
        // $(e).attr('value', $(e).val());
        $location.search('season', $(e).val());
        $scope.params = $location.search();
        $scope.list();
    };

    $scope.setOrderBy = function(order_by) {
        if ($scope.loaded) {
            if ($scope.params.order_by === order_by ||
                    (!$scope.params.order_by && !order_by)) { // same field -> reverse
                if ($scope.params.reversed === 'true') {
                    $scope.$location.search('reversed', null);
                } else {
                    $scope.$location.search('reversed', 'true');
                }
            } else { // other field -> reset
                $scope.$location.search('reversed', null);
            }
            $scope.$location.search('order_by', order_by);
            $scope.list($scope);
        }
    };

    $scope.setCountry = function(country) {
        if ($scope.params.country != country) {
            $location.search('country', country);
            $scope.params = $location.search();
            $scope.list();
        }
    };

    $scope.setLeague = function(league) {
        if ($scope.params.league != league) {
            $location.search('league', league);
            $scope.params = $location.search();
            $scope.list();
        }
    };

    $scope.list = function(all) {
        var params = $('#ClubListForm').serialize();

        params += '&order_by=' + ($scope.params.order_by || '%s_title');
        if ($scope.params.reversed) {
            params += '&reversed=true';
        }

        // if ($scope.sparams.leaguesSelected) {
        //     $location.search('league', $scope.sparams.leaguesSelected);
        // } else {
        //     $location.search('league', null);
        // }
        // if ($scope.sparams.contriesSelected) {
        //     $location.search('country', $scope.sparams.countriesSelected);
        // } else {
        //     $location.search('country', null);
        // }

        if ($scope.params.league) {
            params += '&league=' + $scope.params.league;
        }
        if ($scope.params.country) {
            params += '&country=' + $scope.params.country;
        }

        $scope.params = $location.search();
        $scope.data = {};
        $scope.loaded = false;
        $http.get(url + '?' + params)
            .success(function(data) {
                $scope.data = data;
                $scope.loaded = true;
            });
    };

    $scope.next = function(isAll) {
        var url = $scope.data.next;
        if (isAll) {
            url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count);
        }
        $scope.loaded = false;
        $http.get(url).success(function(data) {
            if (isAll) {
                $scope.data = data;
            } else {
                $scope.data.next = data.next;
                $scope.data.results = $scope.data.results.concat(data.results);
            }
            $scope.loaded = true;
        });
    };

    PlayersSearchService.loadCountries($scope, $location, $scope.list);
}]);

angular.module('Sportomatics')
    .controller('ClubNewsController', ["$scope", "$http", "ChartFactory", "LocaleFactory", "$timeout", function($scope, $http, ChartFactory, LocaleFactory, $timeout){
        $scope.club = $("#team-name-hidden").length ? $("#team-name-hidden").val() : 'Club';
        $scope.data = [
            {
                date: '2001',
                values: 17
            },
            {
                date: '2002',
                values: 14
            },
            {
                date: '2003',
                values: 12
            },
            {
                date: '2004',
                values: 10
            },
            {
                date: '2005',
                values: 12
            },
            {
                date: '2006',
                values: 8
            },
            {
                date: '2007',
                values: 12
            },
            {
                date: '2008',
                values: 6
            },
            {
                date: '2009',
                values: 4
            }
        ];
        $scope.matchData = [
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            },
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 2,
                resultNote: 'Б'
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 6,
                resultOpponent: 1
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 5,
                resultOpponent: 4
            },
            {
                date: '21.09.2014',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 3,
                resultOpponent: 3
            },
            {
                date: '14.01.2013',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 5,
                resultOpponent: 2
            },
            {
                date: '04.07.2012',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 4,
                resultOpponent: 1
            },
            {
                date: '30.11.2000',
                club: $scope.club,
                opponent: 'СКА',
                resultClub: 1,
                resultOpponent: 4
            }
        ];

        $scope.setCurrentSeasonString = function(date, value){
            $timeout(function(){

                $scope.currentSeason = date;
                $scope.currentPlace = value;
                $scope.currentSeasonString = parseInt($scope.currentSeason)-1 + '/' + $scope.currentSeason;
            }, 100)
        };
        $scope.setCurrentSeasonString(2001, 17);

        $scope.makeGraph = function(id, title, color, field, valueAxis, localeObject){
            console.log(id, title, color, field);
            var graph = new AmCharts.AmGraph();
            graph.id = "gl"+id;
            graph.valueAxis = valueAxis; // we have to indicate which value axis should be used
            graph.title = title + ' ' + field;
            graph.valueField = "values"+id;
            graph.bullet = "none";
            graph.hideBulletsCount = 30;
            graph.bulletBorderThickness = 1;
            graph.lineColor = color;
            graph.fillColor = "#FFFFFF";
            graph.fillAlphas = 0;
            graph.lineThickness = 1;
            graph.type = 'line';
            return graph;
        };


        $scope.graph = $scope.makeGraph('', 'positions', "#408e3a", null, null, LocaleFactory.locale_ru);
        $scope.graphs = [$scope.graph];
        ChartFactory.generateSerialLineChart('position', $scope.data, LocaleFactory.locale_ru, $scope.graphs).then(function(chart){
            chart.addListener("rendered", addListeners);

            function addListeners(){
                var categoryAxis = chart.categoryAxis;
                categoryAxis.addListener("clickItem", handleClick);
                categoryAxis.addListener("rollOverItem", handleOver);
                categoryAxis.addListener("rollOutItem", handleOut);
            }

            function handleClick(event){
                var value = _.where($scope.data, {date: event.value.toString()})[0].values;
                console.log(event.value, value);
                $scope.setCurrentSeasonString(event.value, value);
            }

            function handleOut(event){
                event.target.setAttr("cursor", "default");
                event.target.setAttr("fill", "#000000");
            }


            function handleOver(event){
                event.target.setAttr("cursor", "pointer");
                event.target.setAttr("fill", "#CC0000");
            }

            chart.write("chartdiv");

        })
    }])
angular.module('Sportomatics')
.controller('ClubStatsController', [
    '$http', '$scope', 'PlayersSearchService', '$location',
    function($http, $scope, PlayersSearchService, $location) {

    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;

    $scope.data = {};
    $scope.loader = false;

    $location.search('club', +$('[name="club"]').val());
    $scope.params = $location.search();

    $scope.sparams = {
        countriesSelected: [],
        leaguesSelected: [],
        leaguesSelectedLoaded: false
    };

    $scope.PlayerPartnersPopup = {
        data: null,
        isClubsVisible: false
    };

    $scope.PlayerPartnersPopupShow = function(e, event) {
        var popup = $('.player-partners-popup:hidden'),
        url = $('#PlayerCardLink').attr('href');
        if (popup.length) {
            $scope.PlayerPartnersPopup.data = null;
            $http.get(url.replace(0, this.player.pk))
            .success(function(data) {
                $scope.PlayerPartnersPopup.data = data;
            });
            $('.player-partners-popup:hidden').show(500).offset({
                left: event.pageX,
                top: event.pageY
            });
        }
    };

    $scope.setPlayersFilter = function(obj) {
        PlayersSearchService.setPlayersFilter($scope, obj);
    };

    PlayersSearchService.search($scope);
}]);

angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope',
    function($http, $scope) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        popup = null;

        $scope.PlayerPartnersPopup = {
            data: null,
            isClubsVisible: true
        };
        $scope.PlayerPartnersPopupShow = function(e, event) {
            var popup = $('.player-partners-popup:hidden'),
            url = $('#PlayerCardLink').attr('href'),
            pk;
            if (popup.length && this.cell_id[0] !== 'trainer') {
                pk = self.getCell(self.players, this.cell_id).pk;
                $scope.PlayerPartnersPopup.data = null;
                $http.get(url.replace(0, pk))
                .success(function(data) {
                    $scope.PlayerPartnersPopup.data = data;
                });
                $('.player-partners-popup:hidden').show(500).offset({
                    left: event.pageX,
                    top: event.pageY
                });
            }
        };

        self.PLAYERS_TABLE = [ // table indexes, null is an empty filler
            // row 1
            [['defender', 0], ['defender', null], ['defender', 1], ['defender', null],
             ['defender', 2], ['defender', null], ['defender', 3],
             ['forward', null], ['forward', 0], ['forward', null],
             ['goalkeeper', 0]],
            // row 2
            [['defender', null], ['defender', 4], ['defender', null],
             ['forward', 1], ['forward', null], ['forward', 2], ['forward', null],
             ['forward', 3], ['forward', null], ['forward', 4],
             ['goalkeeper', null]],
            // row 3
            [['defender', 5], ['defender', null], ['defender', 6],
             ['forward', null], ['forward', 5], ['forward', null], ['forward', 6],
             ['forward', null], ['forward', 7], ['forward', null],
             ['goalkeeper', 1]],
            // row 4
            [['defender', null], ['defender', 7], ['defender', null],
             ['forward', 8], ['forward', null], ['forward', 9], ['forward', null],
             ['forward', 10], ['forward', null], ['forward', 11],
             ['goalkeeper', null]],
            // row 5
            [['defender', 8], ['defender', null], ['defender', 9],
             ['forward', null], ['forward', 12], ['forward', null], ['forward', 13],
             ['forward', null], ['forward', 14], ['forward', null],
             ['goalkeeper', 2]],
            // row 6
            [['defender', null], ['defender', 10], ['defender', null],
             ['forward', 15], ['forward', null], ['forward', 16], ['forward', null],
             ['forward', 17], ['forward', null], ['forward', 18],
             ['goalkeeper', null]],
            // row 7
            [['defender', 11], ['defender', null], ['defender', 12],
             ['forward', null], ['forward', 19], ['forward', null], ['forward', 20],
             ['forward', null], ['forward', 21], ['forward', null],
             ['goalkeeper', 3]],
            // row 8
            [['defender', null], ['defender', 13], ['defender', null],
             ['forward', 22], ['forward', null], ['forward', 23], ['forward', null],
             ['forward', 24], ['forward', null], ['forward', 25],
             ['goalkeeper', null]],
            // row 9
            [['defender', 13], ['defender', null], ['defender', 14],
             ['trainer', null], ['trainer', 0], ['trainer', null], ['trainer', 1],
             ['trainer', null], ['trainer', 2], ['trainer', null],
             ['goalkeeper', 4]],
            // row 10
            [['defender', null], ['defender', 15], ['defender', null],
             ['trainer', 3], ['trainer', null], ['trainer', 4], ['trainer', null],
             ['trainer', 5], ['trainer', null], ['trainer', 6],
             ['goalkeeper', null]],
        ];

        self.CLUBS_TABLE = [ // table indexes, null is an empty filler
            // row 1
            [['club', 0], ['club', null], ['club', 1], ['club', null],
             ['club', 2], ['club', null], ['club', 3], ['club', null],
             ['club', 4], ['club', null], ['club', 5]],
            // row 1
            [['club', null], ['club', 6], ['club', null], ['club', 7],
             ['club', null], ['club', 8], ['club', null], ['club', 9],
             ['club', null], ['club', 10],  ['club', null]],
            // row 3
            [['club', 11], ['club', null], ['club', 12], ['club', null],
             ['club', 13], ['club', null], ['club', 14], ['club', null],
             ['club', 15], ['club', null], ['club', 16]],
            // row 4
            [['club', null], ['club', 17], ['club', null], ['club', 18],
             ['club', null], ['club', 19], ['club', null], ['club', 20],
             ['club', null], ['club', 21],  ['club', null]],
            // row 5
            [['club', 22], ['club', null], ['club', 23], ['club', null],
             ['club', 24], ['club', null], ['club', 25], ['club', null],
             ['club', 26], ['club', null], ['club', 27]],
            // row 6
            [['club', null], ['club', 28], ['club', null], ['club', 29],
             ['club', null], ['club', 30], ['club', null], ['club', 31],
             ['club', null], ['club', 32],  ['club', null]]
        ];

        self.players = {};
        self.clubs = {
            'getLastClub': function() {
                if (this.clubs.length) {
                    return this.clubs[this.clubs.length - 1];
                }
            },
            'clubs': []
        };

        $scope.setSeason = function(e) {
            self.list(self.compare);
        };

        self.getCell = function(table, cell_id) {
            var group;
            if (table.table && cell_id && Array.isArray(cell_id) && cell_id[1] !== null) {
                group = table.table[cell_id[0]];
                if (group) {
                    return group[cell_id[1]];
                }
            }
        };

        self.isPersonVisible = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            if (cell) {
                switch (self.players.status) {
                    default:
                        return true;
                    case 'joined':
                        return cell.is_joined;
                    case 'left':
                        return cell.is_left;
                    case 'legionnaire':
                        return cell.is_legionnaire;
                }
            } else {
                return false;
            }
        };
        self.isPersonInCell = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            if (cell) {
                return true;
            } else {
                return false;
            }
        };

        self.list = function(callback) {
            var params = $('#ClubTeamForm').serialize();
            self.players.data = null;
            self.players.table = null;
            self.players.loader = true;
            self.clubs.clubs = [];
            $http.get(url + '?' + params)
            .success(function(data) {
                self.players.data = data;
                self.players.table = {
                    'goalkeeper': data.goalkeeper_players,
                    'defender': data.defender_players,
                    'forward': data.offender_players,
                    'trainer': data.coaches
                }
                self.players.loader = false;
                if (typeof callback === 'function') {
                    callback();
                }
            });
        };

        this.compare = function() {
            var url = $('#ClubTeamCompareLink').attr('href'),
            club = self.clubs.getLastClub(),
            params, leagues;
            if (club) {
                params = 'source_season=' + club.data.season.pk +
                    '&season=' + club.data.prev_season.pk;
            } else {
                params = 'source_season=' + self.players.data.season.pk +
                    '&season=' + self.players.data.prev_season.pk;
            }
            self.clubs.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                if (data.leagues.length) {
                    self.clubs.clubs.push({
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs,
                        },
                        'league': data.leagues[0]
                    });
                }
                self.clubs.loader = false;
            });
        };

        this.list(this.compare);
    }
]);

angular.module('Sportomatics')
.controller('MetricsCompareController', ['$http', '$scope', function($http, $scope) {
    this.graph_type = 'linear';
    this.data = {};
    this.setGraphType = function(type) {
        this.graph_type = type;
    };
}])
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
angular.module('Sportomatics')
.controller('NewsListController', [
    '$http', '$scope', '$location',
    function($http, $scope, $location) {
    var url = $('#NewsListLink').attr('href');

    $scope.columns = [0, 1, 2, 3, 4];
    $scope.limit = 50;

    $scope.getColumn = function(data, limit, column) {
        var result = [], i = 0, b = 0;
        if (data && data.length) {
            for (i = 0; i < data.length && i < limit; i += 50) {
                b = i + column * 10;
                result = result.concat(data.slice(b, b + 10));
            }
        };
        return result;
    };

    $scope.list = function($scope) {
        var params = '';
        if ($location.search().date) {
            params += 'date=' + $location.search().date;
        }
        $http.get(url + '?' + params).success(function(data) {
            $scope.data = data;
            $scope.loaded = true;
        });
    };

    // $scope.next = function($scope) {
    //     var url = $scope.data.next;
    //     $scope.loaded = false;
    //     $http.get(url).success(function(data) {
    //         $scope.data.next = data.next;
    //         $scope.data.results = $scope.data.results.concat(data.results);
    //         $scope.loaded = true;
    //     });
    // };

    $scope.hasNext = function() {
        return $scope.limit < $scope.data.length;
    };

    $scope.next = function() {
        $scope.limit += 50;
    };

    $scope.list($scope);
}]);

angular.module('Sportomatics')
    .config(['$resourceProvider', function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
.factory('ClubInstaPhoto', ["$resource", function($resource){
    return $resource("/ru/api/hockey/clubinstaphoto/"+":id/", {}, {
        query: {method:'GET', params:{processed: 1, id: null}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
}])
.factory('PlayerInstaPhoto', ["$resource", function($resource){
    return $resource("/ru/api/hockey/playerinstaphoto/", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
}])
.factory('ArenaInstaPhoto', ["$resource", function($resource){
    return $resource("/ru/api/hockey/processedarenainstaphoto/", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
}])
.factory('InstagramUser', ["$resource", function($resource){
    return $resource("/ru/api/base/instagram_user/"+":id/", {}, {
        query: {method:'GET', params:{id:null}, isArray:true},
        get: { method: 'GET'}
    });
}])
.controller('PhotosController', ["$scope", "ClubInstaPhoto", "InstagramUser", "PlayerInstaPhoto", "ArenaInstaPhoto", "$resource", "$timeout", "$location", function($scope, ClubInstaPhoto, InstagramUser,PlayerInstaPhoto,ArenaInstaPhoto, $resource, $timeout, $location){

        var playerClubsMasonry = $('.masonry-clubs-photos');
        var closePopupBtn = $('#close-popup-btn');


        closePopupBtn.on('click', function(e) {
            e.preventDefault();
            $(this).parent().hide();
            $scope.clearPopupFields();
            $('.overlay-black').css('visibility', 'hidden');
            $scope.selectedClub = null;
        });
        $('.overlay-black').on('click', function(event){
            $('.photo-popup').hide();
            $('.overlay-black').css('visibility', 'hidden');
        });

        $scope.club_id = $('#team-id').val();
        $scope.player_id = $('#player-id').val();
        $scope.arena_id = (document.URL.indexOf('photos') > -1) ? null : $('#team-arena-id').val();
        $scope.photosSlider = [];
        $scope.photosChunk = [];
        console.log()

        $scope.photos = [];
        $scope.next_page = 1;
        $scope.currentIndex = 0;

        $scope.getPage = function(){
            var get_params = {
                page: $scope.next_page,
                min_id: 0,
                max_id: 10000000,
                club: $scope.club_id,
                player: $scope.player_id,
                arena: $scope.arena_id
            };
            $scope.photoDataLoader = true;
            if($scope.arena_id){
                get_params = {
                    page: $scope.next_page,
                    min_id: 0,
                    max_id: 10000000,
                    arena: $scope.arena_id
                };
                ArenaInstaPhoto.query(get_params).$promise.then(function (data) {
                    $scope.photoDataLoader = false;
                    $.each(data.results, function (index, value) {
                        value.created = new Date(value.photo.created).instagramDateFormat();
                        $scope.photos.push(value);
                        if($scope.photosChunk.length < 5){
                            $scope.photosChunk.push(value);
                        }
                        if($scope.photosChunk.length === 5 || index === data.results.length - 1){
                            $scope.photosSlider.push($scope.photosChunk);
                            $scope.photosChunk = [];
                        }
                    });
                    setTimeout(function(){
                        $('.photo-square').hover(function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '1');
                        }, function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '0');
                        });
                    }, 100);
                    $scope.next_page = data.next_page;
                    if (!$scope.next_page && $('#nextpagebutton').length) {
                        $('#nextpagebutton').remove();
                    }
                });
            } else if( $scope.club_id){
                ClubInstaPhoto.query(get_params).$promise.then(function (data) {
                    $scope.photoDataLoader = false;
                    $.each(data.results, function (index, value) {
                        value.created = new Date(value.photo.created).instagramDateFormat();
                        $scope.photos.push(value);
                        if($scope.photosChunk.length < 5){
                            $scope.photosChunk.push(value);
                        }
                        if($scope.photosChunk.length === 5 || index === data.results.length - 1){
                            $scope.photosSlider.push($scope.photosChunk);
                            $scope.photosChunk = [];
                        }
                    });
                    setTimeout(function(){
                        $('.photo-square').hover(function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '1');
                        }, function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '0');
                        });
                    }, 100);
                    $scope.next_page = data.next_page;
                    if (!$scope.next_page && $('#nextpagebutton').length) {
                        $('#nextpagebutton').remove();
                    }
                });
            } else if ($scope.player_id){
                PlayerInstaPhoto.query(get_params).$promise.then(function (data) {
                    $scope.photoDataLoader = false;
                    $.each(data.results, function (index, value) {
                        value.created = new Date(value.photo.created).instagramDateFormat();
                        $scope.photos.push(value)
                        if($scope.photosChunk.length < 5){
                            $scope.photosChunk.push(value);
                        }
                        if($scope.photosChunk.length === 5 || index === data.results.length - 1){
                            $scope.photosSlider.push($scope.photosChunk);
                            $scope.photosChunk = [];
                        }
                    });
                    setTimeout(function(){
                        $('.photo-square').hover(function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '1');
                        }, function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '0');
                        });
                    }, 100);
                    $scope.next_page = data.next_page;
                    if (!$scope.next_page && $('#nextpagebutton').length) {
                        $('#nextpagebutton').remove();
                    }
                }, function(){
                    $scope.photoDataLoader = false;
                });
            }
        };

        $scope.nextPage = function(){
            if($scope.next_page) {
                $scope.getPage();
            }
        };

        $scope.PhotoPopup = {
            data: null,
            index: null
        };

        $scope.PhotoPopupShow = function(id, index, event, position){
            console.log(index);
            $scope.currentIndex = index;
            var photo = $scope.photos[index];
            $scope.PhotoPopup.data = $scope.photos[index];
            $scope.PhotoPopup.instagramUser = InstagramUser.get({id: photo.photo.instagram_user}, function(){});
            $scope.PhotoPopup.comment = photo.photo.comment;
            $(".instagram-comment").val(photo.photo.comment);
            $('.overlay-black').css('visibility', 'visible');
            $('.photo-popup').show();
            $scope.PhotoPopup.index = index;

        };
        $scope.nextPhoto = function(){
            var index = $scope.PhotoPopup.index + 1;
            $scope.currentIndex++;
            if($scope.photos[index]){
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'next');
            }
        };
        $scope.prevPhoto = function(){
            var index = $scope.PhotoPopup.index - 1;
            if($scope.photos[index]){
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'prev');
            }
        };

        $scope.getPage();

        Date.prototype.instagramDateFormat = function(){
            var monthsRu = ["января", "февраля", "марта", "апреля", "мая","июня","июля", "августа", "сентября", "октября", "ноября", "декабря"];
            return this.getDate() + ' ' + monthsRu[this.getMonth()] + ' ' + this.getFullYear();
        }
}])
    angular.module('Sportomatics')
        .controller('PlayerCardIndicatorsController', ["$http", "$scope", "$timeout", "AmChartsFactory", "ChartFactory", "zoomData", "LocaleFactory", "$state", "$location", "$q", function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q) {
            //http://www.amcharts.com/lib/images/
            $scope.disabled = false;
            var self = this,
                url = $('#IndicatorsLink').attr('href');
            this.url = $('#IndicatorsLink').attr('href');
            this.indicatorsType = 'graph';
            this.field = $location.search()['field'] || 'count';
            this.fieldName = LocaleFactory.getFieldName(this.field);
            this.club = parseInt($location.search()['club']) || null;
            this.coach = parseInt($location.search()['coach']) || null;
            this.groupBy = 'season';
            this.data = [];
            this.graphData = {};
            this.chartsCount = 0;
            this.playerId = $('#player-id').val();
            $scope.activeSeason = -1;
            $scope.playersStats = [];

            this.setIndicatorsType = function(type) {
                this.indicatorsType = type;
                if(type === 'graph') {
                    $timeout(function(){
                        //self.list();
                    }, 100);
                }
                else {
                    this.data = (this.groupBy === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
                }
            };

            this.setField = function(field) {
                this.field = field;
                this.fieldName = LocaleFactory.getFieldName(field, self.locale);
                $location.search('field', field);
                this.list(true);
            };

            this.setClub = function(club) {
                this.club = club;
                $location.search('club', club);
                $scope.getClubData(true);
            };

            this.setCoach = function(coach) {
                this.coach = coach;
                $location.search('coach', coach);
                $scope.getCoachData(true);
            };
            this.setGraphResults = function(results) {

            };
            $scope.animateAgain = function(){
                $scope.chart.animateAgain();
            };
            //var chart = null;
            $scope.removeGraph = function(player){
                if(contains($scope.playersStats, 'id', (parseInt(player.id)).toString())){
                    $scope.playersStats = _.without($scope.playersStats, _.findWhere($scope.playersStats, {id: (parseInt(player.id)).toString()}));
                    $scope.makeChart($scope.activeSeason > -1);
                }
            };
            $scope.disableGraph = function(player){
                console.log( $('.amcharts-legend-item-gl'+player.id).length)
                $('.amcharts-legend-item-gl'+player.id).trigger("click");
                console.log($('.amcharts-legend-item-gl'+player.id)[0]);
            };
            $scope.addGraph = function(url, local){
                //TODO: make production version
                var players = [
                    {
                        title: 'Горохов Илья',
                        color: "#FF3232",
                        id: '1',
                        link: '/static/json/gorohov'
                    },
                    {
                        title: 'Сергей Соин',
                        color: "#3232FF",
                        id: '2',
                        link: '/static/json/soin'
                    }
                ];
                if(contains($scope.playersStats, 'id', (parseInt(local)+1).toString())){
                    $scope.playersStats = _.without($scope.playersStats, _.findWhere($scope.playersStats, {id: (parseInt(local)+1).toString()}));
                    return $scope.makeChart($scope.activeSeason > -1);
                }
                var playerObject = players[local];
                url = playerObject.link;
                var localUrlMonths = url + '_months.json';
                var localUrlSeasons = url + '_seasons.json';
                    self.loader = true;
                    $http.get(localUrlMonths)
                        .success(function(data){
                            playerObject.dataByMonth = data;
                        }).then(function(){
                            $http.get(localUrlSeasons)
                                .success(function(data){
                                    playerObject.dataBySeason = data;
                                    self.loader = false;
                                }).then(function(){
                                    $scope.playersStats.push(playerObject);
                                    /*var data = (self.groupBy === 'month') ?  playerObject.dataByMonth : playerObject.dataBySeason;
                                    var newChartData = populateChartData($scope.chart, $scope.chartData, data.results, self.field, $scope.localeObject, playerObject);
                                    var newGraph = makeGraph(playerObject.id, playerObject.title, playerObject.color, self.field, $scope.chart.valueAxes[0], $scope.localeObject);
                                    //var newChartDataByMonth = populateChartData($scope.chart, $scope.chartData, newPlayer.dataByMonth.results, self.field, $scope.localeObject, playerObject);
                                    //var newChartDataBySeason = populateChartData($scope.chart, $scope.chartData, newPlayer.dataBySeason.results, self.field, $scope.localeObject, playerObject);
                                    $scope.latestData = newChartData.data;
                                    $scope.chart.dataProvider = newChartData.data;
                                    $scope.chart.addGraph(newGraph);
                                    //$scope.chart.validateData();
                                    $scope.chart.write("chartdiv");*/
                                    $scope.makeChart($scope.activeSeason > -1);
                                })
                        })
            };

            $scope.makeChart = function(switched){
                var initialData = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var initialGraph = makeGraph('', $scope.playerObject.title, $scope.playerObject.color, self.field, null, $scope.localeObject);
                var initialChartData = generateChartData(initialData.results, self.field, self.groupBy);
                var newChartGraphs = [initialGraph];
                var newChartData = {};
                _.each($scope.playersStats, function(player, index) {
                    var data = (self.groupBy === 'month') ? player.dataByMonth : player.dataBySeason;
                    newChartData = populateChartData($scope.chart, initialChartData, data.results, self.field, $scope.localeObject, player);
                    var newChartGraph = makeGraph(player.id, player.title, player.color, self.field, null, $scope.localeObject);
                    newChartGraphs.push(newChartGraph);
                });
                if(switched){
                    if(!$scope.playersStats.length) newChartData.data = initialData.results;
                    var datesArray = newChartData.data.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                if(!$scope.playersStats.length) newChartData = initialChartData;
                //TODO: seasons for all players
                ChartFactory.generateSerialChart(self.field, newChartData, $scope.localeObject, newChartGraphs).then(function(chart){
                    $scope.chart = chart;
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
                });
            };

            $scope.isDisabled = function(season){
                return (self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 );
            };
            $scope.setGroupBy = function(groupby){
                self.groupBy = groupby;
                self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
                $scope.onSeason = false;
                self.list();
                $scope.activeSeason = -1;
                $timeout(function(){}, 500);
            };
            $scope.moveToSeason = function(season, index){
                if((self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
                zoomData.startDate = season.start_date;
                zoomData.endDate = season.end_date;
                $scope.onSeason = true;
                self.groupBy = 'month';
                self.data = $scope.dataByMonth;
                self.list(true);
                $scope.activeSeason = index;
            };
            this.list = function(switched) {
                var data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                var datesArray = (self.groupBy === 'month') ? data.results.map(function(e){ return new Date(e['date']) }) : data.results.map(function(e){ return new Date(e['season']['end_date']) });
                var min = Math.min.apply(null, datesArray);
                var max = Math.max.apply(null, datesArray);
                if(switched){
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                $scope.chartData = generateChartData(data.results, self.field, self.groupBy);
                ChartFactory.generateSerialChart(self.field, $scope.chartData, $scope.localeObject).then(function(chart){
                    $scope.chart = chart;
                    // WRITE
                    if(self.coach){
                        $scope.chart.guides = [];
                        _.each($scope.coachData.results, function(result){
                            var seasonEnd = new Date(result.season.end_date);
                            var prevSeasonEndString = (parseInt(result.season.end_date.substr(0,4))-1).toString() + result.season.end_date.substr(4);
                            var prevSeasonEnd = new Date(prevSeasonEndString);
                            $scope.chart.guides.push({
                                "fillAlpha" : 0.3,
                                "date" : (prevSeasonEnd.getTime() >= min) ? prevSeasonEnd : new Date(min),
                                "toDate": seasonEnd,
                                "fillColor" : "#3498db",
                                "lineThickness": 0
                            });
                        })
                    }
                    if(self.club){
                        $scope.chart.guides = [];
                        _.each($scope.clubData.results, function(result){
                            var seasonEnd = new Date(result.season.end_date);
                            var prevSeasonEndString = (parseInt(result.season.end_date.substr(0,4))-1).toString() + result.season.end_date.substr(4);
                            var prevSeasonEnd = new Date(prevSeasonEndString);
                            $scope.chart.guides.push({
                                "fillAlpha" : 0.3,
                                "date" : (prevSeasonEnd.getTime() >= min) ? prevSeasonEnd : new Date(min),
                                "toDate": seasonEnd,
                                "fillColor" : "#3498db"
                            });
                        })
                    }
                    $scope.chart.categoryAxis.minPeriod = (self.groupBy === 'month') ? 'MM' : 'YYYY';
                    if ($scope.playersStats.length > 0) return $scope.makeChart(switched);
                    if($scope.disabled){
                        $scope.chart.chartCursor = null;
                        $scope.chart.chartScrollbar = null;
                        $scope.chart.startDuration = null;
                        for(var i = 0; i < $scope.chart.graphs.length; i ++){
                            $scope.chart.graphs[i].balloonText = '';
                            $scope.chart.graphs[i].visibleInLegend = false;
                        }

                    }
                    $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));}));
                    $scope.createRadar([self.playerId], $scope.lastSeason).then(function(){
                        //$scope.createRadar(['1634']);
                    });
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
                });
            };
            $scope.getPlayerData = function(){
                $scope.playerObject = {
                    id: $('#player-id').val(),
                    title: 'Player' + $('#player-id').val(),
                    color: "#408e3a"
                };
                var group = 'month';
                var params = 'group_by=' + group;
                self.loader = true;
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        self.locale = headers()['content-language'];
                        $scope.localeObject = LocaleFactory['locale_'+self.locale];
                        self.fieldName = $scope.localeObject.fieldNames[self.field].fullName;
                        $scope.dataByMonth = data;
                        $scope.playerObject.dataByMonth = data;
                        group = 'season';
                        params = 'group_by=' + group;
                        $http.get(url + '?' + params)
                            .success(function(data, status, headers) {
                                $scope.dataBySeason = data;
                                $scope.playerObject.dataBySeason = data;
                                self.data = data; //for table view
                                self.loader = false;
                            }).then(function(){
                                //$scope.playersStats.push(playerObject);
                                self.list();
                            })
                    })
            };
            $scope.getCoachData = function(){
                var group = 'season';
                var params = 'group_by=' + group;
                if (self.coach !== null) {
                    params += '&coach=' + self.coach;
                    $http.get(url + '?' + params)
                        .success(function(data, status, headers) {
                            $scope.coachData = data;
                        }).then(function(){
                            self.list();
                        })
                }
            };
            $scope.getClubData = function(toList){
                var group = 'season';
                var params = 'group_by=' + group;
                if (self.club !== null) {
                    params += '&club=' + self.club;
                    $http.get(url + '?' + params)
                        .success(function(data, status, headers) {
                            $scope.clubData = data;
                        }).then(function(){
                            self.list();
                        })
                }
            };


            $scope.createRadar = function(players, season, sum){
                $scope.playersInRadarChart = [];
                $scope.playersRadarChartData = [{
                    field: 'goals'
                },{
                    field: 'points'
                }, {
                    field: 'assists'
                },{
                    field: 'plus_minus'
                }];
                $scope.playersRadarChartGraphs = [];
                var deferred = $q.defer();
                if(players.length > 1){
                    if(sum){
                        var playersRequestArray = [];
                        _.each(players, function(player){
                            var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                            playersRequestArray.push($http.get(url));
                        });
                        $q.all(playersRequestArray).then(function(results) {
                            console.log('results');
                            console.log(results);

                            _.each(results, function(result){
                                var playerSeasonsDataResults = result.data.results;
                                var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                                _.each($scope.playersRadarChartData, function(radarChartDataCategory, index){
                                    if(radarChartDataCategory['value']){
                                        radarChartDataCategory['value'] += playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                    }
                                    else {
                                        radarChartDataCategory['value'] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                    }
                                });
                                $scope.playersInRadarChart.push({
                                    player: player,
                                    playerData: playerDataInSeason
                                });
                            });
                            _.each($scope.playersRadarChartData, function(radarChartDataCategory, index){
                                console.log(radarChartDataCategory)
                                radarChartDataCategory['value'] = radarChartDataCategory['value'] / $scope.playersInRadarChart.length;
                                console.log(radarChartDataCategory)
                            });
                            var graph = new AmCharts.AmGraph();
                            graph.valueField = "value";
                            graph.bullet = "round";
                            graph.balloonText = "team [[value]]";
                            $scope.playersRadarChartGraphs.push(graph);
                            ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                                $scope.chartRadar = chart;
                                $scope.chartRadar.write('chartdiv2');
                                deferred.resolve(true);
                            })
                        });


                    } else {
                        _.each(players, function(player){
                            var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                            $http.get(url)
                                .success(function(playerSeasonsData){
                                    var playerSeasonsDataResults = playerSeasonsData.results;
                                    var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                                    if(playerDataInSeason){
                                        _.each($scope.playersRadarChartData, function(radarChartDataCategory){
                                            radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'] ;
                                        });
                                        var graph = new AmCharts.AmGraph();
                                        graph.valueField = "value" + player;
                                        graph.bullet = "round";
                                        graph.balloonText = "player " + player + " [[value]]";
                                        $scope.playersInRadarChart.push({
                                            player: player,
                                            playerData: playerDataInSeason
                                        });
                                        $scope.playersRadarChartGraphs.push(graph);
                                    }
                                }).then(function(){
                                    ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                                        $scope.chartRadar = chart;
                                        $scope.chartRadar.write('chartdiv2');
                                        deferred.resolve(true);
                                    })
                                });
                        })
                    }
                } else {
                    var player = players[0];
                    var url = 'http://127.0.0.1:8000/ru/hockey/api/players/'+ player + '/indicators/?group_by=season';
                    $http.get(url)
                        .success(function(playerSeasonsData){
                            var playerSeasonsDataResults = playerSeasonsData.results;
                            var playerDataIn2013 = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                            console.log(playerDataIn2013);
                            _.each($scope.playersRadarChartData, function(radarChartDataCategory){
                                radarChartDataCategory['value' + player] = playerDataIn2013[radarChartDataCategory.field] / playerDataIn2013['count'] ;
                            });
                            var graph = new AmCharts.AmGraph();
                            graph.valueField = "value" + player;
                            graph.bullet = "round";
                            graph.balloonText = "player " + player + " [[value]]";
                            $scope.playersInRadarChart.push({
                                player: player,
                                playerData: playerDataIn2013
                            });
                            $scope.playersRadarChartGraphs.push(graph);
                        }).then(function(){
                            ChartFactory.generateRadarChart($scope.playersRadarChartData, $scope.playersRadarChartGraphs).then(function(chart){
                                $scope.chartRadar = chart;
                                $scope.chartRadar.write('chartdiv2');
                                deferred.resolve(true);
                            })
                        });
                }
                return deferred.promise;
            };
            $scope.generateRadarChart = function(){
                var players = [
                    {
                        title: 'Горохов Илья',
                        color: "#FF3232",
                        id: '1',
                        link: '/static/json/gorohov'
                    },
                    {
                        title: 'Сергей Соин',
                        color: "#3232FF",
                        id: '2',
                        link: '/static/json/soin'
                    }
                ];
                var playerObject = players[1];
                var url = playerObject.link;
                var localUrlMonths = url + '_months.json';
                var localUrlSeasons = url + '_seasons.json';
                $http.get(localUrlMonths)
                    .success(function(data){
                        playerObject.dataByMonth = data;
                    }).then(function(){
                        $http.get(localUrlSeasons)
                            .success(function(data){ //1634
                                playerObject.dataBySeason = data;
                                $scope.soin2013 = playerObject.dataBySeason.results[14];
                                console.log($scope.soin2013);
                                $scope.radarPlayerData2013 = [{
                                    field: 'goals',
                                    value: ($scope.soin2013.goals+$scope.soin2013.ev_goals+$scope.soin2013.es_goals) / $scope.soin2013.count
                                },{
                                    field: 'points',
                                    value: $scope.soin2013.points / $scope.soin2013.count
                                }, {
                                    field: 'assists',
                                    value: $scope.soin2013.assists / $scope.soin2013.count
                                },{
                                    field: 'plus_minus',
                                    value: $scope.soin2013.plus_minus / $scope.soin2013.count
                                }];
                            }).then(function(){
                                $http.get('http://127.0.0.1:8000/ru/hockey/api/players/1634/indicators/?group_by=season')
                                    .success(function(konkov){
                                        console.log(konkov.results[14])
                                        $scope.konkov2013 = konkov.results[14];
                                        _.each($scope.radarPlayerData2013, function(value){
                                            value['value2'] = $scope.konkov2013[value.field] / $scope.konkov2013['count'] ;
                                        })
                                    }).then(function(){
                                        $http.get('http://127.0.0.1:8000/ru/hockey/api/players/1373/indicators/?group_by=season')
                                            .success(function(radulov){
                                                console.log(radulov.results[5])
                                                $scope.radulov2013 = radulov.results[5];
                                                _.each($scope.radarPlayerData2013, function(value){
                                                    value['value3'] = $scope.radulov2013[value.field] / $scope.radulov2013['count'] ;
                                                })
                                            }).then(function(){
                                                ChartFactory.generateRadarChart($scope.radarPlayerData2013).then(function(chart){
                                                    $scope.chartRadar = chart;
                                                    $scope.chartRadar.write('chartdiv2');
                                                })
                                            })
                                    })

                            })
                    })

            };


            $scope.getPlayerData();
            $scope.getCoachData();
            $scope.getClubData();
            //$scope.generateRadarChart();
            $scope.sumRadars = function(){
               // $scope.createRadar(['1373', '1634'], '2013', true).then(function(){
                    //$scope.createRadar(['1634']);
               //})
            };



        }])
        .factory('AmChartsFactory', ["$q", "$rootScope", "$document", function ($q, $rootScope, $document) {
            var deferred = $q.defer();

            AmCharts.ready(function(){
                $rootScope.$apply(deferred.resolve);
            });

            return {
                ready: function () {
                    return deferred.promise;
                }
            };
        }])
        .run(["AmChartsFactory", function (AmChartsFactory) {}]);

    Array.prototype.contains = function(obj) {
        var i = this.length;
        while (i--) {
            if (this[i] === obj) {
                return true;
            }
        }
        return false;
    };
    function generateRadarChartData(){

    }
    function makeRadarGraph(){

    }
    function generateChartData(data, field, groupBy) {
        var chartData = {};
        chartData.groupBy = groupBy;
        chartData.data = [];
        var dates = data.map(function(e){
            if(e['date'] == null){
                return new Date(e['season']['end_date']);
            }
            return new Date(e['date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        for(var i = 0; i< dates.length; i++){
            if(!((field === 'shots' || field === 'pis__avg' || field === 'shots__avg' || field === 'faceoff' || field === 'winfaceoff' || field === 'winfaceoff_p__avg' || field === 'gamingtime__avg' || field === 'change_count__avg')
                && (dates[i].getFullYear() <= 2008)))
                chartData.data.push({
                    date: dates[i],
                    values: values[i],
                    count: count[i],
                    percentage: (field === 'count') ? undefined : (count[i] === 0) ? undefined : Math.round(parseFloat(values[i]/realCount[i])*1000)/1000
                });
        }
        return chartData;
    }
    function populateChartData(chart, initialData, data, field, localeObject, playerObject){
        var chartData = initialData;
        var dates = data.map(function(e){
            if(e['date'] == null){
                return new Date(e['season']['end_date']);
            }
            return new Date(e['date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        _.each(dates, function(date, index){
            if(!((field === 'shots' || field === 'pis__avg' || field === 'shots__avg' || field === 'faceoff' || field === 'winfaceoff' || field === 'winfaceoff_p__avg' || field === 'gamingtime__avg' || field === 'change_count__avg')
                && (date.getFullYear() <= 2008))){
                var dataObject = {};
                dataObject['date'] = date;
                dataObject['values'+playerObject.id] = values[index];
                dataObject['count'+playerObject.id] = count[index];
                dataObject['percentage'+playerObject.id] = (field === 'count') ? undefined : (count[index] === 0) ? undefined : Math.round(parseFloat(values[index]/realCount[index])*1000)/1000;
                chartData.data.push(dataObject);
            }
        });
        var a = _.map(_.toArray(_.groupBy(chartData.data, 'date')), function(e){
            var object = {};
            //if(e.length < 2) return null; //в случае если нужно будет сделать только общие сезоны
            _.each(e, function(dateObject){
                object = mergeJSON(object, dateObject);
            });
            object.date = new Date(object.date);
            return object;
        });
        chartData.data = _.without(_.sortBy(_.toArray(a), 'date'), null);

        return chartData;
    }
    function getArrayElementIndex(array, field, value){
        _.each(array, function(element, index){
            if(element[field].toString() === value.toString()){
                return index;
            }
        });
        return null;
    }
    function mergeJSON(source1,source2){
        /*
         * Properties from the Souce1 object will be copied to Source2 Object.
         * Note: This method will return a new merged object, Source1 and Source2 original values will not be replaced.
         * */
        var mergedJSON = source2;// Copying Source2 to a new Object

        for (var attrname in source1) {
            if(mergedJSON.hasOwnProperty(attrname)) {
                if ( source1[attrname]!=null && source1[attrname].constructor==Object ) {
                    /*
                     * Recursive call if the property is an object,
                     * Iterate the object and set all properties of the inner object.
                     */
                    mergedJSON[attrname] = mergeJSON(source1[attrname], mergedJSON[attrname]);
                }
            } else {//else copy the property from source1
                mergedJSON[attrname] = source1[attrname];

            }
        }

        return mergedJSON;
    }
    function makeGraph(id, title, color, field, valueAxis, localeObject){
        console.log(id, title, color, field);
        var graph = new AmCharts.AmGraph();
        graph.id = "gl"+id;
        graph.valueAxis = valueAxis; // we have to indicate which value axis should be used
        graph.title = title + ' ' + field;
        graph.valueField = "values" + id;
        graph.bullet = "none";
        graph.hideBulletsCount = 30;
        graph.bulletBorderThickness = 1;
        graph.lineColor = color;
        graph.fillColors = color;
        graph.fillAlphas = 1;
        graph.lineThickness = 0;
        graph.type = 'column';
        if(field === 'goals' || field === 'assists' || field === 'points' || field === 'plus_minus' || field === 'penalty_time' )
        graph.balloonText = '<span style="text-align: left; float: left">'+localeObject.fieldNames[field].shortName + ': [[values' + id +']]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage'+ id +']]</span>';

        return graph;
    }
    function contains(array, field, value){
        for(var i = 0; i < array.length; i++) {
            if (array[i][field] === value) {
                return true;
            }
        }
        return false;
    }
angular.module('Sportomatics')
.controller('PlayersSearchController', [
    '$http', '$scope', 'PlayersSearchService', '$location',
    function($http, $scope, PlayersSearchService, $location) {
    var self = this,
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;

    $scope.data = {};
    $scope.countries = [];
    $scope.loader = false;

    $scope.params = $location.search();

    $scope.PlayerPartnersPopup = {
        data: null,
        isClubsVisible: false
    };

    $scope.PlayerPartnersPopupShow = function(e, event) {
        var popup = $('.player-partners-popup:hidden'),
        url = $('#PlayerCardLink').attr('href');
        if (popup.length) {
            $scope.PlayerPartnersPopup.data = null;
            $http.get(url.replace(0, this.player.pk))
            .success(function(data) {
                $scope.PlayerPartnersPopup.data = data;
            });
            $('.player-partners-popup:hidden').show(500).offset({
                left: event.pageX,
                top: event.pageY
            });
        }
    };

    $scope.lineCheck = function(e) {
        var defaultValue = '',
            isDefault;
        isDefault = $(e).attr('value') === defaultValue;
        if ($(e).is(':checked')) {
            $('input[name="line"]').each(getUnchecker(isDefault, defaultValue));
        }
    };

    $scope.setCitizenship = function(event) {
        if (event.target.id === 'isCitizenshipAll' && event.target.checked) {
            $('#isCitizenshipRussia').attr('checked', false);
            $('#isCitizenshipOther').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipRussia' && event.target.checked) {
            $('#isCitizenshipAll').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipOther' && event.target.checked) {
            self.isCitizenshipOther = event.target.checked;
            self.isCitizenshipAll = false;
            $('#isCitizenshipAll').attr('checked', false);
        }
    }

    $scope.contractCheck = function(e) {
        var isDefault = $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="contract"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.setPlayersFilter = function(obj) {
        PlayersSearchService.setPlayersFilter($scope, obj);
    };

    $scope.setClubsFilter = function(obj) {
        PlayersSearchService.setClubsFilter($scope, obj);
    };

    // PlayersSearchService.search($scope);
    PlayersSearchService.loadCountries($scope, $location, PlayersSearchService.search);
}]);

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
angular.module('Sportomatics').controller('RegistrationController', [
    '$http', '$scope','$templateCache','$q', '$cookies', '$location', 'tags', 'ProfileService',
    function($http, $scope, $templateCache, $q, $cookies, $location, tags, ProfileService) {
        $scope.$location = $location;
        if ($location.search().uidb64 && $location.search().token) {
            $scope.selectedType = 'remember';
        } else {
            $scope.selectedType = 'social';
        }
        $scope.user = {};
        $scope.avatar = null;
        $scope.userCreated = false;
        $scope.errors = {};
        $scope.personal = {};
        $scope.rememberPasswordData = {};
        $scope.preferences = {};
        $scope.currentStep = 1;
        $scope.currentStepTemplate = 'step1';
        $scope.subscribe = true;
        $scope.personalInfo = true;
        $scope.preferencesInfo = true;
        $scope.rememberWithLogin = true;
        $scope.selectedRegistrationType = 'social';
        $scope.preferencesSports = {
            'hockey': true,
            'football': false,
            'basketball': false
        };
        $scope.tags = [];
        $scope.countries = [];
        $scope.setAvatar = ProfileService.setAvatar;
        $scope.loadTagsCountries = function (query) {
            return tags.loadCountries(query);
        };
        $scope.loadTags = function(query) {
            return tags.loadClubs(query);
        };
        $scope.$watch('countries', function(newval, oldval){
            console.log(newval);
        }, true);
        $scope.log = function(){
            console.log($scope.preferencesSports);
        };
        $scope.selectType = function(type){
            $scope.selectedType = type;
        };
        $scope.checkStep = function(){
            switch($scope.currentStep){
                case 1:
                    // return $scope.user.login && $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);
                    return $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);
                case 2:
                    return true;
                case 3:
                    return true;
            }
            return false;
        };
        $scope.comparePasswords = function(password, password2) {
            if(password && password2){
                if(password === password2) {
                    // $scope.passwordsMatch = true;
                    return true;
                } else {
                    return false;
                }
            }
            // $scope.passwordsMatch = false;
            return false;
        };
        $scope.saveStep = function(){
            var signupURL = $('#SignupApiLink').attr('href'),
            profileURL = $('#ProfileApiLink').attr('href'),
            config = {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken
                },
            };

            switch($scope.currentStep){
                case 0:
                    if($scope.personalInfo){
                        var userToLocalStorage;
                        angular.copy($scope.user, userToLocalStorage);
                        userToLocalStorage.password = undefined;
                        userToLocalStorage.password2 = undefined;
                        localStorage.setItem('sportomatics_registrationUserInfo', JSON.stringify(userToLocalStorage));
                        $scope.currentStep += 1;
                        $scope.currentStepTemplate = 'step' + $scope.currentStep;
                    }
                    break;
                case 1:
                    if($scope.personalInfo){
                        var data = {
                            username: $scope.user.email,
                            password: $scope.user.password,
                            email_notification: $scope.subscribe
                        };
                        localStorage.setItem('sportomatics_registrationPersonalInfo', JSON.stringify($scope.personal));
                        if ($scope.userCreated) {
                            $http.patch(profileURL, data, config).success(function(data) {
                                $scope.errors = {};
                                $scope.currentStep += 1;
                                $scope.currentStepTemplate = 'step' + $scope.currentStep;
                            }).error(function(data) {
                                $scope.errors = data;
                            });
                        } else {
                            $http.post(signupURL, data, config).success(function(data) {
                                $scope.userCreated = true;
                                $scope.errors = {};
                                $scope.currentStep += 1;
                                $scope.currentStepTemplate = 'step' + $scope.currentStep;
                            }).error(function(data) {
                                $scope.errors = data;
                            });
                        }
                    }
                    break;
                case 2:
                    if($scope.personalInfo){
                        var data = {
                            fio: $scope.personal.name,
                            name_visible: !$scope.personal.hideName,
                            website: $scope.personal.website
                        };
                        $http.patch(profileURL, data, config).success(function(data) {
                            $scope.errors = {};
                            $scope.currentStep += 1;
                            $scope.currentStepTemplate = 'step' + $scope.currentStep;
                        }).error(function(data) {
                            $scope.errors = data;
                        });
                    }
                    break;
                case 3:
                    if($scope.personalInfo){
                        var data = {
                            sport_hockey: $scope.preferencesSports.hockey,
                            sport_football: $scope.preferencesSports.football,
                            sport_basketball: $scope.preferencesSports.basketball,
                            countries: [],
                            clubs: []
                        };
                        $.each($scope.countries, function() {
                            data.countries.push(+this.pk);
                        });
                        $.each($scope.tags, function() {
                            data.clubs.push(+this.pk);
                        });
                        $http.patch(profileURL, data, config).success(function(data) {
                            document.location = '/';
                            // $scope.currentStep += 1;
                            // $scope.currentStepTemplate = 'step' + $scope.currentStep;
                        });
                    }
                    break;
            }
        };
        $scope.nextStep = function(){
            if($scope.checkStep()) {
                $scope.saveStep();
            }
            else alert('Введите все данные');
        };
        $scope.prevStep = function(){
            $scope.currentStep -= 1;
            $scope.currentStepTemplate = 'step'+ $scope.currentStep;
        };
        $scope.getAjaxConfig = function() {
            return {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken
                },
            };
        };
        $scope.remindPassword = function() {
            var resetURL = $('#PasswordResetApiLink').attr('href'),
            data = {
                email: $scope.rememberPasswordData.email
            };
            $http.post(resetURL, data, $scope.getAjaxConfig()).success(function(data) {
                $scope.rememberPasswordData.isSent = true;
                $scope.rememberPasswordData.errors = null;
            }).error(function(data) {
                $scope.rememberPasswordData.errors = data;
            });
        };
        $scope.setPassword = function() {
            var confirmURL = $('#PasswordResetConfirmApiLink').attr('href'),
            data = {
                uidb64: $location.search().uidb64,
                token: $location.search().token,
                password: $scope.rememberPasswordData.password
            };
            if ($scope.rememberPasswordData.password && $scope.rememberPasswordData.password2 &&
                   $scope.rememberPasswordData.password === $scope.rememberPasswordData.password2) {
                $http.post(confirmURL, data, $scope.getAjaxConfig()).success(function(data) {
                    $scope.rememberPasswordData.isComplete = true;
                    $scope.rememberPasswordData.errors = null;
                }).error(function(data) {
                    $scope.rememberPasswordData.errors = data;
                });
            }
        };
    }
]);
        function validateEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
