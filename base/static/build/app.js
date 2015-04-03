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
});

/* better fps test */
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
/* better fps test */

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

angular.module('Sportomatics')

angular.module('Sportomatics')
.value('zoomData', {
    startDate: 'a',
    endDate: 'a'
})
.factory('ChartFactory', function($q, $rootScope, AmChartsFactory, zoomData, LocaleFactory){

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
                chart.dataProvider = data;
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
                };

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
                categoryAxis.minPeriod = (chartData.groupBy === 'month') ? 'MM' : 'YYYY';
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

                var balloon = new AmCharts.AmBalloon();
                balloon.maxWidth = 300;
                if(graphs && graphs.length){
                    var oneBalloon = "<p style='text-align: left;'><span style='font-size:14px; color:#000000;'>[[value]]</span></p>";
                    var balloons = "<div class='inline-block text-left'><p style='text-align: left;'><span style='font-size:14px; color:#000000;'><b>"+localeObject.fieldNames[field].fullName+"</b></span></p>";
                    _.each(graphs, function(graph, index){
                        console.log(graph);
                        balloons+= createBalloon(graph.valueField, graph.title);
                        graph.valueAxis = valueAxis1;
                        graph.balloonText = (index < graphs.length -1 ) ? '' : balloons + '</div><div class="inline-block season-balloon"><div class="balloon-div">Сезон 06/07</div></div> ';
                       //chart.addGraph(graph);
                    });
                    _.each(graphs, function(graph, index){
                        graph.balloonText = balloons + '</div><div class="inline-block season-balloon"><div class="balloon-div">Сезон 06/07</div></div> ';
                        graph.lineColorField = 'lineColor';
                        graph.fillColorsField = 'lineColor';
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
                    graph1.lineColorField = 'lineColor';
                    graph1.fillColorsField = 'lineColor';
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
                var maximums = [];
                for(var field in data[0]){
                    maximums.push(Math.max.apply(Math,data.map(function(o){return o[field];})))
                }
                var max = Math.max.apply(null, _.filter(maximums, function(value){ return value >= 0;}));
                chart = new AmCharts.AmRadarChart();
                chart.dataProvider = data;
                chart.categoryField = "field";

                var valueAxis = new AmCharts.ValueAxis();
                valueAxis.axisAlpha = 0.15;
                valueAxis.minimum = 0;
                valueAxis.maximum = max;
                valueAxis.dashLength = 3;
                valueAxis.axisTitleOffset = 20;
                valueAxis.gridCount = 5;
                //valueAxis.stackType = "regular";
                chart.addValueAxis(valueAxis);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);

                _.each(graphs, function(graph, index){
                    graph.valueAxis = valueAxis;
                    graph.lineThickness = 3;
                    chart.addGraph(graph);
                });

                deferred.resolve(chart);
            });
            return deferred.promise;

        }
    }
});
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
function createBalloon(valueField, text){
    console.log(text)
    return "<div style='text-align: left; min-width: 60%; max-width: 80%; display: inline-block'><span style='font-size:14px; color:#000000;'>" + text + ": </span></div><div class='vertical-middle inline-block' style='width: 20%;'><div class='float-right'>[[" + valueField + "]]</div></div> ";
}
angular.module('Sportomatics').service('ClubsMapService', function(){

})
angular.module('Sportomatics')
    .factory('LocaleFactory', function($rootScope){
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
                        fullName: 'Количество проведенных игр',
                        field: 'count'
                    },
                    goals: {
                        shortName: 'Ш',
                        fullName: 'Заброшенные шайбы',
                        field: 'goals'
                    },
                    assists: {
                        shortName: 'А',
                        fullName: 'Передачи',
                        field: 'assists'
                    },
                    points: {
                        shortName: 'О',
                        fullName: 'Очки',
                        field: 'points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Коэффициент полезности',
                        field: 'plus_minus'
                    },
                    penalty_time: {
                        shortName: 'Штр',
                        fullName: 'Штрафное время, мин',
                        field: 'penalty_time'
                    },
                    es_goals: {
                        shortName: 'ШР',
                        fullName: 'Шайбы в равенстве',
                        field: 'es_goals'
                    },
                    pp_goals: {
                        shortName: 'ШБ',
                        fullName: 'Шайбы в большинстве',
                        field: 'pp_goals'
                    },
                    ev_goals: {
                        shortName: 'ШМ',
                        fullName: 'Шайбы в меньшинстве',
                        field: 'ev_goals'
                    },
                    overtime_goals: {
                        shortName: 'ШО',
                        fullName: 'Шайбы в овертайме',
                        field: 'overtime_goals'
                    },
                    win_goals: {
                        shortName: 'ШП',
                        fullName: 'Победные шайбы',
                        field: 'win_goals'
                    },
                    bullet_goals: {
                        shortName: 'РБ',
                        fullName: 'Решающие буллиты',
                        field: 'bullet_goals'
                    },
                    shots: {
                        shortName: 'БВ',
                        fullName: 'Броски по воротам',
                        field: 'shots'
                    },
                    pis__avg: {
                        shortName: '%БВ',
                        fullName: 'Процент реализованных бросков',
                        field: 'pis__avg'
                    },
                    shots__avg: {
                        shortName: 'БВ/И',
                        fullName: 'Среднее количество бросков по воротам за игру',
                        field: 'shots__avg'
                    },
                    faceoff: {
                        shortName: 'Вбр',
                        fullName: 'Вбрасывания',
                        field: 'faceoff'
                    },
                    winfaceoff: {
                        shortName: 'ВВбр',
                        fullName: 'Выигранные вбрасывания',
                        field: 'winfaceoff'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%Вбр',
                        fullName: 'Процент выигранных вбрасываний',
                        field: 'winfaceoff_p_avg'
                    },
                    gamingtime__avg: {
                        shortName: 'ВП/И',
                        fullName: 'Среднее время на площадке за игру, мин',
                        field: 'gamingtime__avg'
                    },
                    change_count__avg: {
                        shortName: 'См/И',
                        fullName: 'Среднее количество смен за игру',
                        field: 'change_count__avg'
                    },
                    shots_received: {
                        shortName: 'Бр',
                        fullName: 'Броски',
                        field: 'shots_received'
                    },
                    loose_goals: {
                        shortName: 'ПШ',
                        fullName: 'Пропущенные шайбы',
                        field: 'loose_goals'
                    },
                    saves: {
                        shortName: 'ОШ',
                        fullName: 'Отраженные броски',
                        field: 'saves'
                    },
                    saves_p__avg: {
                        shortName: '%ОШ',
                        fullName: 'Процент отраженных бросков',
                        field: 'saves_p__avg'
                    },
                    sf__avg: {
                        shortName: 'КН',
                        fullName: 'Коэффициент надежности',
                        field: 'sf__avg'
                    },
                    matches_win: {
                        shortName: 'В',
                        fullName: 'Выигрыши',
                        field: 'matches_win'
                    },
                    matches_lose: {
                        shortName: 'П',
                        fullName: 'Проигрыши',
                        field: 'matches_lose'
                    },
                    zero_goals_matches: {
                        shortName: 'И"0"',
                        fullName: '"Сухие игры"',
                        field: 'zero_goals_matches'
                    },
                    bullet_matches: {
                        shortName: 'ИБ',
                        fullName: 'Игры с буллитными сериями',
                        field: 'bullet_matches'
                    },
                    position: {
                        shortName: '',
                        fullName: 'Место',
                        field: 'position'
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
                        fullName: 'Games played',
                        field: 'count'
                    },
                    goals: {
                        shortName: 'G',
                        fullName: 'Goals',
                        field: 'goals'
                    },
                    assists: {
                        shortName: 'A',
                        fullName: 'Assists',
                        field: 'assists'
                    },
                    points: {
                        shortName: 'PTS',
                        fullName: 'Points',
                        field: 'points'
                    },
                    plus_minus: {
                        shortName: '+/-',
                        fullName: 'Plus/Minus',
                        field: 'plus_minus'
                    },
                    penalty_time: {
                        shortName: 'PIM',
                        fullName: 'Penalty in minutes',
                        field: 'penalty_time'
                    },
                    es_goals: {
                        shortName: 'ESG',
                        fullName: 'Even Strength Goals',
                        field: 'es_goals'
                    },
                    pp_goals: {
                        shortName: 'PPG',
                        fullName: 'Power play goals',
                        field: 'pp_goals'
                    },
                    ev_goals: {
                        shortName: 'SHG',
                        fullName: 'Shorthanded goals',
                        field: 'ev_goals'
                    },
                    overtime_goals: {
                        shortName: 'OTG',
                        fullName: 'Overtime goals',
                        field: 'overtime_goals'
                    },
                    win_goals: {
                        shortName: 'GWG',
                        fullName: 'Game winning goals',
                        field: 'win_goals'
                    },
                    bullet_goals: {
                        shortName: 'SDS',
                        fullName: 'Shootouts deciding shots',
                        field: 'bullet_goals'
                    },
                    shots: {
                        shortName: 'SOG',
                        fullName: 'Shots on goal',
                        field: 'shots'
                    },
                    pis__avg: {
                        shortName: '%SOG',
                        fullName: 'Shots on goal percentage',
                        field: 'pis__avg'
                    },
                    shots__avg: {
                        shortName: 'S/G',
                        fullName: 'Average Shots/Game',
                        field: 'shots__avg'
                    },
                    faceoff: {
                        shortName: 'FO',
                        fullName: 'Faceoffs',
                        field: 'faceoff'
                    },
                    winfaceoff: {
                        shortName: 'FOW',
                        fullName: 'Faceoffs won',
                        field: 'winfaceoff'
                    },
                    winfaceoff_p__avg: {
                        shortName: '%FO',
                        fullName: 'Faceoffs won percentage',
                        field: 'winfaceoff_p__avg'
                    },
                    gamingtime__avg: {
                        shortName: 'TOI/G',
                        fullName: 'Average time on ice/Game',
                        field: 'gamingtime__avg'
                    },
                    change_count__avg: {
                        shortName: 'SFT/G',
                        fullName: 'Average Shifts/Game',
                        field: 'change_count__avg'
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

    })

