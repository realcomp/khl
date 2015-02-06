angular.module('Sportomatics')
.factory('ChartFactory', function($q, $rootScope, AmChartsFactory){


    return {
        generateSerialChart: function(data, field){
            var deferred = $q.defer();
            var chart;
            AmChartsFactory.ready().then(function () {
                console.log('abc')
                // generate some random data first
                var chartData = generateChartData(data, field);

                // SERIAL CHART
                chart = new AmCharts.AmSerialChart();
                chart.pathToImages = "http://www.amcharts.com/lib/images/";
                chart.dataProvider = chartData;
                chart.categoryField = "date";
                chart.cursorColor = "#DADADA";

                // listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener("dataUpdated", zoomChart);

                // AXES
                // category
                var categoryAxis = chart.categoryAxis;
                categoryAxis.parseDates = true; // as our data is date-based, we set parseDates to true
                categoryAxis.minPeriod = "DD"; // our data is daily, so we set minPeriod to DD
                categoryAxis.minorGridEnabled = true;
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
                var valueAxis2 = new AmCharts.ValueAxis();
                valueAxis2.position = "right"; // this line makes the axis to appear on the right
                valueAxis2.axisColor = "#FCD202";
                valueAxis2.gridAlpha = 0;
                valueAxis2.axisThickness = 2;
                chart.addValueAxis(valueAxis2);

                // third value axis (on the left, detached)
                var valueAxis3 = new AmCharts.ValueAxis();
                valueAxis3.offset = 50; // this line makes the axis to appear detached from plot area
                valueAxis3.gridAlpha = 0;
                valueAxis3.axisColor = "#B0DE09";
                valueAxis3.axisThickness = 2;
                chart.addValueAxis(valueAxis3);

                // GRAPHS
                // first graph
                var graph1 = new AmCharts.AmGraph();
                graph1.valueAxis = valueAxis1; // we have to indicate which value axis should be used
                graph1.title = self.field;
                graph1.valueField = "values";
                graph1.bullet = "round";
                graph1.hideBulletsCount = 30;
                graph1.bulletBorderThickness = 1;
                graph1.lineColor = "#408e3a";
                graph1.lineThickness = 4;
                chart.addGraph(graph1);
                // second graph
                var graph2 = new AmCharts.AmGraph();
                graph2.valueAxis = valueAxis2; // we have to indicate which value axis should be used
                graph2.title = self.field;
                graph2.valueField = "hits";
                graph2.bullet = "square";
                graph2.hideBulletsCount = 30;
                graph2.bulletBorderThickness = 1;
                //chart.addGraph(graph2);

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
                chart.addChartScrollbar(chartScrollbar);

                // LEGEND
                var legend = new AmCharts.AmLegend();
                legend.marginLeft = 110;
                legend.useGraphSettings = true;
                chart.addLegend(legend);
                deferred.resolve(chart);
            });
            return deferred.promise;
        }
    }
})
function generateChartData(data, field) {
    var chartData = [];
    var dates = data.map(function(e){
        if(e['date'] == null){
            return new Date(e['season']['start_date'].substr(0,4));
        }
        return new Date(e['date']);
    });
    var values = data.map(function(e){ return e[field]});
    for(var i = 0; i< dates.length; i++){
        console.log(dates[i])
        console.log(values[i])
        chartData.push({
            date: dates[i],
            values: values[i]
        });
    }
    return chartData;
}
// this method is called when chart is first inited as we listen for "dataUpdated" event
function zoomChart() {
    // different zoom methods can be used - zoomToIndexes, zoomToDates, zoomToCategoryValues
    //chart.zoomToIndexes(10, 20);
}