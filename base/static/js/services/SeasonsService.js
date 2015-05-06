angular.module('Sportomatics').service('SeasonsService', function() {
  this.isSeasonActive = function(season, pk, isFirst) {
    if (season) {
      return +season === +pk;
    } else {
      return isFirst;
    }
  };
  this.getSeason = function(season) {
    var e, es;
    if (season) {
      e = $('.menu.seasons .item[data-value="' + season + '"]');
    } else {
      es = $('.menu.seasons .item');
      if (es) {
        e = $(es[0]);
      }
    }
    if (e) {
      return e.text().trim();
    }
  };
});