angular.module('Sportomatics').service('MapService', function($q, $timeout){
        var self = this;
        var startCoordinate1 = 55.749792; // Moscow latitude
        var startCoordinate2 = 37.632495; // Moscow longitude

        // Variables:

        self.mapsDivName = 'clubs-map';
        this.clubs_map = document.getElementById(self.mapsDivName);
        this.rendered = false;
        this.map = null;
        this.geocoder = new google.maps.Geocoder();
        this.addedMarkers = [];

        // Methods:

        this.createClubsMap = function(data, dataLabel){ // creates clubs map inside maps-div marked as mapsDivName
            self.map = L.map(self.mapsDivName, {
                scrollWheelZoom: false
            }).setView([startCoordinate1, startCoordinate2], 4);
            var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
            var ggl = new L.Google('ROADMAP');
            self.map.addLayer(ggl);
            self.map.addControl(new L.Control.Layers( {'Google':ggl, 'OpenStreetMap': osm}, {}));
            self.markers = new L.MarkerClusterGroup({ showCoverageOnHover: false });
            switch (dataLabel){
                case 'clubs':
                    self.markersFunctionClubs(data);
                    break;
                case 'players':
                    self.markersFunctionPlayers(data);
                    break;
                case 'trips':
                    self.markersFunctionClubGames(data);
                    break;
            }
            self.map.addLayer(self.markers);
            this.rendered = true;
        };

        this.markersFunctionClubs = function(clubs){
            var countOfGeocoded = 0;
            _.each(clubs, function(club, index){
                var clubIcon = L.icon({
                    iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
                    iconSize: [20, 20],
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48]
                });
                if(!club.arena) return;
                var coords = club.arena.coords;
                if(coords != null){
                    var coordinate1 = coords.split(',')[0];
                    var coordinate2 = coords.split(',')[1];
                }
                if(!club.arena.coords){
                    self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result){
                       self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {icon: clubIcon}).bindPopup(club.title + '<br>'));
                    });
                    countOfGeocoded++;
                }
                if(coordinate1 && coordinate2){
                    self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {icon: clubIcon}).bindPopup(club.title + '<br>'));
                }
            });
        };

        this.markersFunctionClubGames = function(games){
            var countOfGeocoded = 0;
            var clubs = [];
            _.each(games, function(game, index){
                if(game.is_guest){
                    var club = game.home_team;
                    if(!club.arena) return;
                    if(_.findWhere(clubs, {'title': club.title})) return; // prevent duplicate clubs

                    clubs.push(club);
                    var clubIcon = L.icon({
                        iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
                        iconSize: [20, 20],
                        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                        shadowSize: [34, 48]
                    });
                    var coords = club.arena.coords;
                    if(coords != null){
                        var coordinate1 = coords.split(',')[0];
                        var coordinate2 = coords.split(',')[1];
                    }
                    var clubDates = [];
                    _.each(games, function(game){
                        if(game.home_team.title === club.title) clubDates.push(new Date(game.date).yyyymmddFormatted());
                    });
                    var clubDatesString = clubDates.join(" <br> ");
                    var popup = L.popup({
                        className: 'map-popup'
                    }).setContent('<div class="bold">' + club.title + '</div><br> Матчи:<br>'+ clubDatesString);
                    if(!club.arena.coords){
                        self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result){
                            self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {icon: clubIcon}).bindPopup(popup));
                        });
                        countOfGeocoded++;
                    }
                    if(coordinate1 && coordinate2){
                        self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {icon: clubIcon}).bindPopup(popup));
                    }
                }
            });
        };

        this.markersFunctionPlayers = function(players){
            var countOfGeocoded = 0;
            _.each(players, function(player, index){
                if(!player.birth_place) return;
                var playerIcon = L.icon({
                    iconUrl: player.photo ? player.photo : '/static/abc.jpg',
                    iconSize: [20, 20],
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48]
                });
                self.googleGeocode(player.birth_place, countOfGeocoded).then(function(result){
                    self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {icon: playerIcon}).bindPopup(player.fio + '<br> Место рождения: ' + player.birth_place));
                });
                countOfGeocoded++;
            });
        };

        this.isRendered = function(){ // return map rendered state
            return this.rendered;
        };

        this.setRendered = function(value){ // set boolean state for map rendered variable
            if(value !== true && value !== false) return;
            this.rendered = value;
        };

        this.remove = function(){
            $('#'+self.mapsDivName).remove();
            $('#'+self.mapsDivName + '-container').append('<div id="' + self.mapsDivName + '"></div>');
        };

        this.googleGeocode = function(address, delay){
            var deferred = $q.defer();
            address = address.substr(address.indexOf(" ") + 1).replace('ул.', "").replace('д.', '').replace('Московская обл.,', '')
            if(address.indexOf('Телефон') > -1) address = address.substring(0, address.indexOf('Телефон'));
            $timeout(function(){
                self.geocoder.geocode({'address': address}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        var coordinate1 = results[0].geometry.location.B;
                        var coordinate2 = results[0].geometry.location.k;
                        deferred.resolve([coordinate2, coordinate1]);
                    } else {
                        deferred.reject();
                        console.log(address, 'Geocode was not successful for the following reason: ' + status);
                    }
                });
            }, 400 * delay);

            return deferred.promise;
        };


});
angular.module('Sportomatics')
.service('PlayersSearchService', function($http) {
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
            $scope.$location.search('alphabet', null);
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

        $scope.$location.search('number', $scope.number);

        $scope.params = $scope.$location.search();

        params += 'order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
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
        if ($scope.params.season) {
            params += '&season=' + $scope.params.season;
        }
        if ($scope.params.league) {
            $.each($scope.params.league, function() {
                params += '&league=' + this;
            });
        }
        if ($scope.params.number) {
            params += '&number=' + $scope.params.number;
        }
        $scope.data = {};
        $scope.loader = true;
        $http.get(url + '?' + params).success(function(data) {
            $scope.data = data;
            $scope.loader = false;
        });
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
});

