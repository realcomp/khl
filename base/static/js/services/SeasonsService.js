angular.module('Sportomatics').service('SeasonsService', function() {
  this.isSeasonActive = function(season, pk, isFirst) {
    if (season) {
      return +season === +pk;
    } else {
      return isFirst;
    }
  };
  this.getDefaultSeason = function() {
    var e, es;
    es = $('.menu.seasons .item');
    if (es) {
      e = $(es[0]);
      if (e) {
        return e.attr('data-value');
      }
    }
  };
  this.getSeasonTitle = function(season) {
    var e, pk;
    pk = season;
    if (!pk) {
      pk = this.getDefaultSeason();
    }
    e = $('.menu.seasons .item[data-value="' + pk + '"]');
    if (e) {
      return e.text().trim();
    }
  };
});
