angular.module('Sportomatics').factory('IndicatorsFactory', function() {
  var PlayerIndicatorsChart;
  PlayerIndicatorsChart = (function() {
    function PlayerIndicatorsChart() {
      this.field = 'count';
      this.dataType = 'graph-serial';
    }

    PlayerIndicatorsChart.prototype.setField = function(field) {
      this.field = field;
    };

    PlayerIndicatorsChart.prototype.getField = function() {
      return this.field;
    };

    PlayerIndicatorsChart.prototype.setDataType = function(dataType) {
      this.dataType = dataType;
    };

    PlayerIndicatorsChart.prototype.getDataType = function() {
      return this.dataType;
    };

    return PlayerIndicatorsChart;

  })();
  return {
    PlayerIndicatorsChart: PlayerIndicatorsChart
  };
});
