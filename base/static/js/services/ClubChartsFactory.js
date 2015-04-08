angular.module('Sportomatics').factory('ClubChartsFactory', function($q, $timeout, AmChartsFactory, zoomData) {
  var PlayerClubsChart;
  PlayerClubsChart = (function() {
    function PlayerClubsChart(data1, graphs1) {
      this.data = data1;
      this.graphs = graphs1;
    }

    PlayerClubsChart.prototype.init = function() {};

    PlayerClubsChart.prototype.setData = function(data1) {
      this.data = data1;
    };

    PlayerClubsChart.prototype.create = function(field, chartData, localeObject, graphs, player) {
      var chart, deferred;
      deferred = $q.defer();
      chart = void 0;
      AmChartsFactory.ready().then(function() {
        var balloons, categoryAxis, chartCursor, chartScrollbar, currMax, currMin, data, legend, valueAxis1;
        data = chartData.data;
        chart = new AmCharts.AmSerialChart;
        chart.pathToImages = 'http://www.amcharts.com/lib/images/';
        chart.dataProvider = data;
        chart.categoryField = 'end_date';
        chart.cursorColor = '#DADADA';
        chart.startDuration = 0.5;
        chart.startEffect = 'easeOutSine';
        chart.addClassNames = true;
        chart.depth3D = 60;
        chart.angle = 30;
        chart.exportConfig = {
          'menuTop': '45px',
          'menuRight': '5px',
          'menuItems': [
            {
              'icon': 'http://www.amcharts.com/lib/3/images/export.png',
              'format': 'png'
            }
          ]
        };
        chart.addListener('dataUpdated', zoomChart);
        chart.addListener('zoomed', function(chart) {
          zoomData.startDate = chart.startDate;
          zoomData.endDate = chart.endDate;
        });

        /*chart.addListener 'rollOverGraph', (event) ->
            $('.balloon-value').each (index, element) ->
                field = $(element).attr('id').split('-')[1]
                $('#block-'+field).remove() if $(element).text().length is 0
                console.log field
                #$('#block-'+field).remove
         */
        categoryAxis = chart.categoryAxis;
        categoryAxis.parseDates = true;
        categoryAxis.minPeriod = chartData.groupBy === 'month' ? 'MM' : 'YYYY';
        categoryAxis.equalSpacing = true;
        categoryAxis.minHorizontalGap = 40;
        categoryAxis.gridAlpha = 0;
        categoryAxis.boldPeriodBeginning = false;
        categoryAxis.axisColor = '#DADADA';
        categoryAxis.markPeriodChange = false;
        categoryAxis.dateFormats = [
          {
            period: 'MM',
            format: 'MMM'
          }, {
            period: 'YYYY',
            format: 'YYYY'
          }
        ];
        categoryAxis.labelFunction = function(valueText, date, categoryAxis) {
          var endDate, startDate, value;
          value = new Date(date);
          if (chartData.groupBy == 'season') {
            endDate = valueText.substr(2, 2);
            startDate = endDate == '00' ? '99' : (parseInt(endDate) - 1).toString();
            if (startDate.length == 1) {
              startDate = '0' + startDate;
            }
            return startDate + '/' + endDate;
          }
          if (valueText == 'Jan') {
            return localeObject.monthNames[value.getMonth()] + '\n' + value.getFullYear();
          }
          return localeObject.monthNames[value.getMonth()];
        };
        currMax = Math.max.apply(Math, data.map(function(e) {
          return e['values'];
        }));
        currMin = Math.min.apply(Math, data.map(function(e) {
          return e['values'];
        }));
        valueAxis1 = new AmCharts.ValueAxis();
        valueAxis1.axisColor = '#408e3a';
        valueAxis1.axisThickness = 1;
        valueAxis1.stackType = "regular";
        valueAxis1.axisAlpha = 0;
        valueAxis1.gridAlpha = 0;
        chart.addValueAxis(valueAxis1);
        if (graphs && graphs.length) {
          balloons = '<div class=\'inline-block text-left\'><p style=\'text-align: left;\'><span style=\'font-size:14px; color:#000000;\'><b>' + localeObject.fieldNames[field].fullName + '</b></span></p>';
          _.each(graphs, function(graph, index) {
            balloons += createBalloon(graph.valueField, graph.title);
            graph.valueAxis = valueAxis1;
          });
          _.each(graphs, function(graph, index) {
            graph.lineColorField = 'lineColor';
            graph.fillColorsField = 'lineColor';
            chart.addGraph(graph);
          });
        }
        chartScrollbar = new AmCharts.ChartScrollbar;
        chartScrollbar.autoGridCount = true;
        chartScrollbar.color = '#000000';
        chart.addChartScrollbar(chartScrollbar);
        legend = new AmCharts.AmLegend;
        legend.marginLeft = 110;
        legend.useGraphSettings = true;
        chart.addLegend(legend);
        chart.allLabels = [
          {
            align: 'center',
            y: 60,
            alpha: 0.7,
            bold: true,
            text: localeObject.fieldNames[field].fullName.toUpperCase()
          }
        ];
        chartCursor = new AmCharts.ChartCursor;
        chartCursor.cursorAlpha = 1;
        chartCursor.cursorColor = '#8ebd5d';
        chartCursor.oneBalloonOnly = true;
        chartCursor.categoryBalloonFunction = function(value) {
          if (chartData.groupBy === 'month') {
            return localeObject.monthNames[value.getMonth()] + ' ' + value.getFullYear();
          } else {
            return localeObject.words.season + (value.getFullYear() - 1).toString().substr(2, 2) + '/' + value.getFullYear().toString().substr(2, 2);
          }
        };
        chart.addChartCursor(chartCursor);
        deferred.resolve(chart);
      });
      return deferred.promise;
    };

    return PlayerClubsChart;

  })();
  return {
    PlayerClubsChart: PlayerClubsChart
  };
});