angular.module('Sportomatics').service('ProfileService',
    function($http, $cookies) {
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
    }
);

angular.module('Sportomatics').factory('RadarChartFactory', function(ChartFactory, LocaleFactory, $http, $q, $timeout){

    var RadarChart = function(){

        var self = this;

        // Variables:

        this.localeObject = LocaleFactory.locale_ru;
        this.playerId = document.getElementById('player-id').value;
        this.playerName = document.getElementById('player-name').value;
        this.apiPlayersUrl = document.getElementById('api-players-url').value;
        this.selectedRadarFields = [{ // default radar fields we use
            field: "goals"
        }, {
            field: "points"
        }, {
            field: "assists"
        }, {
            field: "plus_minus"
        }];

        this.availableFields = _.toArray(LocaleFactory.locale_ru.fieldNames); // generate available fields
        _.each(this.availableFields, function(object){
            object.ticked = !!(object.field === 'points' || object.field === 'goals' || object.field === 'assists' || object.field === 'plus_minus');
        });

        // Methods:

        this.setApiPlayersUrl = function(value){
            this.apiPlayersUrl = value;
        };

        this.setSelectedRadarFields = function(selectedRadarFields){
            if(selectedRadarFields != null)
            this.selectedRadarFields = selectedRadarFields;
        };

        this.getSeasons = function(){
            return this.seasons;
        };

        this.setLocaleObject = function(localeObject){
            this.localeObject = localeObject;
        };

        this.create = function(players, dataBySeason, season, sum) { // function to create radar chart for one or multiple players

            var deferred = $q.defer();

            this.seasons = dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); })
            this.playersInRadarChart = [];
            this.playersRadarChartData = [];
            _.each(this.selectedRadarFields, function(field){
                self.playersRadarChartData.push({
                    field: field.field
                })
            });
            this.playersRadarChartGraphs = [];
            if(players.length > 0) { // multiple players
                if (sum) {
                    var playersRequestArray = [];
                    _.each(players, function (player) {
                        var url = self.apiPlayersUrl + player + '/indicators/?group_by=season';
                        playersRequestArray.push($http.get(url));
                    });
                    $q.all(playersRequestArray).then(function (results) { // we should request all players data
                        self.lastSeason = Math.max.apply(Math, this.dataBySeason.results.map(function (o) {
                            return parseInt(o.season.end_date.substr(0, 4));
                        })).toString();
                        self.playerSeasons = this.dataBySeason.results.map(function (e) {
                            return e.season.end_date.substr(0, 4);
                        });

                        _.each(results, function (result) {
                            var playerSeasonsDataResults = result.data.results;
                            var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                return e.season.end_date.substr(0, 4);
                            });
                            self.playerSeasons = self.playerSeasons.concat(playerSeasons).unique().sort();

                            var playerDataInSeason = _.filter(playerSeasonsDataResults, function (e) {
                                return e.season.end_date.indexOf(season) > -1;
                            })[0];
                            _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                                if (playerDataInSeason) {
                                    if (radarChartDataCategory['value']) {
                                        radarChartDataCategory['value'] += playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                    }
                                    else {
                                        radarChartDataCategory['value'] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                    }
                                } else {
                                    radarChartDataCategory['value'] = 0;
                                }
                            });
                            self.playersInRadarChart.push({
                                player: player,
                                playerData: playerDataInSeason
                            });
                        });
                        _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                            radarChartDataCategory['value'] = radarChartDataCategory['value'] / self.playersInRadarChart.length;
                        });
                        var graph = new AmCharts.AmGraph();
                        graph.valueField = "value";
                        graph.bullet = "round";
                        graph.balloonText = "team [[value]]";
                        self.playersRadarChartGraphs.push(graph);
                        ChartFactory.generateRadarChart(self.playersRadarChartData, self.playersRadarChartGraphs).then(function (chart) {
                            self.chartRadar = chart;
                            self.chartRadar.write('chartdiv2');
                            deferred.resolve(true);
                        })
                    });
                } else if (players.length > 1) {
                    _.each(players, function (player) {
                        var url = self.apiPlayersUrl + player + '/indicators/?group_by=season';
                        $http.get(url)
                            .success(function (playerSeasonsData) {
                                var playerSeasonsDataResults = playerSeasonsData.results;
                                var playerSeasons = playerSeasonsDataResults.map(function (e) {
                                    return e.season.end_date.substr(0, 4);
                                });
                                var playerDataInSeason = _.filter(playerSeasonsDataResults, function (e) {
                                    return e.season.end_date.indexOf(season) > -1;
                                })[0];
                                self.seasons = self.seasons.concat(playerSeasons).unique().sort();
                                _.each(self.playersRadarChartData, function (radarChartDataCategory, index) {
                                    if (playerDataInSeason && playerDataInSeason['count']) {
                                        radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field] / playerDataInSeason['count'];
                                        if(radarChartDataCategory.field === 'shots')
                                            radarChartDataCategory['value' + player] /= 10;
                                    } else {
                                        radarChartDataCategory['value' + player] = 0;
                                    }
                                });
                                $http.get(self.apiPlayersUrl+player)
                                    .success(function(playerInfo){
                                        var playerName = playerInfo.name + ' ' + playerInfo.lastname;
                                        var graph = new AmCharts.AmGraph();
                                        graph.valueField = "value" + player;
                                        graph.bullet = "round";
                                        graph.balloonText = playerName + " [[value]]";
                                        graph.title = playerName;
                                        graph.balloonFunction = function(a,b){
                                            var value = a.values.value;
                                            var title = b.title;
                                            if(a.category === 'shots' || a.category === 'shots__avg') value *= 10;
                                            return title + ', ' + self.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                                        };
                                        self.playersInRadarChart.push({
                                            player: player,
                                            playerData: playerDataInSeason
                                        });
                                        self.playersRadarChartGraphs.push(graph);
                                    }).then(function () {
                                        ChartFactory.generateRadarChart(self.playersRadarChartData, self.playersRadarChartGraphs).then(function (chart) {
                                            self.chartRadar = chart;
                                            deferred.resolve(true);
                                        })
                                    });
                            })
                    })
                }
                else { // 1 player
                    var player = players[0];
                    var playerSeasonsData = dataBySeason; //dataBySeason
                    var playerSeasonsDataResults = dataBySeason.results;
                    var playerDataInSeason = _.filter(playerSeasonsDataResults, function(e){ return e.season.end_date.indexOf(season) > -1;})[0];
                    var maximums = [];
                    var data = this.playersRadarChartData;
                    var balloonValues = [];
                    _.each(this.playersRadarChartData, function(radarChartDataCategory){
                        if(playerDataInSeason && playerDataInSeason['count']){
                            radarChartDataCategory['value' + player] = playerDataInSeason[radarChartDataCategory.field];
                            if(radarChartDataCategory.field !== 'shots__avg') radarChartDataCategory['value' + player] /= playerDataInSeason['count'] ;
                            if(radarChartDataCategory.field === 'shots' || radarChartDataCategory.field === 'shots__avg')
                                radarChartDataCategory['value' + player] /= 10;
                        } else {
                            radarChartDataCategory['value' + player] = 0;
                        }
                    });
                    for(var field in data[0]){
                        maximums.push(Math.max.apply(Math, data.map(function(o){return o[field];})))
                    }
                    var max = Math.max.apply(null, _.filter(maximums, function(value){ return value >= 0;}));
                    var graph = new AmCharts.AmGraph();
                    graph.valueField = "value" + player;
                    graph.bullet = "round";
                    graph.balloonText = this.playerName + " [[value]]";
                    graph.title = this.playerName;
                    graph.balloonFunction = function(a,b){
                        var value = a.values.value;
                        var title = b.title;
                        if(a.category === 'shots' || a.category === 'shots__avg') value *= 10;
                        return title + ', ' + self.localeObject.fieldNames[a.category].fullName + ': ' + value.toFixed(3);
                    };
                    this.playersInRadarChart.push({
                        player: player,
                        playerData: playerDataInSeason
                    });
                    this.playersRadarChartGraphs.push(graph);
                    console.log(this.playersRadarChartData);
                    ChartFactory.generateRadarChart(this.playersRadarChartData, this.playersRadarChartGraphs).then(function(chart){
                        $timeout(function(){
                            self.chartRadar = chart;
                            self.chartRadar.write('chartdiv2');
                        }, 100);
                        deferred.resolve(true);
                    })
                }
            }

            return deferred.promise;

        }; // createRadar

        this.draw = function(){
            if(this.chartRadar != null)
            this.chartRadar.write('chartdiv2');
        }; // draw

    };

    return {
        PlayerRadarChart: RadarChart
    };

    // End of factory declaration
    
});
angular.module('Sportomatics').service('tags', function($http, $q, $filter) {
  this.loadCountries = function(url, query) {
    return $http.get(url);
  };
  this.loadClubs = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
});

angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', '$parse', 'MapService', function($scope, $http, $location, $parse, MapService) {
    $scope.MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    $scope.data = {};
    $scope.params = $location.search();
    $scope.CalendarEventPopup = {};
    $scope.CalendarEventPopupShow = function(e, event) {
      var params;
      if ($('.calendar-event-popup:hidden').length && this.cell.schedule) {
        $scope.CalendarEventPopup.data = null;
        $scope.CalendarEventPopup.is_home = this.cell.schedule.is_home;
        $scope.CalendarEventPopup.is_guest = this.cell.schedule.is_guest;
        params = '';
        if (this.cell.schedule.is_home) {
          params = '?is_home=true';
        }
        if (this.cell.schedule.is_guest) {
          params = '?is_guest=true';
        }
        $http.get($scope.urlPopup.replace(0, this.cell.schedule.pk) + params).success(function(data) {
          $scope.CalendarEventPopup.data = data;
        });
        $('.calendar-event-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
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
    $scope.parseSchedules = function(data) {
      var getDate, k, len, ref, result, s;
      result = {};
      getDate = $parse('date|date:"yyyy-MM-dd"');
      ref = data.results;
      for (k = 0, len = ref.length; k < len; k++) {
        s = ref[k];
        result[getDate(s)] = s;
      }
      return result;
    };
    $scope.getSchedule = function(schedules, date) {
      var strfdate;
      strfdate = function(date) {
        var d, m, y;
        y = 1900 + date.getYear();
        m = String(date.getMonth() + 1);
        if (m.length < 2) {
          m = '0' + m;
        }
        d = String(date.getDate());
        if (d.length < 2) {
          d = '0' + d;
        }
        return [y, m, d].join('-');
      };
      return schedules[strfdate(date)];
    };
    $scope.getCalendar = function(date, schedules) {
      var cell, day, daysInM, i, j, k, month, result, row, startDoW, year;
      year = date.getYear() + 1900;
      month = date.getMonth();
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
          cell = {
            'cell': i * 7 + j
          };
          day = cell.cell - startDoW + 1;
          if ((1 <= day && day <= daysInM)) {
            cell['date'] = new Date(year, month, day);
            cell['schedule'] = $scope.getSchedule(schedules, cell.date);
          }
          row.push(cell);
        }
        result.push(row);
        i += 1;
      }
      return result;
    };
    $scope.isHome = function(cell) {
      return cell.schedule && cell.schedule.is_home && $scope.params.type !== 'guest';
    };
    $scope.isGuest = function(cell) {
      return cell.schedule && cell.schedule.is_guest && $scope.params.type !== 'home';
    };
    $scope.getLogo = function(cell) {
      if ($scope.isHome(cell)) {
        return cell.schedule.guest_team.logo;
      }
      if ($scope.isGuest(cell)) {
        return cell.schedule.home_team.logo;
      }
      return null;
    };
    $scope.monthDelta = function(date, deltaM) {
      var d;
      d = new Date(date);
      d.setDate(1);
      d.setMonth(d.getMonth() + deltaM);
      return d;
    };
    $scope.getMinEndDate = function(data) {
      var a, b;
      a = new Date();
      b = new Date(data.season.end_date);
      if (a < b) {
        return a;
      } else {
        return b;
      }
    };
    $scope.list = function() {
      var params;
      $scope.params = $location.search();
      params = '';
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        var date, deltaM;
        console.log(data);
        if (MapService.isRendered()) {
          MapService.remove();
        }
        MapService.createClubsMap(data.results, 'trips');
        $scope.data = data;
        $scope.schedules = $scope.parseSchedules(data);
        date = $scope.getMinEndDate(data);
        $scope.calendars = [
          (function() {
            var k, len, ref, results;
            ref = [-1, 0, 1];
            results = [];
            for (k = 0, len = ref.length; k < len; k++) {
              deltaM = ref[k];
              results.push({
                'date': $scope.monthDelta(date, deltaM),
                'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
                'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
              });
            }
            return results;
          })()
        ];
        return $scope.loaded = true;
      });
    };
    $scope.previous = function() {
      var date, deltaM;
      date = $scope.calendars[$scope.calendars.length - 1][0].date;
      return $scope.calendars.push((function() {
        var k, len, ref, results;
        ref = [-3, -2, -1];
        results = [];
        for (k = 0, len = ref.length; k < len; k++) {
          deltaM = ref[k];
          results.push({
            'date': $scope.monthDelta(date, deltaM),
            'month_display': $scope.MONTHS[$scope.monthDelta(date, deltaM).getMonth()],
            'table': $scope.getCalendar($scope.monthDelta(date, deltaM), $scope.schedules)
          });
        }
        return results;
      })());
    };
  }
]);

angular.module('Sportomatics')
    .controller('ClubHomeMapController', function($scope, $rootScope){
        /*var coordinates = $('#coordinates').val();
        var coordinate1 = coordinates.split(',')[0];
        var coordinate2 = coordinates.split(',')[1];
        var title = $('#place-title').val();

        console.log(coordinate1, coordinate2)
        console.log(coordinates.replace(' ', '+'));
        // create a map in the "map" div, set the view to a given place and zoom
        var map = L.map('map').setView([coordinate1, coordinate2], 15);

        // add an OpenStreetMap tile layer
        L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // add a marker in the given location, attach some popup content to it and open the popup
        L.marker([coordinate1, coordinate2]).addTo(map)
            .bindPopup(title + '<br>')
            .openPopup();*/
    })
angular.module('Sportomatics')
.controller('ClubListController', [
    '$http', '$scope', '$location', 'PlayersSearchService', 'MapService',
    function($http, $scope, $location, PlayersSearchService, MapService) {
    var url = $('#ClubListForm').attr('action');
    this.map = true;

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
                $scope.clubs = data.results;
                $scope.loaded = true;
            }).then(function(){
                if(MapService.isRendered()) MapService.remove();
                MapService.createClubsMap($scope.clubs, 'clubs');
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
                $scope.clubs = $scope.clubs.concat(data.results);
            }
            $scope.loaded = true;
        }).then(function(){
            if(MapService.isRendered()) MapService.remove();
            MapService.createClubsMap($scope.clubs, 'clubs');
        });
    };

    PlayersSearchService.loadCountries($scope, $location, function(){});
}]);

angular.module('Sportomatics')
    .controller('ClubNewsController', function($scope, $http, ChartFactory, LocaleFactory, $timeout){
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
    })
