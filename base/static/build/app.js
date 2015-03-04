'use strict';
angular.module('Sportomatics', ['angucomplete', 'ngTagsInput', 'ui.router', 'ngResource'])
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
            console.log('player call ');
            $('.breadcrumb').after($("<div class='inline-block min-photo-container'></div>"));
            $('#player-card-avatar').addClass('clipped-img');
            $('#player-card-avatar').detach().appendTo($('.min-photo-container').css('margin-left', (1000 - 110 - breadcrumbWidth*2 - playerNameWidth)/2 + 'px', 'important'));
            $('.min-photo-container').after($('#player-card-name').addClass('inline-block player-card-name-inner'));
            $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important').css('box-shadow', '0 4px 2px -2px gray','important'));
            $('.page-container').css('margin-top', '68px');
            scrolledAfterPlayer = true;
        } else if (topPlayer && y < topPlayer && scrolledAfterPlayer){
            console.log('player reverse call ');
            $('#player-card-amplua').before($('#player-card-name').removeClass('inline-block player-card-inner'));
            $('#player-card-desc').before($('#player-card-avatar').removeClass('clipped-img').css('margin-left', '0'));
            $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important').css('box-shadow', '0','important'));
            $('.page-container').css('margin-top', '0px');
            $(".min-photo-container").remove();
            scrolledAfterPlayer = false;
        }
        //team card
        if (topSecondary && y >= topSecondary && !scrolledAfterTeamInfo && !$('#player-card-block').length){
            console.log('team info call ');
            $('.page-container').css('margin-top', '114px');
            $('.my-team-btn').css('margin-top', '4px');
            $('.breadcrumb').after($('#team-logo')).addClass('inline-block breadcrumb-inner');
            $("#team-logo").after($('#team-name')).addClass('team-logo-inner inline-block').css('margin-left', teamLogoMargin + 'px', 'important');
            $('#team-name').addClass('team-name-inner inline-block');
            $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important').css('box-shadow', '0 4px 2px -2px gray','important'));
            scrolledAfterTeamInfo = true;
        } else if (topSecondary && y < topSecondary && scrolledAfterTeamInfo){
            console.log('team info reverse call ');
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
        console.log('player call ');
        $('.breadcrumb').after($("<div class='inline-block min-photo-container'></div>"));
        $('#player-card-avatar').addClass('clipped-img');
        $('#player-card-avatar').detach().appendTo($('.min-photo-container').css('margin-left', (1000 - 110 - breadcrumbWidth*2 - playerNameWidth)/2 + 'px', 'important'));
        $('.min-photo-container').after($('#player-card-name').addClass('inline-block').css('font-weight', '700', 'important'));
        $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important'));
        $('.page-container').css('margin-top', '68px');
        scrolledAfterPlayer = true;
    } else if (topPlayer && y < topPlayer && scrolledAfterPlayer){
        console.log('player reverse call ');
        $('#player-card-amplua').before($('#player-card-name').removeClass('inline-block').css('margin-left', 0 + 'px', 'important'));
        $('#player-card-desc').before($('#player-card-avatar').removeClass('clipped-img').css('margin-left', '0'));
        $('.page-inner-container').before($('.page-menu').removeClass('fixed').css('margin-left', '0px', 'important').css('margin-right', '0px', 'important'));
        $('.page-container').css('margin-top', '0px');
        $(".min-photo-container").remove();
        scrolledAfterPlayer = false;
    }
    //team card
    if (topSecondary && y >= topSecondary && !scrolledAfterTeamInfo && !$('#player-card-block').length){
        console.log('team info call ');
        $('.page-container').css('margin-top', '114px');
        $('.my-team-btn').css('margin-top', '4px');
        $('.breadcrumb').after($('#team-logo')).addClass('inline-block breadcrumb-inner');
        $("#team-logo").after($('#team-name')).addClass('team-logo-inner inline-block').css('margin-left', teamLogoMargin + 'px', 'important');
        $('#team-name').addClass('team-name-inner inline-block');
        $('.search-block').after($('.page-menu').css('margin-left', '5px', 'important').css('margin-right', '5px', 'important'));
        scrolledAfterTeamInfo = true;
    } else if (topSecondary && y < topSecondary && scrolledAfterTeamInfo){
        console.log('team info reverse call ');
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
        generateSerialChart: function(data, field, chartData, locale, graphsCount){
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = chartData;
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
                categoryAxis.minorGridEnabled = true;
                categoryAxis.autoGridCount =  true;
                categoryAxis.grudCount = 12;
                categoryAxis.minHorizontalGap = 40;
                categoryAxis.gridAlpha = 0.1;
                categoryAxis.boldPeriodBeginning = false;
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.twoLineMode = true;
                categoryAxis.tickLength = 12;
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
                var currMax = Math.max.apply(Math, chartData.map(function(e){ return e['values']}));
                var currMin = Math.min.apply(Math, chartData.map(function(e){ return e['values']}));
                // first value axis (on the left)
                var valueAxis1 = new AmCharts.ValueAxis();
                valueAxis1.axisColor = "#408e3a";
                valueAxis1.axisThickness = 1;
                valueAxis1.gridAlpha = 0.1;
                valueAxis1.maximum = (currMax === 0) ? +2 : (currMax/10 > 0) ? currMax+(currMax/10)*5: currMax + currMax%10;
                valueAxis1.minimum = (currMin === 0) ? -2 : (currMin/10 > 0) ? currMin-(currMin/10)*5 : currMin - Math.abs(currMin%10);
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

                // GRAPHS
                // first graph
                for(var i = 0; i < graphsCount; i ++){
                    var graph = generateGraph(i, data[i]['title'], valueAxis1);
                    chart.addGraph(graph);
                }
                var graph1 = new AmCharts.AmGraph();

                graph1.id = "g2";
                graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                graph1.title = field;
                graph1.valueField = "values";
                graph1.bullet = "round";
                graph1.hideBulletsCount = 30;
                graph1.bulletBorderThickness = 1;
                graph1.lineColor = "#408e3a";
                graph1.lineThickness = 4;
                graph1.animationPlayed = true;
                if(field === 'goals' || field === 'assists' || field === 'points' || field === 'plus_minus' || field === 'penalty_time' )
                graph1.balloonText = '<span style="text-align: left; float: left">'+locale.fieldNames[field].shortName + ': [[values]]</span> <br><span class="percentage">' + locale.fieldNames[field].shortName +'/'+ locale.fieldNames['count'].shortName+': '+'[[percentage]]</span>';
                chart.addGraph(graph1);

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
                    text: locale.fieldNames[field].fullName.toUpperCase()
                }];

                deferred.resolve(chart);
            });
            return deferred.promise; //метод возвращает промис и ждет когда выполнится resolve, а он выполнится после полного создания графика
        }
    }
}])
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
                        fullName: 'Штрафное время'
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
                    }
                },
                buttonNames: {
                    month: 'По месяцам',
                    season: 'По сезонам'
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
    this.loadCountries = function($scope, callback) {
        var url = $('#LeagueListLink').attr('href');
        if (url) {
            $http.get(url).success(function(data) {
                $scope.countries = data;
                if ($scope.countries.length) { // has countries
                    if (Array.isArray($scope.sparams.countriesSelected) &&
                        $scope.sparams.countriesSelected.length === 0) { // array is expected
                        $scope.sparams.countriesSelected = [String($scope.countries[0].pk)];
                    } else {
                        $scope.sparams.countriesSelected = $scope.countries[0].pk;
                    }
                    if ($scope.countries[0].league_set.length) { // has leagues
                        if (Array.isArray($scope.sparams.leaguesSelected) &&
                            $scope.sparams.leaguesSelected.length === 0) { // array is expected
                            $scope.sparams.leaguesSelected = [String($scope.countries[0].league_set[0].pk)];
                        } else {
                            $scope.sparams.leaguesSelected = $scope.countries[0].league_set[0].pk;
                        }
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

    this.getLeagues = function(countries, countriesSelected) {
        var result = [];
        $.each(countriesSelected, function() {
            var pk = this;
            $.each(countries, function() {
                if (this.pk == pk) {
                    result = result.concat(this.league_set);
                }
            });
        });
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
            if ($scope.params.order_by === order_by) { // same field -> reverse
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

            if (!$scope.sparams.leaguesLoaded) {
                $scope.sparams.leaguesLoaded = true;
                if ($scope.params.league) {
                    if (Array.isArray($scope.params.league)) {
                        $scope.sparams.leaguesSelected = $scope.params.league;
                    } else {
                        $scope.sparams.leaguesSelected = [$scope.params.league];
                    }
                }
            }
            $scope.$location.search('league', $scope.sparams.leaguesSelected);

            $scope.params = $scope.$location.search();

            params += '&order_by=' + ($scope.params.reversed === 'true' ? '-' : '') +
                ($scope.params.order_by || '["%s_lastname","%s_name"]');

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

        if (!$scope.countries) {
             this.loadCountries($scope, f);
        } else {
            f($scope);
        }
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

angular.module('Sportomatics').service('tags', ["$q", "$filter", function($q, $filter) {
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
}]);
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
    return $resource("{% url 'api:hockey:cip_list' %}", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
}])
.factory('ArenaInstaPhoto', ["$resource", function($resource){
    return $resource("{% url 'api:hockey:cip_list' %}", {}, {
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
.controller('PhotosController', ["$scope", "ClubInstaPhoto", "InstagramUser", "$resource", function($scope, ClubInstaPhoto, InstagramUser, $resource){

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
        $scope.photos = [];
        $scope.next_page = 1;
        $scope.currentIndex = 0;

        $scope.getPage = function(){
            var get_params = {
                page: $scope.next_page,
                min_id: 0,
                max_id: 10000000,
                club: $scope.club_id
            };
            $scope.photoDataLoader = true;
            ClubInstaPhoto.query(get_params).$promise.then(function (data) {
                $scope.photoDataLoader = false;
                $.each(data.results, function (index, value) {
                    $scope.photos.push(value)
                });
                setTimeout(function(){
                    playerClubsMasonry.imagesLoaded(function(){
                        playerClubsMasonry.masonry({
                            itemSelector: '.item',
                            gutterWidth: 20
                        })
                    });
                }, 100);
                $scope.next_page = data.next_page;
                if (!$scope.next_page && $('#nextpagebutton').length) {
                    $('#nextpagebutton').remove();
                }
            });
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
                //$scope.PhotoPopup.data = ClubInstaPhoto.get({id:id}, function(photo) {
            console.log(index)
            $scope.currentIndex = index;
            var photo = $scope.photos[index];
           // console.log($scope.photos[index]);
            $scope.PhotoPopup.data = $scope.photos[index];
            $scope.photoDataLoader = true;
                $scope.PhotoPopup.instagramUser = InstagramUser.get({id: photo.photo.instagram_user}, function(){
                    $scope.photoDataLoader = false;
                    $scope.PhotoPopup.userStr = photo.photo.user_str;
                    $(".instagram-user-str").val(photo.photo.user_str);
                    $scope.PhotoPopup.data.players = '';
                    /*if(photo.arena){
                     $scope.PhotoPopup.arena = Arena.get({id:photo.arena}, function(arena){
                     $.each(arena.club_set, function(index, value){
                     Club.get({id:value}, function(club){
                     $scope.PhotoPopup.clubSet.push(club);
                     })
                     })
                     })
                     }*/
                    var params = {date:photo.photo.created, arena:photo.arena};
                    $scope.lastSucceedIndex = index;
                    /*}, function(a){
                     console.log(a)
                     });*/
                    $scope.PhotoPopup.index = index;
                    $('.overlay-black').css('visibility', 'visible');
                    $('.photo-popup').show();
                });

        };
        $scope.nextPhoto = function(){
            var index = $scope.PhotoPopup.index + 1;
            if($scope.photos[index]){
                $scope.PhotoPopup.domIndex = $scope.photos[index].id;
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'next');
            }
        };
        $scope.prevPhoto = function(){
            var index = $scope.PhotoPopup.index - 1;
            if($scope.photos[index]){
                $scope.PhotoPopup.domIndex = $scope.photos[index].id;
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'prev');
            }
        };

        $scope.getPage();
}])
angular.module('Sportomatics')
.controller('PlayerCardIndicatorsController', ["$http", "$scope", "$timeout", "AmChartsFactory", "ChartFactory", "zoomData", "LocaleFactory", "$state", "$location", "$q", function($http, $scope, $timeout, AmChartsFactory, ChartFactory, zoomData, LocaleFactory, $state, $location, $q) {
    //http://www.amcharts.com/lib/images/

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
    //var chart = null;
    $scope.addGraph = function (url) {
        var params = 'group_by=month';
        if (self.club !== null) {
            params += '&club=' + self.club;
        }
        if (self.coach !== null) {
            params += '&coach=' + self.coach;
        }
        $http.get(url + '?' + params)
            .success(function(data) {
                $scope.dataByMonth = data;
                params = 'group_by=season';
                if (self.club !== null) {
                    params += '&club=' + self.club;
                }
                if (self.coach !== null) {
                    params += '&coach=' + self.coach;
                }
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        $scope.dataBySeason = data;
                        self.loader = false;
                    }).then(function(){
                        var data;
                        data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
                        var newChartData = updatedChartData($scope.chart, $scope.chartData, data.results, self.field);
                        $scope.chart.dataProvider = newChartData.chartData;
                        $scope.chart.addGraph(newChartData.newGraph);
                        $scope.chart.validateData();
                    })
            })
    };
    $scope.isDisabled = function(season){
        return (self.field === 'shots' || self.field === 'pis__avg' || self.field === 'shots__avg' || self.field === 'faceoff' || self.field === 'winfaceoff' || self.field === 'winfaceoff_p__avg' || self.field === 'gamingtime__avg' || self.field === 'change_count__avg') && (parseInt(season.end_date.split('-')[0]) < 2009 );
    };
    $scope.setGroupBy = function(groupby){
        self.groupBy = groupby;
        self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
        $scope.onSeason = false;
        self.list();
        $timeout(function(){}, 500);
    };
    $scope.unload = function(){

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
        var data;
        data = (self.groupBy === 'month') ?  $scope.dataByMonth : $scope.dataBySeason;
        var datesArray = (self.groupBy === 'month') ? data.results.map(function(e){ return new Date(e['date']) }) : data.results.map(function(e){ return new Date(e['season']['end_date']) });
        var min = Math.min.apply(null, datesArray);
        var max = Math.max.apply(null, datesArray);
                if(switched){
                    var zoomStart = (new Date(zoomData.startDate).getTime() >= min) ? new Date(zoomData.startDate) : new Date(min);
                    var zoomEnd = (new Date(zoomData.endDate).getTime() <= max) ? new Date(zoomData.endDate) : new Date(max);
                }
                $scope.chartData = generateChartData(data.results, self.field);
                ChartFactory.generateSerialChart(data.results, self.field, $scope.chartData, $scope.localeObject).then(function(chart){
                    $scope.chart = chart;
                    // CURSOR
                    var chartCursor = new AmCharts.ChartCursor();
                    chartCursor.cursorAlpha = 1;
                    chartCursor.cursorColor = "#8ebd5d";
                    chartCursor.categoryBalloonFunction = function(value){
                        if(self.groupBy === 'month'){
                            return $scope.localeObject.monthNames[value.getMonth()] + ' ' + value.getFullYear();
                        } else {
                            return $scope.localeObject.words.season + ' ' +  (value.getFullYear()-1).toString().substr(2, 2) + '/' + value.getFullYear().toString().substr(2, 2)
                        }
                    };
                    $scope.chart.addChartCursor(chartCursor);

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
                    $scope.chart.write("chartdiv");
                    $scope.chart.addClassNames = false;
                    if(switched){
                        $scope.chart.zoomToDates(zoomStart, zoomEnd);
                    }
                });
            //});
    };
    $scope.getPlayerData = function(){
        var group = 'month';
        var params = 'group_by=' + group;
        self.loader = true;
        $http.get(url + '?' + params)
            .success(function(data, status, headers) {
                self.locale = headers()['content-language'];
                $scope.localeObject = LocaleFactory['locale_'+self.locale];
                self.fieldName = $scope.localeObject.fieldNames[self.field].fullName;
                $scope.dataByMonth = data;
                group = 'season';
                params = 'group_by=' + group;
                $http.get(url + '?' + params)
                    .success(function(data, status, headers) {
                        $scope.dataBySeason = data;
                        self.data = data; //for table view
                        self.loader = false;
                    }).then(function(){
                        self.list();
                        console.log($scope.dataByMonth);
                        console.log($scope.dataBySeason);
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
                    if(toList) self.list();
                })
        }
    };

    $scope.getPlayerData();
    $scope.getCoachData(true);
    $scope.getClubData(true);

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
function generateChartData(data, field) {
    var chartData = [];
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
        chartData.push({
            date: dates[i],
            values: values[i],
            count: count[i],
            percentage: (field === 'count') ? undefined : (count[i] === 0) ? undefined : Math.round(parseFloat(values[i]/realCount[i])*1000)/1000
        });
    }
    return chartData;
}
function updatedChartData(chart, initialData, data, field){

    var chartData = initialData;
    console.log(chartData);
    var dates = data.map(function(e){
        if(e['date'] == null){
            return new Date(e['season']['end_date']);
        }
        return new Date(e['date']);
    });
    var values = data.map(function(e){ return e[field]});
    var count = data.map(function(e){ return Math.ceil(e['count']/10)});
    _.each(dates, function(date, index){
        var pushed = false;
        _.each(chartData, function(e){
            if(e['date'] === date){
                e['values1'] = values[index];
                e['count1'] = count[index];
                pushed = true;
            }
        });
        if (!pushed) {
            chartData.push({
                date: date,
                values1: values[index],
                count1: count[index]
            });
        }
    });
    console.log(chartData);
    var graph = new AmCharts.AmGraph();
    graph.valueAxis = chart.valueAxes[0]; // we have to indicate which value axis should be used
    graph.title = '926';
    graph.valueField = 'values'+1;
    graph.bullet = "round";
    graph.hideBulletsCount = 30;
    graph.bulletBorderThickness = 1;
    graph.lineColor = '#000000'; //TODO: add more colors
    graph.lineThickness = 4;
    return {
        chartData: chartData,
        newGraph: graph
    };
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
    $scope.countries = null;
    $scope.loader = false;

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

    PlayersSearchService.search($scope);
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
angular.module('Sportomatics')
    .controller('RegistrationController', ['$http', '$scope','$templateCache','$q','tags', function($http, $scope, $templateCache, $q, tags) {
        $scope.selectedType = 'social';
        $scope.user = {};
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
                    return $scope.user.login && $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);

                case 2:
                    return true;
            }
            return false;
        };
        $scope.comparePasswords = function(){
            if($scope.user.password && $scope.user.password2){
                if($scope.user.password == $scope.user.password2) {
                    $scope.passwordsMatch = true;
                    return true;
                }
            }
            $scope.passwordsMatch = false;
            return false;
        };
        $scope.saveStep = function(){
            switch($scope.currentStep){
                case 1:
                    if($scope.personalInfo){
                        var userToLocalStorage;
                        angular.copy($scope.user, userToLocalStorage);
                        userToLocalStorage.password = undefined;
                        userToLocalStorage.password2 = undefined;
                        localStorage.setItem('sportomatics_registrationUserInfo', JSON.stringify(userToLocalStorage));
                    }
                    break;
                case 2:
                    if($scope.personalInfo){
                        localStorage.setItem('sportomatics_registrationPersonalInfo', JSON.stringify($scope.personal));
                    }
                    break;
                case 3:
                    if($scope.e()){

                    }
                    break;
            }
        };
        $scope.nextStep = function(){
            if($scope.checkStep()) {
                $scope.currentStep += 1;
                $scope.currentStepTemplate = 'step'+ $scope.currentStep;
                $scope.saveStep();
            }
            else alert('Введите все данные');
        };
        $scope.prevStep = function(){
            $scope.currentStep -= 1;
            $scope.currentStepTemplate = 'step'+ $scope.currentStep;
        }
    }]);
        function validateEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }