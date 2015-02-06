angular.module('Sportomatics')
.factory('ChartFactory', function($q, $rootScope, AmChartsFactory){

    return {
        generateSerialChart: function(data, field, graphsCount){
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                // generate some random data first
                var chartData = generateChartData(data, field);

                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = chartData;
                chart.categoryField = "date";
                chart.cursorColor = "#DADADA";
                chart.addClassNames = true;

                // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener("dataUpdated", zoomChart);

                // AXES
                // category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
                //categoryAxis.minorGridEnabled = true;
                categoryAxis.autoGridCount =  false;
                categoryAxis.gridAlpha = 0.1;
                categoryAxis.axisColor = "#DADADA";
                categoryAxis.twoLineMode = true;
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

                // first value axis (on the left)
                var valueAxis1 = new AmCharts.ValueAxis();
                valueAxis1.axisColor = "#408e3a";
                valueAxis1.axisThickness = 1;
                valueAxis1.gridAlpha = 0.1;
                valueAxis1.minimum = -2;
                chart.addValueAxis(valueAxis1);

                // second value axis (on the right)
                var gamesAxis = new AmCharts.ValueAxis();
                gamesAxis.position = "right"; // this line makes the axis to appear on the right
                gamesAxis.axisColor = "#408e3a";
                gamesAxis.gridAlpha = 0;
                gamesAxis.axisThickness = 0;
                gamesAxis.stackType = "regular";
                gamesAxis.maximum = 100;
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
                chart.addGraph(graph1);
                // second graph
                var distanceGraph = new AmCharts.AmGraph();
                distanceGraph.valueField = "count";
                distanceGraph.title = "games";
                distanceGraph.type = "step";
                distanceGraph.fillAlphas = 0;
                distanceGraph.lineColor = "#408e3a";
                distanceGraph.alphaField = "alpha";
                distanceGraph.lineThickness = 0;
                distanceGraph.lineAlpha = 0.3;
                distanceGraph.newStack = true;
                distanceGraph.stackable = true;
                distanceGraph.balloonText = '';
                distanceGraph.visibleInLegend = false;
                if(field !== 'count')
                chart.addGraph(distanceGraph);

                // third graph
                var graph3 = new AmCharts.AmGraph();
                graph3.valueAxis = valueAxis3; // we have to indicate which value axis should be used
                graph3.valueField = "views";
                graph3.title = "green line";
                graph3.bullet = "triangleUp";
                graph3.hideBulletsCount = 30;
                graph3.bulletBorderThickness = 1;
                //chart.addGraph(graph3);

                // CURSOR
                var chartCursor = new AmCharts.ChartCursor();
                chartCursor.cursorAlpha = 1;
                //chartCursor.fullWidth = true;
                chartCursor.cursorColor = "#8ebd5d";
                chart.addChartCursor(chartCursor);

                // SCROLLBAR
                var chartScrollbar = new AmCharts.ChartScrollbar();
                if(field !== 'count')
                chartScrollbar.graph = distanceGraph;
                chartScrollbar.autoGridCount = true;
                chartScrollbar.color = "#000000";
                chart.addChartScrollbar(chartScrollbar);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);

                deferred.resolve(chart);
            });
            return deferred.promise; //метод возвращает промис и ждет когда выполнится resolve, а он выполнится после полного создания графика
        }
    }
});
var colors = ["#26A65B", "#CF000F", "#663399", "#F9690E"];
function generateChartData(data, field) {
    var chartData = [];
    var dates = data.map(function(e){
        if(e['date'] == null){
            return new Date(e['season']['start_date'].substr(0,4));
        }
        return new Date(e['date']);
    });
    var values = data.map(function(e){ return e[field]});
    var count = data.map(function(e){ return e['count']});
    for(var i = 0; i< dates.length; i++){
        chartData.push({
            date: dates[i],
            values: values[i],
            count: count[i]
        });
    }
    return chartData;
}
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