angular.module('Sportomatics').controller('ClubStatsController', [
  '$http', '$scope', '$location', 'PlayersSearchService', function($http, $scope, $location, PlayersSearchService) {
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;
    $scope.data = {};
    $scope.countries = [];
    $scope.loader = false;
    $location.search('club', +$('[name="club"]').val());
    $scope.params = $location.search();
    $scope.PlayerPartnersPopup = {
      'data': null,
      'isClubsVisible': false
    };
    $scope.PlayerPartnersPopupShow = function(e, event) {
      var popup, url;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length) {
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, this.player.pk)).success(function(data) {
          $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
    $scope.setPlayersFilter = function(obj) {
      PlayersSearchService.setPlayersFilter($scope, obj);
    };
    $scope.setSeason = function(e) {
      $location.search('season', $(e).val());
      $scope.params = $location.search();
      PlayersSearchService.search($scope);
    };
    PlayersSearchService.search($scope);
  }
]);

angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout', 'MapService',
    function($http, $scope, $timeout, MapService) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        popup = null;
        $scope.type = 'photos';
        $scope.cache_players = null;
        $scope.cache_clubs = null;
        $scope.notplaying_players = null;

        $scope.setType = function(type){
            $scope.type = type;
            $scope.unMakeTransferArrows()
        };

        $scope.go = function(path){
            window.location.href = path;
        };

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

        $scope.workWithData = function(data){
            console.log(data);

            if(MapService.isRendered()) MapService.remove();
            MapService.createClubsMap(data.all_players, 'players');

            var goalkeeper_players = data.goalkeeper_players;
            var defender_players = data.defender_players;
            var offender_players = data.offender_players;
            var players = [];
            _.each(offender_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
            _.each(defender_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
            _.each(goalkeeper_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
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
                    case 'home':
                        return cell.is_home;
                }
            } else {
                return false;
            }
        };

        self.isPersonInCell = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            return cell;
        };

        self.list = function(callback, callbackArg) {
            var params = $('#ClubTeamForm').serialize();
            self.players.data = null;
            self.players.table = null;
            self.players.loader = true;
            self.clubs.clubs = [];
            $http.get(url + '?' + params)
            .success(function(data) {
                $scope.players = data;
                self.players.data = data;
                self.players.table = {
                    'goalkeeper': data.goalkeeper_players,
                    'defender': data.defender_players,
                    'forward': data.offender_players,
                    'trainer': data.coaches
                };
                $http.get('/static/json/countries-json-ru-codes.json')
                .success(function(data){
                    $scope.countryCodes = data;
                }).then(function(){
                    $scope.workWithData($scope.players);
                });
                self.players.loader = false;
                if (typeof callback === 'function') {
                    callback(callbackArg);
                }
            });
        };

        this.compare = function(arg) {
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
                    console.log(data)
                if (data.leagues.length) {
                    var clubRows = [];
                    var clubsInRow = [];
                    var clubs = [];
                    $scope.clubplayers = [];
                    _.each(data.leagues, function(league, index){
                        clubs = clubs.concat(league.clubs);
                        $scope.clubplayers = $scope.clubplayers.concat(league.clubplayers);
                    });
                    _.each(clubs, function(club, index){
                        if(clubsInRow.length < 7){
                            clubsInRow.push(club)
                        }
                        if(index === clubs.length -1 || (index + 1) % 7 === 0){
                            clubRows.push(clubsInRow);
                            clubsInRow = [];
                        }
                    });
                    var clubsObject = {
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs
                        },
                        'league': data.leagues[0],
                        'clubRows': clubRows
                    };
                    self.clubs.clubs.push(clubsObject);
                }
                self.clubs.loader = false;
                if(arg !== false){
                }
            });
        };

        $scope.getFromCache = function() {
            if ($scope.cache_players) {
                $scope.players = $scope.cache_players;
                $scope.clubs = $scope.cache_clubs;
            }
        };

        $scope.makeTransferArrows = function(){
            $scope.getFromCache();
            _.each($scope.clubplayers, function(clubplayer){
                createTransferArrow('#club_'+clubplayer.club, '#player_'+clubplayer.player, clubplayer.pk);
            });
            $( ".player-item" ).each(function() {
                if(!_.findWhere($scope.clubplayers, {player: parseInt($(this).attr('id').split('_')[1]) })){
                    $( this ).addClass("opacity-30");
                } else {
                    var id = $(this).attr('id');
                    $(this).hover(function(){
                        $("canvas").each(function(){
                            if ($(this).attr('player') !== id)
                                $(this).addClass("opacity-10");
                        })
                    }, function(){
                        $("canvas").each(function(){
                            $(this).removeClass("opacity-10");
                        })
                    })
                }
            });
        };
        $scope.unMakeTransferArrows = function(){
            $scope.getFromCache();
            $('canvas').remove();
            $( ".player-item" ).each(function() {
                $( this ).removeClass("opacity-30");
            });
        };

        //this.list(this.compare, false);

        $scope.notPlayingNow = function(callback, callbackArg) {
            $scope.unMakeTransferArrows();
            $scope.players.loader = true;
            if ($scope.notplaying_players) {
                $scope.players = $scope.notplaying_players;
            } else {
                $http.get(url+'?notplaying=1').success(function(data) {
                    $scope.cache_players = $scope.players;
                    $scope.cache_clubs = $scope.clubs;
                    $scope.players = data;
                    $scope.players.data = data;
                    $scope.players.table = {
                        'goalkeeper': data.goalkeeper_players,
                        'defender': data.defender_players,
                        'forward': data.offender_players,
                        'trainer': data.coaches
                    };
                    $scope.notplaying_players = $scope.players;
                });
            }
            $scope.workWithData($scope.players);
            $scope.players.loader = false;
            if (typeof callback === 'function') {
                callback(callbackArg);
            }
        };

        function drawArr(c, fromx, fromy, tox, toy){
            //variables to be used when creating the arrow
            var ctx = c;
            var headlen = 5;
            var angle = Math.atan2(toy-fromy,tox-fromx);
            //starting path of the arrow from the start square to the end square and drawing the stroke
            ctx.beginPath();
            ctx.moveTo(fromx, fromy);
            var amount = 0;
            (function myLoop (amount) {
               setTimeout(function () {
                   amount += 0.05; // change to alter duration
                    ctx.lineWidth = 5;
                    ctx.lineTo(fromx + (tox - fromx) * amount,
                             fromy + (toy - fromy) * amount);
                    ctx.stroke();
                    if (amount < 1){
                       myLoop(amount);
                    }
                    else {
                         //starting a new path from the head of the arrow to one of the sides of the point
                        ctx.beginPath();
                        ctx.moveTo(tox, toy);
                        ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));

                        //path from the side point of the arrow, to the other side point
                        ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),toy-headlen*Math.sin(angle+Math.PI/7));

                        //path from the side point back to the tip of the arrow, and then again to the opposite side point
                        ctx.lineTo(tox, toy);
                        ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));

                        //draws the paths created above
                        //ctx.strokeStyle = "#cc0000";
                        ctx.lineWidth = 5;
                        ctx.stroke();
                        ctx.fill();
                    }
               }, 30)
            })(0);
            //ctx.lineTo(tox, toy);
            //ctx.strokeStyle = "#cc0000";
            //ctx.lineWidth = 10;
            //ctx.stroke();
        }

        function createTransferArrow(from, to, id){

                var $from = $(from);
                var $to = $(to);
                if($to.length === 0 || $from.length === 0) return;
                // find offset positions for the word (t = this) and image (i)
                var ofrom = {
                    x: $from.offset().left + $from.width() / 2,
                    y: $from.offset().top + $from.height() / 2
                };
                var oto = {
                    x: $to.offset().left + $to.width() / 2,
                    y: $to.offset().top + $to.height() / 2
                };
                // x,y = top left corner
                // x1,y1 = bottom right corner
                var p = {
                    x: ofrom.x < oto.x ? ofrom.x : oto.x,
                    x1: ofrom.x > oto.x ? ofrom.x : oto.x,
                    y: ofrom.y < oto.y ? ofrom.y : oto.y,
                    y1: ofrom.y > oto.y ? ofrom.y : oto.y
                };
                // create canvas between those potonts
                var c = $('<canvas id="'+id+'" player="'+ to.replace('#', '') + '" />').attr({
                    'width': p.x1 - p.x + 20 ,
                    'height': p.y1 - p.y + 20
                }).css({
                    'position': 'absolute',
                    'left': p.x,
                    'top': p.y,
                    'z-index': 1
                }).appendTo($('body'))[0].getContext('2d');

                // draw line
                var x1 = ofrom.x - p.x + 10;
                var y1 = ofrom.y - p.y - 30;
                var x2 = oto.x - p.x; //+20
                var y2 = oto.y - p.y + 40;

                drawArr(c, x1,y1,x2,y2,1,2);
        }

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
.factory('ClubInstaPhoto', function($resource){
    return $resource("/ru/api/hockey/clubinstaphoto/"+":id/", {}, {
        query: {method:'GET', params:{processed: 1, id: null}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('PlayerInstaPhoto', function($resource){
    return $resource("/ru/api/hockey/playerinstaphoto/", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('ArenaInstaPhoto', function($resource){
    return $resource("/ru/api/hockey/processedarenainstaphoto/", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('InstagramUser', function($resource){
    return $resource("/ru/api/base/instagram_user/"+":id/", {}, {
        query: {method:'GET', params:{id:null}, isArray:true},
        get: { method: 'GET'}
    });
})
.controller('PhotosController', function($scope, ClubInstaPhoto, InstagramUser,PlayerInstaPhoto,ArenaInstaPhoto, $resource, $timeout, $location){

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
})
    angular.module('Sportomatics')
        .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q, RadarChartFactory) {
            //http://www.amcharts.com/lib/images/
            var self = this;
            var url = $('#IndicatorsLink').attr('href');
            this.field = $location.search()['field'] || 'count';
            this.club = parseInt($location.search()['club']) || null;
            this.coach = parseInt($location.search()['coach']) || null;
            this.compare_to = parseInt($location.search()['compare_to']) || null;
            this.groupBy = 'season';
            this.data = [];
            this.graphData = {};
            this.chartsCount = 0;
            this.playerUrl = '';
            this.playerId = document.getElementById('player-id').value;
            this.playerName = document.getElementById('player-name').value;
            $scope.apiPlayersUrl = document.getElementById('api-players-url').value;
            $scope.limited = false; // user is not limited by default
            $scope.activeSeason = -1; // all seasons selected by default
            $scope.playersToCompare = [];
            $scope.radarPlayers = [self.playerId]; // array of players to compare in radar chart
            $scope.playerToCompare = { // last found player to compare with
                id: this.compare_to
            };
            $scope.currentPlayerObject = { // object of current player
                id: self.playerId,
                title: self.playerName,
                color: "#408e3a"
            };
            $scope.dataType = 'graph-serial'; // we'll be on serial chart tab by default

            $scope.setDataType = function(type){
                $scope.dataType = type;
                if(type === 'graph-radar'){
                    if($scope.playerToCompare.id){
                        $http.get($scope.apiPlayersUrl+$scope.playerToCompare.id)
                            .success(function(data){
                                $timeout(function(){
                                    $scope.playerToCompare.photo = data.photo;
                                    $scope.playerToCompare.name = data.name + ' ' + data.lastname + ' ( ' + data.club.title + ' )';
                                    $scope.playerToCompare.club = data.club;
                                }, 100)
                            })
                    }
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason);//.then(function(){});
                }
            };

            $scope.addRadarGraph = function(id){
                if(_.contains($scope.radarPlayers, id)) return;
                $scope.radarPlayers.push(id);
                $scope.createRadar($scope.radarPlayers, $scope.lastSeason);//.then(function(){});
            };

            this.setField = function(field) {
                $location.search('field', field);
                this.field = field;
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

            $scope.removeGraph = function(player){
                if(contains($scope.playersToCompare, 'id', (parseInt(player.id)).toString())){
                    $scope.playersToCompare = _.without($scope.playersToCompare, _.findWhere($scope.playersToCompare, {id: (parseInt(player.id)).toString()}));
                    $scope.makeChart($scope.activeSeason > -1);
                }
            };

            $scope.$watch('playerToCompare.id', function(newval){
                if(newval){
                    $http.get($scope.apiPlayersUrl+newval)
                        .success(function(data){
                            $scope.playerToCompare.photo = data.photo;
                            $scope.playerToCompare.name = data.name + ' ' + data.lastname + ' ( ' + data.club.title + ' )';
                            $scope.playerToCompare.club = data.club;
                        })
                } else {
                    $scope.playerToCompare = {};
                    $location.search('compare_to', null);
                }
            });

            $scope.addGraph = function(id){
                //$('#chartdiv').empty();
                if(!id) return;
                $location.search('compare_to', id);
                $http.get($scope.apiPlayersUrl+id)
                    .success(function(data){
                        $scope.playerToCompare.photo = data.photo;
                        $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                        $scope.playerToCompare.club = data.club;
                        /*if(contains($scope.playersToCompare, 'id', (parseInt(id)).toString())){
                         $scope.playersToCompare = _.without($scope.playersToCompare, _.findWhere($scope.playersToCompare, {id: (parseInt(id)).toString()}));
                         return $scope.makeChart($scope.activeSeason > -1);
                         }*/
                        var playerObject = {
                            title: $scope.playerToCompare.name || id,
                            color: $scope.playerToCompare.club.main_color || getRandomColor(),
                            id: id,
                            link: $scope.apiPlayersUrl + id + '/indicators/'
                        };
                        url = playerObject.link;
                        var localUrlMonths = url + '?group_by=month';
                        var localUrlSeasons = url + '?group_by=season';
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
                                        $scope.playersToCompare.push(playerObject);
                                        $scope.makeChart($scope.activeSeason > -1);
                                    })
                            })
                    })
            };

            $scope.makeChart = function(switched){ // make column chart with multiple players
                var initialData = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason; // initial player data
                var initialGraph = makeGraph('', $scope.currentPlayerObject.title, $scope.currentPlayerObject.color, self.field, null, $scope.localeObject); // initial player graph
                var initialChartData = generateChartData(initialData.results, self.field, self.groupBy); // chart data generated with initial player
                var newChartGraphs = [initialGraph]; // array of graphs we'll use in chart creation
                var newChartData = {}; // object to create chart
                _.each($scope.playersToCompare, function(player, index) {
                    var data = (self.groupBy === 'month') ? player.dataByMonth : player.dataBySeason; // data by season or month same as initial player data
                    newChartData = populateChartData(initialChartData, data.results, self.field, $scope.localeObject, player);
                    var newChartGraph = makeGraph(player.id, player.title, player.color, self.field, null, $scope.localeObject);
                    newChartGraphs.push(newChartGraph);
                });
                if(switched){
                    if($scope.playersToCompare.length === 0) newChartData.data = initialData.results;
                    var datesArray = newChartData.data.map(function(e){ return new Date(e['date']) });
                    var min = Math.min.apply(null, datesArray);
                    var max = Math.max.apply(null, datesArray);
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                if(!$scope.playersToCompare.length) newChartData = initialChartData;
                ChartFactory.generateSerialChart(self.field, newChartData, $scope.localeObject, newChartGraphs).then(function(chart){
                    $scope.chart = chart;
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
                $scope.getPlayerDataByMonth().then(function(){
                    zoomData.startDate = season.start_date;
                    zoomData.endDate = season.end_date;
                    $scope.onSeason = true;
                    self.groupBy = 'month';
                    self.data = $scope.dataByMonth;
                    self.list(true);
                    $scope.activeSeason = index;
                })
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

                    if(self.coach){
                        _.each($scope.chart.dataProvider, function(data){
                            if($scope.activeSeason !== -1) data.lineColor = "#408e3a";
                            else
                            _.each($scope.coachData.results, function(coachData){
                                if(new Date(data.date).getFullYear() === new Date(coachData.end_date).getFullYear()){
                                    data.lineColor = "#699c97"
                                }
                            })
                        });
                    }
                    if(self.club){
                        _.each($scope.chart.dataProvider, function(data){
                            if($scope.activeSeason !== -1) data.lineColor = "#408e3a";
                            else
                            _.each($scope.clubData.results, function(clubData){
                                if(new Date(data.date).getFullYear() === new Date(clubData.end_date).getFullYear()){
                                    data.lineColor = "#699c97"
                                }
                            })
                        });
                    }

                    if ($scope.playersToCompare.length > 0) return $scope.makeChart(switched); //player comparison
                    if ($scope.limited) { //not registered users
                        $scope.chart.chartCursor = null;
                        $scope.chart.chartScrollbar = null;
                        $scope.chart.startDuration = null;
                        for(var i = 0; i < $scope.chart.graphs.length; i ++){
                            $scope.chart.graphs[i].balloonText = '';
                            $scope.chart.graphs[i].visibleInLegend = false;
                        }
                        delete $scope.chart.exportConfig

                    }
                    $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
                    $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); })
                    $scope.chart.write("chartdiv");
                    if(switched) $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    //if(self.compare_to)  $scope.addGraph(self.compare_to);
                });
            };

            $scope.$watch('lastSeason', function(newval){
                if(newval)
                $scope.createRadar($scope.radarPlayers, newval)
            });

            $scope.getPlayerData = function(){
                self.loader = true;
                $http.get(url + '?group_by=season')
                    .success(function(data, status, headers) {
                        if(data.is_limited) $scope.limited = true;
                        self.locale = headers()['content-language']; // determine language locale
                        $scope.localeObject = LocaleFactory['locale_'+self.locale]; // set locale object to use in js
                        $scope.dataBySeason = data;
                        $scope.currentPlayerObject.dataBySeason = data;
                        self.data = data; //for table view
                        self.loader = false;
                    }).then(function(){
                        //$scope.playersToCompare.push(playerObject);
                        if(self.coach){
                            $scope.getCoachData();
                        }
                        else if(self.club) {
                            $scope.getClubData();
                        }
                        else {
                            self.list();
                        }
                    })
            };
            $scope.getPlayerDataByMonth = function(){
                var deferred = $q.defer();
                if($scope.dataByMonth != null) deferred.resolve(true)
                else{
                    self.loader = true;
                    $http.get(url + '?group_by=month')
                        .success(function(data){
                            self.loader = false;
                            $scope.dataByMonth = data;
                            $scope.currentPlayerObject.dataByMonth = data;
                            deferred.resolve(true);
                        })
                }
                return deferred.promise;
            }

            $scope.getCoachData = function(){
                if(self.coach == null) return;
                var params = '?group_by=season&coach=' + self.coach;
                self.loader = true;
                $http.get(url + params)
                .success(function(data) {
                    $scope.coachData = data;
                    self.loader = false;
                    self.list();
                })
            };

            $scope.getClubData = function(){
                if(self.club == null) return;
                var params = '?group_by=season&club=' + self.club;
                self.loader = true;
                $http.get(url + params)
                    .success(function(data) {
                        $scope.clubData = data;
                        self.loader = false;
                        self.list();
                    })
            };

            $scope.selectedRadarFields = [{ // default radar fields we use
                field: "goals"
            }, {
                field: "points"
            }, {
                field: "assists"
            }, {
                field: "plus_minus"
            }];

            $scope.$watch('selectedRadarFields', function(newval){
                if(newval && $scope.lastSeason){
                    $scope.createRadar($scope.radarPlayers, $scope.lastSeason, null, $scope.selectedRadarFields)
                }
            }, true);

            $scope.createRadar = function(players, season, sum, selectedRadarFields){ // function to create radar chart for one or multiple players
                $scope.RadarChart = new RadarChartFactory.PlayerRadarChart();
                $scope.RadarChart.setSelectedRadarFields(selectedRadarFields);
                $scope.RadarChart.create(players, $scope.dataBySeason, season, sum).then(function(){
                    $scope.playerSeasons = $scope.RadarChart.seasons;
                    $scope.RadarChart.draw();
                });
            };

            $scope.getPlayerData();
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

    var KHL_NEWEST_FIELDS = ['shots', 'pis__avg', 'shots__avg', 'faceoff', 'winfaceoff', 'winfaceoff_p__avg', 'gamingtime__avg', 'change_count__avg'];
    var AVERAGE_AVAILABLE_FIELDS = ['goals', 'assists', 'points', 'plus_minus', 'penalty_time'];

    function generateChartData(data, field, groupBy) {
        var chartData = {};
        chartData.groupBy = groupBy;
        chartData.data = [];
        var dates = data.map(function(e){
            return (e['date'] != null) ? new Date(e['date']) : new Date(e['season']['end_date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        for(var i = 0; i< dates.length; i++){
            if(!(_.contains(KHL_NEWEST_FIELDS, field) && dates[i].getFullYear() <= 2008))
                chartData.data.push({
                    date: dates[i],
                    values: values[i],
                    count: count[i],
                    percentage: (field === 'count') ? undefined : (count[i] === 0) ? undefined : Math.round(parseFloat(values[i]/realCount[i])*1000)/1000
                });
        }

        return chartData;

    }

    function populateChartData(initialData, data, field, localeObject, playerObject){
        var chartData = initialData;
        var dates = data.map(function(e){
            return (e['date'] != null) ? new Date(e['date']) : new Date(e['season']['end_date']);
        });
        var values = data.map(function(e){ return e[field]});
        var count = data.map(function(e){ return Math.ceil(e['count']/10)});
        var realCount = data.map(function(e){ return e['count']});
        _.each(dates, function(date, index){
            if(!(_.contains(KHL_NEWEST_FIELDS, field) && date.getFullYear() <= 2008)){
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
        var mergedJSON = source2;
        for (var attrname in source1) {
            if(mergedJSON.hasOwnProperty(attrname)) {
                if ( source1[attrname]!=null && source1[attrname].constructor==Object ) {
                    mergedJSON[attrname] = mergeJSON(source1[attrname], mergedJSON[attrname]);
                }
            } else {
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
        graph.title = title;
        graph.valueField = "values" + id;
        graph.bullet = "none";
        graph.hideBulletsCount = 30;
        graph.bulletBorderThickness = 1;
        graph.lineColor = color;
        graph.fillColors = color;
        graph.fillAlphas = 1;
        graph.lineThickness = 0;
        graph.type = 'column';
        if(_.contains(AVERAGE_AVAILABLE_FIELDS, field))
        graph.balloonText = '<span class="graph-span">'+localeObject.fieldNames[field].shortName + ': [[values' + id +']]</span> <br><span class="percentage">' + localeObject.fieldNames[field].shortName +'/'+ localeObject.fieldNames['count'].shortName+': '+'[[percentage'+ id +']]</span>';

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

    function getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
angular.module('Sportomatics')
    .controller('PlayerPartnersController', function($scope, $rootScope, $timeout, $http, $location){
        $scope.player_id = $('#player-id').val();
        $scope.rate_by_param = parseInt($location.search()['rate_by']);
        $scope.is_playing_param = parseInt($location.search()['is_playing']);

        $scope.params = {
            rate_by: $scope.rate_by_param || '',
            is_playing: ''
        };

        $scope.go = function(href){
            var path = href;
            if($scope.rate_by_param) path+= "#?rate_by=" + $scope.rate_by_param;
            console.log(path);
            window.location.href = path;
        };
        $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
        $scope.increaseLimit = function(index){
            $scope.limit[index] += 4;
        };
        $scope.setPlaying = function(value){
            $scope.params['is_playing'] = value;
            $scope.is_playing_param = value;
            $location.search('is_playing', value);
            $scope.getPartners();
        };
        $scope.setRateBy = function(value){
            $scope.params['rate_by'] = value;
            $scope.rate_by_param = value;
            $location.search('rate_by', value);
            $scope.getPartners();
        };
        $scope.getPartners = function(){
            $http.get('/static/json/countries-json-ru-codes.json')
                .success(function(data){
                    $scope.countryCodes = data;
                }).then(function(){
                    $scope.url = $('#url').val();
                    if(($scope.params && $scope.params.is_playing) || ($scope.params && $scope.params.rate_by)){
                        $scope.url += '?'+ $.param($scope.params)
                    }
                    $scope.loader = true;
                    $http.get($scope.url)
                        .success(function(data){
                            _.each(data, function(object){
                                _.each(object.players, function(player){
                                    if(player.citizenship){
                                        if(!player.citizenship.code){
                                            _.each($scope.countryCodes, function(country){
                                                if(player.citizenship.title)
                                                if(country.name === player.citizenship.title){
                                                    player.citizenship.code = country.code;
                                                }
                                            })
                                        }
                                    }
                                })
                            });
                            $scope.limit = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4];
                            $scope.loader = false;
                            if($scope.params.rate_by){
                                $scope.playersBySeasonTime = data;
                            } else {
                                $scope.playersBySeasonTime = [];
                                $scope.playersBySeasonCount = _.filter(_.sortBy(data, 'seasons_count').reverse(), function(el){ return el.seasons_count > 0});
                            }
                        })
                });
        };
        $scope.getPartners();

    });
angular.module('Sportomatics').controller('PlayersSearchController', [
  '$http', '$scope', '$location', 'PlayersSearchService', function($http, $scope, $location, PlayersSearchService) {
    this.getUnchecker = function(isDefault, defaultValue) {
      return function() {
        if ((isDefault && $(this).attr('value') !== defaultValue) || (!isDefault && $(this).attr('value') === defaultValue)) {
          return $(this).attr('checked', false);
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
      'data': null,
      'isClubsVisible': false
    };
    $scope.PlayerPartnersPopupShow = function(e, event) {
      var popup, url;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length) {
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, this.player.pk)).success(function(data) {
          $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': event.pageX,
          'top': event.pageY
        });
      }
    };
    $scope.lineCheck = function(e) {
      var defaultValue, isDefault;
      defaultValue = '';
      isDefault = $(e).attr('value') === defaultValue;
      if ($(e).is(':checked')) {
        $('input[name="line"]').each(this.getUnchecker(isDefault, defaultValue));
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
    };
    $scope.contractCheck = function(e) {
      var isDefault;
      isDefault = $(e).attr('value') === '';
      if ($(e).is(':checked')) {
        $('input[name="contract"]').each(this.getUnchecker(isDefault, ''));
      }
    };
    $scope.setPlayersFilter = function(obj) {
      PlayersSearchService.setPlayersFilter($scope, obj);
    };
    $scope.setClubsFilter = function(obj) {
      PlayersSearchService.setClubsFilter($scope, obj);
    };
    $scope.setSeason = function(e) {
      if ($(e).val()) {
        $location.search('season', $(e).val());
      } else {
        $location.search('season', null);
      }
      $scope.params = $location.search();
    };
    PlayersSearchService.loadCountries($scope, $location, PlayersSearchService.search);
  }
]);

angular.module('Sportomatics').controller('ProfileController', [
  '$http', '$scope', 'tags', function($http, $scope, tags) {
    $scope.tags = tags;
    $scope.user = {};
    $scope.config = {
      'headers': {
        'X-CSRFToken': null
      }
    };
    $scope.loadCountries = function(query) {
      return $scope.tags.loadCountries($scope.countriesURL, query);
    };
    $scope.loadClubs = function(query) {
      return $scope.tags.loadClubs($scope.clubsURL, query);
    };
    $scope.setAvatar = function(files, csrf_token) {
      var config, fd;
      fd = new FormData();
      fd.append('avatar', files[0]);
      config = {
        'headers': {
          'X-CSRFToken': csrf_token,
          'Content-Type': void 0
        },
        'withCredentials': true,
        'transformRequest': angular.identity
      };
      $http.patch(this.profileURL, fd, config).success(function(data) {
        $('#id_avatar').attr('src', data.avatar);
        $('.user-avatar-hex2').css('background-image', 'url(' + data.avatar + ')');
      }).error(function(data) {});
    };
    $scope.save = function() {
      var club, country;
      $scope.user.clubs = (function() {
        var i, len, ref, results;
        ref = $scope.clubs;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          club = ref[i];
          results.push(club.pk);
        }
        return results;
      })();
      $scope.user.countries = (function() {
        var i, len, ref, results;
        ref = $scope.countries;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          country = ref[i];
          results.push(country.pk);
        }
        return results;
      })();
      $http.patch($scope.profileURL, $scope.user, $scope.config).success(function(data) {
        $scope.user = data;
      });
    };
    $scope.confirmEmail = function() {
      $http.post($scope.emailConfirmationURL, {}, $scope.config).success(function(data) {});
    };
  }
]);

angular.module('Sportomatics').controller('RegistrationController', [
    '$http', '$scope','$templateCache','$q', '$cookies', '$location', 'tags', 'ProfileService',
    function($http, $scope, $templateCache, $q, $cookies, $location, tags, ProfileService) {
        $scope.$location = $location;
        $scope.tags = tags;

        if (($location.search().uidb64 && $location.search().token) || $location.search().remember) {
            $scope.selectedType = 'remember';
        } else {
            $scope.selectedType = 'social';
        }

        $scope.urls = {};
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
        $scope.countries = [];
        $scope.clubs = [];

        $scope.setAvatar = ProfileService.setAvatar;

        $scope.loadCountries = function(query) {
            console.log($scope);
            return $scope.tags.loadCountries($scope.urls.countries, query);
        };

        $scope.loadClubs = function(query) {
            return $scope.tags.loadClubs($scope.urls.clubs, query);
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
            var config = {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken
                },
            },
            data;

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
                        data = {
                            username: $scope.user.email,
                            password: $scope.user.password,
                            email_notification: $scope.subscribe
                        };
                        localStorage.setItem('sportomatics_registrationPersonalInfo', JSON.stringify($scope.personal));
                        if ($scope.userCreated) {
                            $http.patch($scope.urls.profile, data, config).success(function(data) {
                                $scope.errors = {};
                                $scope.currentStep += 1;
                                $scope.currentStepTemplate = 'step' + $scope.currentStep;
                            }).error(function(data) {
                                $scope.errors = data;
                            });
                        } else {
                            $http.post($scope.urls.registration, data, config).success(function(data) {
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
                        data = {
                            fio: $scope.personal.name,
                            name_visible: !$scope.personal.hideName,
                            website: $scope.personal.website
                        };
                        $http.patch($scope.urls.profile, data, config).success(function(data) {
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
                        data = {
                            sport_hockey: $scope.preferencesSports.hockey,
                            sport_football: $scope.preferencesSports.football,
                            sport_basketball: $scope.preferencesSports.basketball,
                            countries: [],
                            clubs: []
                        };
                        $.each($scope.countries, function() {
                            data.countries.push(+this.pk);
                        });
                        $.each($scope.clubs, function() {
                            data.clubs.push(+this.pk);
                        });
                        $http.patch($scope.urls.profile, data, config).success(function(data) {
                            document.location = $scope.urls.redirect;
                        });
                    }
                    break;
            }
        };
        $scope.nextStep = function(skip){
            if (skip) {
                if ($scope.currentStep !== 3) {
                    $scope.currentStep += 1;
                    $scope.currentStepTemplate = 'step' + $scope.currentStep;
                } else {
                    document.location = $scope.urls.redirect;
                }
            } else {
                if($scope.checkStep()) {
                    $scope.saveStep();
                } else {
                    alert('Введите все данные');
                }
            }
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
            var data = {
                email: $scope.rememberPasswordData.email
            };
            $http.post($scope.urls.passwordReset, data, $scope.getAjaxConfig()).success(function(data) {
                $scope.rememberPasswordData.isSent = true;
                $scope.rememberPasswordData.errors = null;
            }).error(function(data) {
                $scope.rememberPasswordData.errors = data;
            });
        };
        $scope.setPassword = function() {
            var data = {
                uidb64: $location.search().uidb64,
                token: $location.search().token,
                password: $scope.rememberPasswordData.password
            };
            if ($scope.rememberPasswordData.password && $scope.rememberPasswordData.password2 &&
                   $scope.rememberPasswordData.password === $scope.rememberPasswordData.password2) {
                $http.post($scope.urls.passwordResetConfirm, data, $scope.getAjaxConfig()).success(function(data) {
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
