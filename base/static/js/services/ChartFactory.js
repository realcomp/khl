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

                var balloon = new AmCharts.AmBalloon();
                balloon.maxWidth = 300;
                if(graphs && graphs.length){
                    var oneBalloon = "<p style='text-align: left;'><span style='font-size:14px; color:#000000;'><b>[[value]]</b></span></p>";
                    var balloons = "";
                    _.each(graphs, function(graph, index){
                        console.log(graph);
                        balloons+= createBalloon(graph.valueField, graph.title);
                        graph.valueAxis = valueAxis1;
                        graph.balloonText = (index < graphs.length -1 ) ? '' : balloons;
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
                //chartCursor.oneBalloonOnly = true;
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
    return "<p style='text-align: left;'><span style='font-size:14px; color:#000000;'><b>" + text + ": [[" + valueField + "]]</b></span></p>";
}