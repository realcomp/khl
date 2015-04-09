angular.module('Sportomatics').factory('PieChartFactory', function($q, $timeout, AmChartsFactory, zoomData) {
  var PlayerClubsChart;
  PlayerClubsChart = (function() {
    function PlayerClubsChart(data, graphs) {
      this.data = data;
      this.graphs = graphs;
    }

    PlayerClubsChart.prototype.init = function() {};

    PlayerClubsChart.prototype.setData = function(data) {
      this.data = data;
    };

    PlayerClubsChart.prototype.create = function(chartData) {
      var deferred;
      deferred = $q.defer();
      AmChartsFactory.ready().then(function() {
        var balloonText, chart;
        chart = new AmCharts.AmPieChart();
        chart.dataProvider = chartData;
        chart.titleField = "clubTitle";
        chart.valueField = "value";
        chart.outlineColor = "#FFFFFF";
        chart.outlineAlpha = 0.8;
        chart.outlineThickness = 2;
        chart.urlField = "clubUrl";
        chart.startDuration = 0.3;
        balloonText = "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>";
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
