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
})

.directive('ngUpdateHidden', function() {
    return {
        'restrict': 'AE',
        'scope': {},
        'replace': true,
        'require': 'ngModel',
        'link': function($scope, elem, attr, ngModel) {
            $scope.$watch(ngModel, function(nv) {
                elem.val(nv);
            });
            elem.change(function() {
                $scope.$apply(function() {
                    ngModel.$setViewValue(elem.val());
                });
            });
        }
    };
});

/* better fps test
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
 better fps test */
var ALL_FIELDS = ["count", "goals", "assists", "points", "plus_minus", "penalty_time", "es_goals", "pp_goals", "ev_goals", "overtime_goals", "win_goals", "bullet_goals", "shots", "pis__avg", "shots__avg", "faceoff", "winfaceoff", "winfaceoff_p_avg", "gamingtime__avg", "change_count__avg", "shots_received", "loose_goals", "saves", "saves_p__avg", "sf__avg", "matches_win", "matches_lose", "zero_goals_matches", "bullet_matches", "position"];
var KHL_NEWEST_FIELDS = ['shots', 'pis__avg', 'shots__avg', 'faceoff', 'winfaceoff', 'winfaceoff_p__avg', 'gamingtime__avg', 'change_count__avg'];
var AVERAGE_AVAILABLE_FIELDS = ['goals', 'assists', 'points', 'plus_minus', 'penalty_time'];

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
Array.prototype.getIndexBy = function (name, value) {
    for (var i = 0; i < this.length; i++) {
        if (this[i][name] == value) {
            return i;
        }
    }
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
Date.prototype.yyyymmddHHMMFormatted = function(){
    var monthNames = [
        'января', 'февраля', 'марта', 'апреля', 'мая', 'июня', 'июля',
        'августа', 'сентября', 'октября', 'ноября', 'декабря'];
    var yyyy = this.getFullYear().toString();
    var mm = (this.getMonth()); // getMonth() is zero-based
    var dd  = this.getDate().toString();
    return dd + ' ' + monthNames[mm] + ' ' + yyyy + ' в ' + this.getHours() + ':' + this.getMinutes();
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
function getParameterByName(string, name) {
        name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
        var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(string);
        return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}
function toSeason(value){
    //TODO заменить
    //14/15
    if(value.indexOf('/') > -1 && value.length === 5){
        value = parseInt(value.substring(2, 5));
        if(value > 20){
            value = '19' + value;
        } else {
            value = '20' + value;
        }

    }
    var seasons = {
        s2002: 1,
        s2003: 2,
        s2001: 3,
        s2004: 4,
        s2000: 5,
        s1999: 6,
        s1998: 7,
        s2005: 8,
        s2006: 9,
        s1997: 10,
        s2007: 11,
        s2008: 12,
        s2009: 13,
        s2010: 14,
        s2011: 15,
        s2012: 16,
        s2013: 17,
        s2014: 18,
        s2015: 19
    }
    return seasons['s'+value];
}
$.fn.textWidth = function(){
    var html_org = $(this).html();
    var html_calc = '<span>' + html_org + '</span>';
    $(this).html(html_calc);
    var width = $(this).find('span:first').width();
    $(this).html(html_org);
    return width;
};

angular.module('Sportomatics')

angular.module('Sportomatics').factory('HighchartsFactory', function($timeout, LocaleFactory, $location, $rootScope) {
  var HighchartsArenaVisitorsChart, HighchartsClubGamesChart, HighchartsPlayerClubsChart, HighchartsPlayerClubsPieChart, HighchartsPlayerIndicatorsChart, HighchartsSpiderChart;
  HighchartsSpiderChart = (function() {
    function HighchartsSpiderChart(divId, data1, categories, season) {
      this.divId = divId;
      this.data = data1;
      this.categories = categories;
      this.season = season;
      self.divId = this.divId;
      self.season = this.season;
    }

    HighchartsSpiderChart.prototype.setLocaleObject = function(localeObject) {
      this.localeObject = localeObject;
      return self.localeObject = this.localeObject;
    };

    HighchartsSpiderChart.prototype.setContext = function(context) {
      this.context = context;
      return self.context = this.context;
    };

    HighchartsSpiderChart.prototype.setFormattedData = function(data) {
      return this.data = data;
    };

    HighchartsSpiderChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          polar: true,
          type: 'line'
        },
        title: {
          text: ''
        },
        xAxis: {
          categories: this.categories,
          tickmarkPlacement: 'on',
          lineWidth: 0,
          labels: {
            formatter: function() {
              if (self.localeObject == null) {
                return this.value;
              }
              if (!$.isNumeric(this.value)) {
                return LocaleFactory.selectedLocale.fieldNames[this.value].fullName;
              }
            }
          }
        },
        tooltip: {
          shared: true,
          formatter: function() {
            var field, s;
            s = '<span style="color:black">' + LocaleFactory.selectedLocale.fieldNames[this.x].fullName + ', Сезон ' + (parseInt(self.season) - 1) + '/' + parseInt(self.season) + '</span><br/>';
            field = this.x;
            _.each(this.points, function(point, index) {
              var value;
              value = field === 'shots' ? point.point.y * 10 : point.point.y;
              return s += '<span style="color:' + point.series.color + '">' + point.series.name + ': <b>' + parseFloat(value).toFixed(3) + '</b><br/>';
            });
            return s;
          }
        },
        plotOptions: {
          series: {
            cursor: 'pointer',
            point: {
              events: {
                click: function() {
                  $('#return-control').click();
                  $timeout((function(_this) {
                    return function() {
                      var seasonIndex;
                      self.context.setField(_this.category, true);
                      seasonIndex = 0;
                      _.map(self.context.dataBySeason.results, function(element, index) {
                        if (element.season.end_date.indexOf(self.context.lastSeason) > -1) {
                          seasonIndex = index;
                        }
                        return element;
                      });
                      self.context.moveToSeason(null, seasonIndex, null, true);
                      return '';
                    };
                  })(this), 200);
                  return '';
                }
              }
            }
          }
        },
        series: this.data
      });
    };

    return HighchartsSpiderChart;

  })();
  HighchartsClubGamesChart = (function() {
    function HighchartsClubGamesChart(divId, data1) {
      this.divId = divId;
      this.data = data1;
    }

    HighchartsClubGamesChart.prototype.setLocaleObject = function(localeObject) {
      this.localeObject = localeObject;
    };

    HighchartsClubGamesChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          type: 'column',
          alignTicks: false
        },
        title: {
          text: 'Счет в матчах'
        },
        xAxis: [
          {
            labels: {
              enabled: false,
              align: 'center',
              autoRotation: false
            },
            reversed: false,
            lineColor: '#FFFFFF',
            max: 100
          }, {
            opposite: true,
            reversed: false,
            linkedTo: 0,
            labels: {
              enabled: false
            },
            lineColor: '#FFFFFF',
            gridZIndex: 4,
            min: -0.5
          }
        ],
        yAxis: {
          gridLineWidth: 0,
          plotLines: [
            {
              color: '#141414',
              width: 1,
              value: 0
            }
          ],
          title: 'Счет',
          allowDecimals: false,
          labels: {
            formatter: function() {
              return Math.abs(this.value);
            }
          },
          stackLabels: {
            formatter: function() {
              return this;
            }
          }
        },
        legend: {
          enabled: false,
          margin: 30
        },
        tooltip: {
          shared: true,
          useHTML: true,
          crosshairs: true,
          style: {
            padding: 0
          },
          formatter: function() {
            return '<div class="text-center"> <div class="tooltip-header"><b>' + this.points[0].key + '<b></div><a class="score">' + this.points[0].point.score + '</a><br><a class="match-date">' + (new Date(this.points[0].point.date).yyyymmddHHMMFormatted()) + '</a>';
          }
        },
        plotOptions: {
          series: {
            stacking: 'normal',
            borderWidth: 0,
            pointWidth: 5,
            pointPlacement: "on"
          },
          column: {
            pointPadding: 0,
            groupPadding: 0,
            borderWidth: 1,
            pointWidth: 4
          }
        },
        series: this.data
      });
    };

    return HighchartsClubGamesChart;

  })();
  HighchartsPlayerClubsChart = (function() {
    function HighchartsPlayerClubsChart(divId, data1, field1) {
      this.divId = divId;
      this.data = data1;
      this.field = field1;
    }

    HighchartsPlayerClubsChart.prototype.setLocaleObject = function(localeObject) {
      this.localeObject = localeObject;
    };

    HighchartsPlayerClubsChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          type: 'column',
          options3d: {
            enabled: true,
            alpha: 15,
            beta: 15,
            viewDistance: 25,
            depth: 40
          }
        },
        title: {
          text: LocaleFactory.selectedLocale.fieldNames[this.field].fullName.toUpperCase()
        },
        xAxis: {
          "type": "datetime",
          labels: {
            align: 'center',
            autoRotation: false,
            formatter: function() {
              return (new Date(this.value).getFullYear() - 1).toString().substr(2, 2) + '/' + (new Date(this.value).getFullYear()).toString().substr(2, 2);
            }
          },
          tickInterval: 24 * 3600 * 1000 * 365,
          gridLineColor: '#FFFFFF'
        },
        yAxis: {
          allowDecimals: false,
          min: 0,
          title: {
            text: ''
          },
          gridLineColor: '#FFFFFF',
          labels: {
            enabled: false
          }
        },
        legend: {
          margin: 30
        },
        tooltip: {
          headerFormat: '<b>{point.key}</b><br>',
          pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: {point.y} / {point.stackTotal}',
          formatter: function() {
            var s, sum;
            s = '<b>Сезон ' + (new Date(this.x).getFullYear() - 1) + '/' + new Date(this.x).getFullYear() + '</b>';
            sum = 0;
            $.each(this.points, function() {
              sum += this.y;
              return s += '<br/>' + this.series.name + ': ' + this.y;
            });
            return s += '<br/><b>Всего: ' + sum;
          },
          shared: true
        },
        plotOptions: {
          column: {
            stacking: 'normal',

            /*depth: 20
            pointWidth: 20
            pointPadding: 2
            groupPadding: 20
             */
            pointRange: 24 * 3600 * 1000 * 365
          }
        },
        series: this.data
      });
    };

    return HighchartsPlayerClubsChart;

  })();
  HighchartsArenaVisitorsChart = (function() {
    function HighchartsArenaVisitorsChart(divId, data1, max) {
      this.divId = divId;
      this.data = data1;
      this.max = max;
    }

    HighchartsArenaVisitorsChart.prototype.setLocaleObject = function(localeObject) {
      this.localeObject = localeObject;
    };

    HighchartsArenaVisitorsChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          type: 'column',
          alignTicks: false
        },
        title: {
          text: 'Посещаемость'
        },
        xAxis: {
          labels: {
            enabled: false,
            align: 'center',
            autoRotation: false
          },
          reversed: false,
          lineColor: '#FFFFFF',
          max: 100
        },
        yAxis: {
          gridLineWidth: 0,
          plotLines: [
            {
              color: '#141414',
              width: 1,
              value: 0
            }, {
              value: this.max,
              width: 1,
              color: '#141414',
              label: {
                text: 'Вместимость'
              }
            }
          ],
          title: 'Счет',
          allowDecimals: false,
          labels: {
            formatter: function() {
              return Math.abs(this.value);
            }
          },
          stackLabels: {
            formatter: function() {
              return this;
            }
          }
        },
        legend: {
          enabled: false,
          margin: 30
        },
        tooltip: {
          shared: true,
          useHTML: true,
          crosshairs: true,
          style: {
            padding: 0
          },
          formatter: function() {
            return '<div class="text-center"> <div class="tooltip-header"><b>' + this.points[0].key + '<b></div><a class="score">' + this.points[0].point.spectators + '</a><br><a class="match-date">' + (new Date(this.points[0].point.date).yyyymmddHHMMFormatted()) + '</a>';
          }
        },
        plotOptions: {
          series: {
            stacking: 'normal',
            borderWidth: 0,
            pointWidth: 5,
            pointPlacement: "on"
          },
          column: {
            pointPadding: 0,
            groupPadding: 0,
            borderWidth: 1,
            pointWidth: 4
          }
        },
        series: this.data
      });
    };

    return HighchartsArenaVisitorsChart;

  })();
  HighchartsPlayerClubsPieChart = (function() {
    function HighchartsPlayerClubsPieChart(divId, data1) {
      this.divId = divId;
      this.data = data1;
    }

    HighchartsPlayerClubsPieChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          plotBackgroundColor: null,
          plotBorderWidth: null,
          plotShadow: false
        },
        title: {
          text: ''
        },
        tooltip: {
          enabled: false
        },
        plotOptions: {
          pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            dataLabels: {
              enabled: true,
              format: '<b>{point.name}</b>: {point.percentage:.1f} %',
              style: {
                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
              }
            }
          }
        },
        series: [
          {
            type: 'pie',
            name: 'Клубная карьера',
            data: this.data,
            point: {
              events: {
                click: function(event) {
                  if (this.selected) {
                    return window.location.href = this.url;
                  }
                }
              }
            }
          }
        ]
      });
    };

    return HighchartsPlayerClubsPieChart;

  })();
  HighchartsPlayerIndicatorsChart = (function() {
    function HighchartsPlayerIndicatorsChart() {
      this.period = self.period = 365;
      this.field = $location.search()['field'] ? $location.search()['field'] : 'count';
      this.dataType = 'graph-serial';
      self.field = this.field;
    }

    HighchartsPlayerIndicatorsChart.prototype.init = function(divId, data1) {
      this.divId = divId;
      this.data = data1;
    };

    HighchartsPlayerIndicatorsChart.prototype.setPeriod = function(period) {
      this.period = period;
      return self.period = this.period;
    };

    HighchartsPlayerIndicatorsChart.prototype.setContext = function(context) {
      this.context = context;
      return self.context = this.context;
    };

    HighchartsPlayerIndicatorsChart.prototype.setField = function(field1, preventList) {
      this.field = field1;
      self.field = this.field;
      $('#chart-tooltip-content').html('');
      return $rootScope.$broadcast('field-changed', preventList);
    };

    HighchartsPlayerIndicatorsChart.prototype.getField = function() {
      return this.field;
    };

    HighchartsPlayerIndicatorsChart.prototype.setDataType = function(dataType) {
      this.dataType = dataType;
    };

    HighchartsPlayerIndicatorsChart.prototype.getDataType = function() {
      return this.dataType;
    };

    HighchartsPlayerIndicatorsChart.prototype.draw = function() {
      return $('#' + this.divId).highcharts({
        chart: {
          type: 'column',
          options3d: {
            enabled: true,
            alpha: 0,
            beta: 15,
            viewDistance: 25,
            depth: 100
          },
          marginLeft: 0,
          events: {
            drilldown: function(e) {
              var chart;
              if (!e.seriesOptions) {
                chart = this;
                chart.showLoading('Загрузка данных по месяцам ...');
                if (self.context.dataByMonth == null) {
                  return self.context.getPlayerDataByMonth().then(function(dataByMonth) {
                    chart.hideLoading();
                    chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
                    return self.context.moveToSeason(e.point.index, e.point.index, e.point.drilldown);
                  });
                } else {
                  chart.hideLoading();
                  chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
                  return self.context.moveToSeason(e.point.index, e.point.index, e.point.drilldown);
                }
              }
            }
          }
        },
        title: {
          text: ''
        },
        xAxis: {
          "type": "datetime",
          labels: {
            align: 'center',
            formatter: function() {
              if (this.dateTimeLabelFormat === '%Y') {
                return (new Date(this.value).getFullYear() - 1).toString().substr(2, 2) + '/' + (new Date(this.value).getFullYear()).toString().substr(2, 2);
              } else {
                return LocaleFactory.selectedLocale.monthNames[new Date(this.value).getMonth()] + ' ' + (new Date(this.value).getFullYear()).toString().substr(2, 2);
              }
            }
          },
          tickInterval: 24 * 3600 * 1000 * 30
        },
        yAxis: {
          allowDecimals: false,
          title: {
            text: ''
          },
          maxPadding: 0.02
        },
        legend: {
          margin: 30
        },
        tooltip: {
          followPointer: true,
          crosshairs: true,
          formatter: function() {
            var header, s;
            header = '<b>' + LocaleFactory.selectedLocale.fieldNames[self.field].fullName.toUpperCase() + '</b>';
            if (this.points[0].point.drilldown != null) {
              s = '<div class="inline-block tooltip-block"><b>Сезон <br>' + (new Date(this.x).getFullYear() - 1) + '/' + new Date(this.x).getFullYear() + '</b></div>';
              $.each(this.points, function() {
                return s += '<div class="inline-block tooltip-block"><b>' + this.series.name + '</b>:<br>' + '<span class="tooltip-value">' + this.y + '</span></div>';
              });
              $('#chart-tooltip-content').html(s);
              return false;
            } else {
              s = '<div class="inline-block tooltip-block"><b>' + LocaleFactory.selectedLocale.monthNamesFull[new Date(this.x).getMonth()] + ' <br>' + new Date(this.x).getFullYear() + '</b></div>';
              $.each(this.points, function() {
                return s += '<div class="inline-block tooltip-block"><b>' + this.series.name + '</b>:<br>' + '<span class="tooltip-value">' + this.y + '</span></div>';
              });
              $('#chart-tooltip-content').html(s);
              return false;
            }
          },
          shared: true
        },
        plotOptions: {
          column: {
            stacking: 'normal',
            pointRange: 24 * 3600 * 1000 * self.period,
            states: {
              hover: {
                brightness: -0.2
              }
            }
          }
        },
        series: this.data,
        drilldown: {
          series: this.drilldownSeries
        }
      });
    };

    HighchartsPlayerIndicatorsChart.prototype.getChart = function() {
      return this.chart;
    };

    return HighchartsPlayerIndicatorsChart;

  })();
  return {
    PlayerStatsSpiderChart: HighchartsSpiderChart,
    ClubGamesChart: HighchartsClubGamesChart,
    ArenaVisitorsChart: HighchartsArenaVisitorsChart,
    PlayerClubsChart: HighchartsPlayerClubsChart,
    PlayerClubsPieChart: HighchartsPlayerClubsPieChart,
    PlayerIndicatorsChart: HighchartsPlayerIndicatorsChart
  };
});

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

angular.module('Sportomatics')
    .factory('LocaleFactory', function($rootScope){
        var chosen = 'ru';
        var self = this;
        var factory = {
            setLocale: function(contentLanguage){
                factory.selectedLocale = factory['locale_'+contentLanguage]
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
                monthNamesFull: ["Январь", "Феввраль", "Март", "Апрель", "Май", "Июнь",
                    "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                words: {
                    season: 'Сезон',
                    months: 'Месяц',
                    offender: 'Нападающий',
                    goalkeeper: 'Вратарь',
                    defender: 'Защитник'
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
                    months: 'Month',
                    offender: 'Offender',
                    goalkeeper: 'Goalkeeper',
                    defender: 'Defender'
                }
            }
        }
        factory.selectedLocale = factory.locale_ru;

        return factory;

    })

var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').service('MapService', function($q, $timeout) {
  var self, startCoordinate1, startCoordinate2;
  self = this;
  startCoordinate1 = 55.749792;
  startCoordinate2 = 37.632495;
  this.mapsDivName = 'clubs-map';
  this.clubs_map = document.getElementById(self.mapsDivName);
  this.rendered = false;
  this.map = null;
  this.geocoder = new google.maps.Geocoder;
  this.addedMarkers = [];
  this.createClubsMap = function(data, dataLabel) {
    var ggl, osm;
    self.map = L.map(self.mapsDivName, {
      scrollWheelZoom: false
    }).setView([startCoordinate1, startCoordinate2], 4);
    osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    ggl = new L.Google('ROADMAP');
    self.map.addLayer(ggl);
    self.map.addControl(new L.Control.Layers({
      'Google': ggl,
      'OpenStreetMap': osm
    }, {}));
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false,
      zoomToBoundsOnClick: false,
      animateAddingMarkers: true,
      maxClusterRadius: 120
    });
    switch (dataLabel) {
      case 'clubs':
        self.markersFunctionClubs(data);
        break;
      case 'players':
        self.markersFunctionPlayers(data);
        break;
      case 'trips':
        self.markersFunctionClubGames(data);
        break;
      case 'fans':
        self.markersFunctionFans(data);
    }
    self.map.addLayer(self.markers);
    this.rendered = true;
  };
  this.cityClickFunction = function(event) {
    self.context.selectedPlace = event.target.options.title.split('_')[0].toUpperCase();
    $timeout(function() {}, 100);
  };
  this.clusterClickClubs = function(a) {
    var cluster;
    self.a = a;
    cluster = a.layer.getAllChildMarkers();
    if (self.map.getZoom() === self.map.getMaxZoom()) {
      return;
    }
    self.popup = L.popup().setLatLng(a.layer._latlng).setContent('<div class="text-center">' + cluster[0].options.title + ' и еще ' + (cluster.length - 1) + ' клубов <br> <a class="link pointer" id="show-all">показать все</a></div>').openOn(self.map);
    document.getElementById('show-all').onclick = function() {
      return self.moveToClusterBounds(self.a);
    };
  };
  this.moveToClusterBounds = function(cluster) {
    cluster.layer.zoomToBounds();
    self.map.closePopup(self.popup);
    if (self.map.getZoom() === self.map.getMaxZoom()) {
      self.map.zoomOut(2);
    }
  };
  this.markersFunctionClubs = function(clubs) {
    var countOfGeocoded;
    countOfGeocoded = 0;
    _.each(clubs, function(club, index) {
      var clubIcon, coordinate1, coordinate2, coords;
      clubIcon = L.icon({
        iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
        iconSize: [20, 20],
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
        shadowSize: [34, 48]
      });
      if (!club.arena) {
        return;
      }
      coords = club.arena.coords;
      if (coords !== null) {
        coordinate1 = coords.split(',')[0];
        coordinate2 = coords.split(',')[1];
      }
      if (!club.arena.coords) {
        self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result) {
          self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
            icon: clubIcon,
            title: club.title
          }).bindPopup(club.title + '<br>'));
        });
        countOfGeocoded++;
      }
      if (coordinate1 && coordinate2) {
        self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {
          icon: clubIcon,
          title: club.title
        }).bindPopup(club.title + '<br>'));
      }
    });
    self.markers.on('clusterclick', this.clusterClickClubs);
  };
  this.markersFunctionClubGames = function(games) {
    var clubs, countOfGeocoded;
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false
    });
    countOfGeocoded = 0;
    clubs = [];
    _.each(games, function(game, index) {
      var club, clubDates, clubDatesString, clubIcon, coordinate1, coordinate2, coords, popup;
      if (game.is_guest) {
        club = game.home_team;
        if (!club.arena || _.findWhere(clubs, {
          'title': club.title
        })) {
          return;
        }
        clubs.push(club);
        clubIcon = L.icon({
          iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
          iconSize: [20, 20],
          shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
          shadowSize: [34, 48]
        });
        coords = club.arena.coords;
        if (coords !== null) {
          coordinate1 = coords.split(',')[0];
          coordinate2 = coords.split(',')[1];
        }
        clubDates = [];
        _.each(games, function(game) {
          if (game.home_team.title === club.title) {
            clubDates.push(new Date(game.date).yyyymmddFormatted());
          }
        });
        clubDatesString = clubDates.join(' <br> ');
        popup = L.popup({
          className: 'map-popup'
        }).setContent('<div class="bold">' + club.title + '</div><br> Матчи:<br>' + clubDatesString);
        if (!club.arena.coords) {
          self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result) {
            self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
              icon: clubIcon
            }).bindPopup(popup));
          });
          countOfGeocoded++;
        }
        if (coordinate1 && coordinate2) {
          self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {
            icon: clubIcon
          }).bindPopup(popup));
        }
      }
    });
  };
  this.markersFunctionPlayers = function(players) {
    var countOfGeocoded;
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false
    });
    countOfGeocoded = 0;
    _.each(players, function(player, index) {
      var playerIcon;
      if (!player.birth_place) {
        return;
      }
      playerIcon = L.icon({
        iconUrl: player.photo ? player.photo : '/static/abc.jpg',
        iconSize: [20, 20],
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
        shadowSize: [34, 48]
      });
      self.googleGeocode(player.birth_place, countOfGeocoded).then(function(result) {
        self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
          icon: playerIcon
        }).bindPopup(player.fio + '<br> Место рождения: ' + player.birth_place));
      });
      countOfGeocoded++;
    });
  };
  this.markersFunctionFans = function(fans) {
    var countOfGeocoded, locations;
    countOfGeocoded = 0;
    locations = [];
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false,
      iconCreateFunction: function(cluster) {
        var c, markers, sum;
        sum = 0;
        c = ' marker-cluster-';
        markers = cluster.getAllChildMarkers();
        _.each(markers, function(marker) {
          if (marker.options.title.length !== 0) {
            sum += Number(marker.options.title.split('_')[1]);
          }
          c = ' marker-cluster-';
          if ((-1 < sum && sum < 10)) {
            c += 'small';
          } else {
            c += 'large';
          }
        });
        return new L.DivIcon({
          html: '<div><span>' + sum + '</span></div>',
          className: 'marker-cluster' + c,
          iconSize: new L.Point(40, 40)
        });
      }
    });
    _.each(fans, function(fan, index) {
      var ref;
      if ((ref = fan.location, indexOf.call(locations.map(function(l) {
        return l.name;
      }), ref) < 0)) {
        locations.push({
          name: fan.location,
          count: 1
        });
      } else {
        locations.map(function(location) {
          if (location.name === fan.location) {
            location.count = location.count + 1;
          }
          return location;
        });
      }
    });
    _.each(locations, function(location, index) {
      self.googleGeocode(location.name, countOfGeocoded).then(function(result) {
        var c, playerIcon, ref;
        c = ' marker-cluster-';
        if ((0 < (ref = location.count) && ref < 10)) {
          c += 'small';
        } else {
          c += 'large';
        }
        playerIcon = new L.DivIcon({
          html: '<div><span>' + location.count + '</span></div>',
          className: 'marker-cluster' + c,
          iconSize: new L.Point(40, 40)
        });
        self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
          icon: playerIcon,
          title: location.name + '_' + location.count
        }).on('click', self.cityClickFunction));
      });
      return countOfGeocoded++;
    });
  };
  this.isRendered = function() {
    return this.rendered;
  };
  this.setRendered = function(value) {
    if (value !== true && value !== false) {
      return;
    }
    this.rendered = value;
  };
  this.setContext = function(context) {
    this.context = context;
  };
  this.remove = function() {
    $('#' + self.mapsDivName).remove();
    $('#' + self.mapsDivName + '-container').append('<div id="' + self.mapsDivName + '"></div>');
  };
  this.googleGeocode = function(address, delay) {
    var deferred;
    deferred = $q.defer();
    address = address.substr(address.indexOf(' ') + 1).replace('ул.', '').replace('д.', '').replace('Московская обл.,', '');
    if (address.indexOf('Телефон') > -1) {
      address = address.substring(0, address.indexOf('Телефон'));
    }
    $timeout((function() {
      self.geocoder.geocode({
        'address': address
      }, function(results, status) {
        var coordinate1, coordinate2;
        if (status === google.maps.GeocoderStatus.OK) {
          coordinate1 = results[0].geometry.location.B;
          coordinate2 = results[0].geometry.location.k;
          deferred.resolve([coordinate2, coordinate1]);
        } else {
          deferred.reject();
          console.log(address, 'Geocode was not successful for the following reason: ' + status);
        }
      });
    }), 400 * delay);
    return deferred.promise;
  };
});

var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').service('PlayersSearchService', function($http, $timeout) {
  this.loadCountries = function($scope, $location, callback) {
    var url;
    url = $('#LeagueListLink').attr('href');
    if (url) {
      $http.get(url).success(function(data) {
        $scope.countries = data;
        $timeout(function() {
          return $('.ui.dropdown.leagues').dropdown();
        }, 0);
        if (callback && typeof callback === 'function') {
          return callback($scope);
        }
      });
    } else if (callback && typeof callback === 'function') {
      callback($scope);
    }
  };
  this.setCountries = function($scope, countries) {
    $scope.countriesSelected = countries;
    $scope.leaguesSelected = [];
    $scope.$location.search('country', countries || null);
    $scope.$location.search('league', null);
  };
  this.getLeagues = function(countries, selected) {
    var country, league_sets, x;
    if (countries && selected) {
      if (!Array.isArray(selected)) {
        selected = [selected];
      }
      selected = (function() {
        var i, len, results;
        results = [];
        for (i = 0, len = selected.length; i < len; i++) {
          x = selected[i];
          results.push(+x);
        }
        return results;
      })();
      league_sets = (function() {
        var i, len, ref, results;
        results = [];
        for (i = 0, len = countries.length; i < len; i++) {
          country = countries[i];
          if (ref = country.pk, indexOf.call(selected, ref) >= 0) {
            results.push(country.league_set);
          }
        }
        return results;
      })();
      return [].concat.apply([], league_sets);
    }
    return [];
  };
  this.isMatchesTotalVisible = function($scope) {
    var ref;
    return (ref = $scope.params.rated_by) === 'goals_average' || ref === 'assists_average' || ref === 'points_average' || ref === 'plus_minus_average';
  };
  this.setOrderBy = function($scope, order_by) {
    if (!$scope.loader) {
      if ($scope.params.order_by === order_by || (!$scope.params.order_by && !order_by)) {
        if ($scope.params.reversed === 'true') {
          $scope.$location.search('reversed', null);
        } else {
          $scope.$location.search('reversed', 'true');
        }
      } else {
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
  };
  this.setRatedBy = function($scope, rated_by) {
    if (!$scope.loader && $scope.params.rated_by !== rated_by) {
      $scope.$location.search('alphabet', null);
      $scope.$location.search('rated_by', rated_by || null);
      if (rated_by) {
        $scope.$location.search('order_by', 'rating');
        $scope.$location.search('reversed', 'true');
        this.search($scope);
      } else {
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
      value = [obj.originalObject];
    } else {
      value = null;
    }
    if (!$scope.loader && $scope.club !== value) {
      $scope.club = value;
      this.search($scope);
    }
  };
  this.search = function($scope) {
    var age, checkBox, contract_types, d, e, k, league, lineAll, lineChecked, lineUnchecked, multiSelect, params, relatedValue, url, x;
    checkBox = function($scope, search, name) {
      $scope.$location.search(search, $('[name="' + name + '"]').is(':checked') || null);
    };
    multiSelect = function($scope, search, value) {
      if (value && value.length) {
        $scope.$location.search(search, JSON.stringify(value));
      } else {
        $scope.$location.search(search, null);
      }
    };
    url = $('#PlayersSearchLink').attr('href');
    params = '';
    if ($('#isCitizenshipRussia').is(':checked')) {
      $scope.$location.search('citizenship1', $('#citizenshipRussia').val());
    } else {
      $scope.$location.search('citizenship1', null);
    }
    if ($('#isCitizenshipOther').is(':checked')) {
      $scope.$location.search('citizenship_other', 'true');
    } else {
      $scope.$location.search('citizenship_other', null);
    }
    lineAll = (function() {
      var i, len, ref, results;
      ref = $('[name="line"]');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    lineChecked = (function() {
      var i, len, ref, results;
      ref = $('[name="line"]:checked');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    lineUnchecked = (function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineAll.length; i < len; i++) {
        e = lineAll[i];
        if (indexOf.call(lineChecked, e) < 0) {
          results.push(e);
        }
      }
      return results;
    })();
    $scope.$location.search('line', ((function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineChecked.length; i < len; i++) {
        e = lineChecked[i];
        if (+e > 0) {
          results.push(e);
        }
      }
      return results;
    })()) || []);
    $scope.$location.search('line', ((function() {
      var i, len, results;
      results = [];
      for (i = 0, len = lineUnchecked.length; i < len; i++) {
        e = lineUnchecked[i];
        if (+e < 0) {
          results.push(e);
        }
      }
      return results;
    })()) || []);
    contract_types = (function() {
      var i, len, ref, results;
      ref = $('[name="contract_types"]:checked');
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        e = ref[i];
        if ($(e).val()) {
          results.push($(e).val());
        }
      }
      return results;
    })();
    $scope.$location.search('contract_types', contract_types || []);
    checkBox($scope, 'contract_type__isnull', 'contractTypeNull');
    checkBox($scope, 'citizenship_reversed', 'citizenshipReversed');
    checkBox($scope, 'season_enabled', 'seasonEnabled');
    checkBox($scope, 'club_enabled', 'clubEnabled');
    checkBox($scope, 'league_enabled', 'league2Enabled');
    checkBox($scope, 'related_enabled', 'relatedEnabled');
    multiSelect($scope, 'citizenship', $scope.citizenship);
    multiSelect($scope, 'club', $scope.club);
    multiSelect($scope, 'league2', $scope.league2);
    multiSelect($scope, 'related_player', $scope.relatedPlayer);
    if ($scope.number) {
      $scope.$location.search('number', $scope.number);
    }
    if ($('[name="age"]').length) {
      age = $('[name="age"]').val().split(';');
      $scope.$location.search('age__lte', age[0]);
      $scope.$location.search('age__gte', age[1]);
    }
    if ($('[name="relatedValue"]').length) {
      relatedValue = $('[name="relatedValue"]').val().split(';');
      $scope.$location.search('related_value__gte', relatedValue[0]);
      $scope.$location.search('related_value__lte', relatedValue[1]);
    }
    $scope.params = $scope.$location.search();
    params += ((function() {
      var i, len, ref, results;
      ref = ['player', 'season', 'number', 'contract_type', 'height', 'weight', 'grip', 'match_count', 'rated_by', 'age__lte', 'age__gte', 'gamingtime', 'related_value__lte', 'related_value__gte'];
      results = [];
      for (i = 0, len = ref.length; i < len; i++) {
        k = ref[i];
        if ($scope.params[k]) {
          results.push(k + '=' + $scope.params[k]);
        }
      }
      return results;
    })()).join('&');
    params += '&order_by=' + ($scope.params.order_by || '%s_lastname,%s_name');
    if ($scope.params.reversed) {
      params += '&reversed=true';
    }
    if ($scope.params.contract_types) {
      params += ((function() {
        var i, len, ref, results;
        ref = $scope.params.contract_types;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&contract_types=' + x);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.citizenship1) {
      params += '&citizenship=' + $scope.params.citizenship1;
    }
    if ($scope.params.citizenship_other === 'true') {
      if ($scope.params.citizenship2) {
        params += '&citizenship=' + $scope.params.citizenship2;
      } else {
        params += '&citizenship_other=true';
      }
    }
    if ($scope.params.is_playing !== 'false') {
      params += '&is_playing=true';
    }
    if ($scope.params.alphabet) {
      params += '&%s_lastname__startswith=' + $scope.params.alphabet;
    }
    if (($scope.club_enabled || $scope.params.club_enabled) && $scope.params.club) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.club);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&club=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.league) {
      params += ((function() {
        var i, len, ref, results;
        ref = $scope.params.league;
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          league = ref[i];
          results.push('&league=' + league);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.contract_to) {
      d = $scope.params.contract_to.split('/');
      params += '&contract_to=' + d[2] + '-' + d[0] + '-' + d[1];
    }
    if ($scope.params.contract_type__isnull) {
      params += '&contract_type__isnull=true';
    }
    if ($scope.params.citizenship_reversed) {
      params += '&citizenship_reversed=true';
    }
    if ($scope.params.citizenship) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.citizenship);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&citizenship=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.league_enabled && $scope.params.league2) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.league2);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&league=' + x['pk']);
        }
        return results;
      })()).join('');
    }
    if ($scope.params.season_enabled) {
      if ($scope.params.season_start && $scope.params.season_end) {
        params += '&season_start=' + $scope.params.season_start + '&season_end=' + $scope.params.season_end;
      }
    }
    if ($scope.params.related_enabled && $scope.params.related_player && $scope.params.related_field) {
      params += ((function() {
        var i, len, ref, results;
        ref = JSON.parse($scope.params.related_player);
        results = [];
        for (i = 0, len = ref.length; i < len; i++) {
          x = ref[i];
          results.push('&related_player=' + x['pk']);
        }
        return results;
      })()).join('');
      params += '&related_field=' + $scope.params.related_field;
    }
    $scope.data = {};
    $scope.loader = true;
    $http.get(url + '?' + params).success(function(data) {
      $scope.data = data;
      return $scope.loader = false;
    });
  };
  this.next = function($scope, isAll) {
    var url;
    url = $scope.data.next;
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
      return $scope.loader = false;
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

angular.module('Sportomatics').service('tags', function($http, $q, $filter) {
  this.loadCountries = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
  this.loadClubs = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
  this.loadPlayers = function(url, query) {
    return $http.get(url + '?s=' + query);
  };
});

angular.module('Sportomatics').controller('ClubCalendarController', [
  '$scope', '$http', '$location', '$parse', 'MapService', 'HighchartsFactory', function($scope, $http, $location, $parse, MapService, HighchartsFactory) {
    $scope.MONTHS = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    $scope.data = {};
    $scope.params = $location.search();
    $scope.clubName = document.getElementById('team-name-hidden').value;
    $scope.clubAddress = document.getElementById('club-address') != null ? document.getElementById('club-address').innerHTML : '';
    $scope.clubMatchApi = document.getElementById('club-match-api') != null ? document.getElementById('club-match-api').value : void 0;
    $scope.clubCalendarApi = $scope.url = document.getElementById('club-calendar-api') != null ? document.getElementById('club-calendar-api').value : void 0;
    $scope.clubPk = document.getElementById('team-id').value;
    $scope.games = [];
    $scope.selection = 'all';
    $scope.setSelecton = function(selection) {
      $scope.selection = selection;
      return $scope.createGamesChart();
    };
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
      } else {
        params += '&season=19';
      }
      $scope.data = {};
      $scope.loaded = false;
      $http.get($scope.url + '?' + params).success(function(data) {
        var date, deltaM;
        console.log(data);
        if (MapService.isRendered()) {
          MapService.remove();
        }
        if ($('#clubs-map').length > 0) {
          MapService.createClubsMap(data.results, 'trips');
        }
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
      return $scope.createGamesChart();
    };
    $scope.createGamesChart = function() {
      var params;
      params = '';
      params += '?club=' + $scope.clubPk;
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      return $http.get($scope.clubMatchApi + params).success(function(data) {
        var clubGamesChart, clubObject, opponentObject, seriesClub, seriesOpponent;
        $scope.games = _.sortBy(data, function(el) {
          return new Date(el).getTime();
        }).reverse();
        seriesClub = {};
        seriesOpponent = {};
        opponentObject = {
          name: 'opponents',
          data: $scope.games.map(function(game, index) {
            if ($scope.selection === 'home' && game.is_home === false) {
              return;
            }
            if ($scope.selection === 'guest' && game.is_home === true) {
              return;
            }
            return {
              x: index,
              y: -Math.abs(game.opponent_score),
              date: game.date,
              name: game.opponent.title_verbose + ' - ' + $scope.clubName + ' ' + $scope.clubAddress,
              score: Math.abs(game.opponent_score) + ' : ' + Math.abs(game.score),
              color: Math.abs(game.opponent_score) > Math.abs(game.score) ? '#e74c3c' : '#2ecc71'
            };
          }).filter(function(toFilter) {
            return toFilter != null;
          })
        };
        clubObject = {
          name: 'club',
          data: $scope.games.map(function(game, index) {
            var opponentAddress;
            if ($scope.homeOnly && game.is_home === false) {
              return;
            }
            opponentAddress = game.opponent.address && game.opponent.address.title ? game.opponent.address.title : '';
            return {
              x: index,
              y: game.score,
              date: game.date,
              name: $scope.clubName + ' ' + $scope.clubAddress + ' - ' + game.opponent.title_verbose,
              score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score),
              color: Math.abs(game.opponent_score) > Math.abs(game.score) ? '#e74c3c' : '#2ecc71'
            };
          }).filter(function(toFilter) {
            return toFilter != null;
          })
        };
        clubGamesChart = new HighchartsFactory.ClubGamesChart('chartdiv', [clubObject, opponentObject]);
        return clubGamesChart.draw();
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
    $scope.list();
  }
]);

angular.module('Sportomatics').controller('ClubFanController', function($scope, MapService) {
  $scope.loaded = true;
  console.log($scope.loaded);
  $scope.fans = [
    {
      name: 'Олег',
      lastname: 'Иванов',
      citizenship: {
        title: 'Россия'
      },
      location: 'Москва'
    }, {
      name: 'Петр',
      lastname: 'Сидоров',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Вячеслав',
      lastname: 'Рябинин',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Олег',
      lastname: 'Иванов',
      citizenship: {
        title: 'Россия'
      },
      location: 'Москва'
    }, {
      name: 'Петр',
      lastname: 'Сидоров',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Вячеслав',
      lastname: 'Рябинин',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Олег',
      lastname: 'Иванов',
      citizenship: {
        title: 'Россия'
      },
      location: 'Москва'
    }, {
      name: 'Петр',
      lastname: 'Сидоров',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Вячеслав',
      lastname: 'Рябинин',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Олег',
      lastname: 'Иванов',
      citizenship: {
        title: 'Россия'
      },
      location: 'Москва'
    }, {
      name: 'Петр',
      lastname: 'Сидоров',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }, {
      name: 'Вячеслав',
      lastname: 'Рябинин',
      citizenship: {
        title: 'Россия'
      },
      location: 'Санкт-Петербург'
    }
  ];
  $scope.compare = function(actual) {
    if ($scope.selectedPlace == null) {
      return true;
    }
    return actual.location.toUpperCase() === $scope.selectedPlace;
  };
  $scope.$watch('selectedPlace', 'change', function() {});
  MapService.setContext($scope);
  if (MapService.isRendered()) {
    MapService.remove();
  }
  MapService.createClubsMap($scope.fans, 'fans');
});

angular.module('Sportomatics').controller('ClubHomeController', function($scope, $location, $http, HighchartsFactory) {
  $scope.clubMatchApi = document.getElementById('club-match-api').value;
  $scope.clubPk = document.getElementById('team-id').value;
  $scope.params = $location.search();
  $scope.createVisitorsChart = function() {
    var params;
    params = '';
    params += '?club=' + $scope.clubPk;
    params += '&season=19';
    return $http.get($scope.clubMatchApi + params).success(function(data) {
      var clubGamesChart, seriesClub, seriesOpponent, visitorsObject;
      $scope.games = _.filter(_.sortBy(data, function(el) {
        return new Date(el).getTime();
      }).reverse(), function(game) {
        return game.is_home === true;
      });
      console.log($scope.games);
      seriesClub = {};
      seriesOpponent = {};
      visitorsObject = {
        name: 'club',
        data: $scope.games.map(function(game, index) {
          return {
            x: index,
            y: game.spectators,
            date: game.date,
            name: game.opponent.title_verbose,
            score: Math.abs(game.score) + ' : ' + Math.abs(game.opponent_score),
            spectators: game.spectators + ' (' + parseInt(parseFloat(game.arena_capacity_rate).toFixed(2) * 100) + '%)'
          };
        }).filter(function(toFilter) {
          return toFilter != null;
        })
      };
      console.log(parseFloat($scope.games[0].arena_capacity_rate).toFixed(2) * 100);
      clubGamesChart = new HighchartsFactory.ArenaVisitorsChart('chartdiv', [visitorsObject], $scope.games[0].arena_capacity);
      return clubGamesChart.draw();
    });
  };
  $scope.createVisitorsChart();
});

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
    $scope.sparams = {};

    $scope.params = $location.search();
    $scope.params.league = '';

    // if ($scope.params.season) {
    //     $('[name="season"]').attr('value', $scope.params.season);
    // }

    $scope.setSeason = function(season) {
        $location.search('season', season);
        $location.search('league', '');
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
        if (!$scope.isCountryActive(country)) {
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

    $scope.isCountryActive = function(country) {
        if ($scope.params.country) {
            return $scope.params.country == country;
        } else {
            return country == 1;
        }
    };

    $scope.isLeagueActive = function(league) {
        if ($scope.data && $scope.data.league) {
            if ($scope.data.league.pk) { // selected league
                return $scope.data.league.pk === league;
            } else { // all leagues
                return league === null;
            }
        } else {
            return false;
        }
    };

    $scope.list = function(all) {
        var params = ''; //$('#ClubListForm').serialize();

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

        if ($scope.params.season || $scope.season) {
            params += '&season=' + ($scope.params.season || $scope.season);
        }
        if ($scope.params.league !== undefined) {
            params += '&league=' + ($scope.params.league || '');
        }
        params += '&country=' + ($scope.params.country || 1);

        $scope.params = $location.search();
        $scope.data = {};
        $scope.loaded = false;
        $http.get(url + '?' + params
        ).success(function(data) {
            $scope.leagues = data.leagues;
            $scope.data = data;
            $scope.clubs = data.results;
            $scope.loaded = true;
        }).then(function(){
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap($scope.clubs, 'clubs');
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
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap($scope.clubs, 'clubs');
        });
    };

    PlayersSearchService.loadCountries($scope, $location, function(){});

    $scope.list();
}]);

angular.module('Sportomatics').controller('ClubMainAboutController', [
  '$scope', '$location', '$http', 'SeasonsService', function($scope, $location, $http, SeasonsService) {
    $scope.$location = $location;
    $scope.SeasonsService = SeasonsService;
    $scope.params = $location.search();
    $scope.bestPlayersURL = $('#bestPlayersURL').val();
    $scope.setSeason = function(season) {
      $location.search('season', season);
      $scope.params = $location.search();
      $scope.getBestPlayers();
    };
    $scope.getBestPlayers = function() {
      var params, season;
      if ($scope.params.season) {
        season = $scope.params.season;
      } else {
        season = SeasonsService.getDefaultSeason();
      }
      params = 'season=' + season;
      $scope.loaded = false;
      $http.get($scope.bestPlayersURL + '?' + params).success(function(data) {
        $scope.data = data;
        $scope.loaded = true;
      });
    };
    $scope.getBestPlayers();
  }
]);

angular.module('Sportomatics')
    .controller('ClubNewsController', function($scope, $http, LocaleFactory, $timeout){
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


    })

angular.module('Sportomatics').controller('ClubStatsController', [
  '$http', '$scope', '$location', 'PlayersSearchService', function($http, $scope, $location, PlayersSearchService) {
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;
    $scope.data = {};
    $scope.countries = [];
    $scope.loader = false;
    $scope.club = [
      {
        'pk': +$('[name="club"]').val()
      }
    ];
    $scope.club_enabled = true;
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

angular.module('Sportomatics').controller('ClubTeamCompareController', function($scope, $http, $q, IndicatorsFactory, HighchartsFactory, LocaleFactory, $timeout) {
  var averageClubPlayerIndicatorsChart, self;
  self = this;
  this.url = document.getElementById('api-player-indicators').value;
  averageClubPlayerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart();
  $scope.localeObject = LocaleFactory.selectedLocale;
  $scope.setField = averageClubPlayerIndicatorsChart.setField;
  $scope.field = averageClubPlayerIndicatorsChart.getField();
  $scope.dataType = averageClubPlayerIndicatorsChart.getDataType();
  $scope.clubs = [];
  $scope.offenders = true;
  $scope.defenders = true;
  this.clubPk = document.getElementById('team-id').value;
  $scope.$watch('field', function() {
    if ($scope.clubs.length > 0) {
      return $scope.listAveragePlayer();
    }
  });
  $scope.setSelectedPlayer = function(obj) {
    if ((obj != null) && (obj.originalObject != null)) {
      return $scope.selectedPlayer = obj.originalObject;
    }
  };
  $scope.addAverageClubPlayerData = function(clubPk) {
    var pk, url;
    if (($scope.selectedClub == null) && (clubPk == null)) {
      return;
    }
    if (($scope.selectedClub != null) && ($scope.selectedClub.originalObject != null)) {
      pk = $scope.selectedClub.originalObject.pk;
    }
    if (pk == null) {
      if (clubPk != null) {
        pk = clubPk;
        $scope.selectedClub = {
          originalObject: {
            title: document.getElementById('team-name-hidden').value,
            pk: clubPk,
            color: null,
            logo: document.getElementById('club-logo').value
          }
        };
      } else {
        return;
      }
    }
    url = $('#club-team-api').val();
    $http.get(url).success(function(data, status, headers) {
      var players, queries;
      LocaleFactory.setLocale(headers()['content-language']);
      players = data.all_players = _.filter(data.all_players, function(player) {
        return player.line > 1;
      });
      queries = [];
      _.each(players, function(player) {
        player.selected = true;
        queries.push($http.get(self.url.replace('/0/', '/' + player.pk + '/') + '?group_by=season'));
      });
      $scope.loader = true;
      $q.all(queries).then(function(results) {
        var clubObject, lastSeasonResult;
        $scope.loader = false;
        lastSeasonResult = _.last(results[0].data.results);
        clubObject = {
          all_players: data.all_players,
          offender_players: data.offender_players,
          defender_players: data.defender_players,
          title: data.title,
          color: data.main_color || getRandomColor(),
          id: data.pk,
          logo: data.logo,
          address: data.address,
          dataBySeason: {
            results: [
              {
                season: lastSeasonResult['season']
              }
            ]
          },
          results: results
        };
        $scope.clubs.push(clubObject);
        $timeout(function() {
          return $scope.listAveragePlayer();
        }, 100);
      });
    });
  };
  $scope.addPlayerToClub = function(title) {
    var club;
    club = _.findWhere($scope.clubs, {
      title: title
    });
    return $q.all([$http.get(self.url.replace('/0/', '/' + $scope.selectedPlayer.pk + '/') + '?group_by=season')]).then(function(results) {
      $scope.selectedPlayer.selected = true;
      $scope.selectedPlayer.added = true;
      club.all_players.push($scope.selectedPlayer);
      club.results.push(results[0]);
      return $scope.listAveragePlayer();
    });
  };
  $scope.togglePlayerSelection = function(title, index) {
    var club, player;
    club = _.findWhere($scope.clubs, {
      title: title
    });
    player = club.all_players[index];
    player.selected = !player.selected;
    $('#player_' + index).attr('checked', !$('#player_' + index).attr('checked'));
    return $scope.listAveragePlayer();
  };
  $scope.listAveragePlayer = function() {
    var newPlayerIndicatorsData;
    newPlayerIndicatorsData = [];
    _.each($scope.clubs, function(club) {
      var averageData, clubObject, key, selectedPlayers;
      selectedPlayers = _.countBy(_.filter(club.all_players, function(player) {
        return player.line === 3 && $scope.offenders === true || player.line === 2 && $scope.defenders === true;
      }), {
        selected: true
      })['true'];
      for (key in _.last(club.results[0].data.results)) {
        if (_.contains(ALL_FIELDS, key)) {
          averageData = 0;
          _.each(club.results, function(result) {
            var player;
            player = _.findWhere(club.all_players, {
              pk: Number(result.config.url.match("players\/(.*)\/indicators")[1])
            });
            player.result = _.last(result.data.results)[$scope.field];
            if (player.line === 3 && !$scope.offenders || player.line === 2 && !$scope.defenders) {
              return;
            }
            if (player.selected === true) {
              averageData += parseFloat(_.last(result.data.results)[key]);
            }
          });
          averageData = parseFloat(averageData / selectedPlayers).toFixed(3);
          club.dataBySeason.results[0][key] = averageData;
        }
      }
      clubObject = {
        name: club.title,
        data: club.dataBySeason.results.map(function(el) {
          return {
            x: new Date(el.season.end_date.split('-')[0]).getTime(),
            y: parseFloat(el[$scope.field]),
            drilldown: el.season.end_date
          };
        }),
        color: club.color,
        stack: club.id
      };
      return newPlayerIndicatorsData.push(clubObject);
    });
    averageClubPlayerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData);
    averageClubPlayerIndicatorsChart.setContext($scope);
    averageClubPlayerIndicatorsChart.setPeriod(30);
    averageClubPlayerIndicatorsChart.draw();
    return self.chart = $('#chartdiv').highcharts();
  };
  $scope.addAverageClubPlayerData(this.clubPk);
});

angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout', 'MapService',
    function($http, $scope, $timeout, MapService) {
        var self = this,
        url = document.getElementById("club-team-api").value,//$('#ClubTeamForm').attr('action'),
        popup = null;
        $scope.type = 'all';
        $scope.cache_players = null;
        $scope.cache_clubs = null;
        $scope.notplaying_players = null;
        $scope.state = 'fio';
        $scope.season = 19;

        $scope.setType = function(type){
            $scope.type = type;
            $scope.unMakeTransferArrows();
        };

        $scope.setState = function(state){
            $scope.state = state;
            $scope.getFromCache();
            //if($scope.state = 'is_joined'){
            //    $timeout(function(){
            //        $scope.makeTransferArrows();
            //    }, 500)
            //}
        };

        $scope.playerFilter = function(value){
            if($scope.state === 'coaches') return false;
            return value[$scope.state] != false;
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

        $scope.setSeason = function(season) {
            $scope.season = season;
            self.list(self.compare);
        };

        $scope.workWithData = function(data){
            //if(MapService.isRendered()) MapService.remove();
            //MapService.createClubsMap(data.all_players, 'players');
            var giveCountryCodes = function(player){
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
            }
            var all_players = data.all_players;
            var players = [];
            _.each(all_players, function(player){
                players.push(player.pk);
            })
            _.each(data.all_players, giveCountryCodes)
            _.each(data.goalkeeper_players, giveCountryCodes)
            _.each(data.offender_players, giveCountryCodes)
            _.each(data.defender_players, giveCountryCodes)
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
            var params = 'season=' + $scope.season;//$('#ClubTeamForm').serialize();
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
            $scope.setState('fio');
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

        self.list();

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

var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

angular.module('Sportomatics').controller('NumbersController', [
  '$http', '$scope', '$location', function($http, $scope, $location) {
    var club, player, url;
    $scope.$location = $location;
    url = $('#PlayerNumbersApi').attr('href');
    club = $('[name="club"]').val();
    player = $('[name="player"]').val();
    $scope.limit = {};
    $scope.data = {};
    $scope.params = $location.search();
    $scope.PlayerPartnersPopup = {
      'data': null,
      'isClubsVisible': false
    };
    $scope.PlayerPartnersPopupShow = function(player, $event) {
      var popup;
      popup = $('.player-partners-popup:hidden');
      url = $('#PlayerCardLink').attr('href');
      if (popup.length) {
        $scope.PlayerPartnersPopup.data = null;
        $http.get(url.replace(0, player.pk)).success(function(data) {
          $scope.PlayerPartnersPopup.data = data;
        });
        $('.player-partners-popup:hidden').show(500).offset({
          'left': $event.pageX,
          'top': $event.pageY
        });
      }
    };
    $scope.getLimit = function(number) {
      if (!$scope.limit[number]) {
        $scope.limit[number] = 4;
      }
      return $scope.limit[number];
    };
    $scope.increaseLimit = function(number) {
      $scope.limit[number] += 4;
    };
    $scope.getSeasonsCount = function(group) {
      var clubplayer, clubplayers, i, j, k, len, len1, ref, ref1, ref2;
      i = 0;
      clubplayers = [];
      ref = group.clubs;
      for (j = 0, len = ref.length; j < len; j++) {
        club = ref[j];
        ref1 = club.clubplayers;
        for (k = 0, len1 = ref1.length; k < len1; k++) {
          clubplayer = ref1[k];
          if (ref2 = clubplayer.pk, indexOf.call(clubplayers, ref2) < 0) {
            clubplayers.push(clubplayer.pk);
            i += 1;
          }
        }
      }
      return i;
    };
    $scope.setSeason = function(season) {
      $location.search('season', season || null);
      $scope.params = $location.search();
      return $scope.list();
    };
    $scope.list = function() {
      var params;
      params = '';
      if (club) {
        params += '&club=' + club;
      }
      if (player) {
        params += '&player=' + player;
      }
      if ($scope.params.season) {
        params += '&season=' + $scope.params.season;
      }
      $scope.loaded = false;
      $http.get(url + '?' + params).success(function(data) {
        $scope.data = data;
        $scope.loaded = true;
      });
    };
    $scope.list();
  }
]);

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
    .controller('PlayerCardIndicatorsController', function($http, $scope, $timeout, LocaleFactory, $state, $location, $q, HighchartsFactory) {
        //http://www.amcharts.com/lib/images/
        var self = this;
        var url = (document.getElementById('api-player-indicators') != null) ? document.getElementById('api-player-indicators').value : '';
        this.url = url;
        var playerIndicatorsChart = new HighchartsFactory.PlayerIndicatorsChart();
        $scope.field = playerIndicatorsChart.getField();
        $scope.setField = playerIndicatorsChart.setField;
        $scope.localeObject = LocaleFactory.selectedLocale;
        this.club = parseInt($location.search()['club']) || null;
        this.coach = parseInt($location.search()['coach']) || null;
        this.compare_to = parseInt($location.search()['compare_to']) || null;
        this.groupBy = 'season';
        this.data = [];
        this.graphData = {};
        this.playerId = (document.getElementById('player-id') != null) ? document.getElementById('player-id').value : '';
        this.playerName = (document.getElementById('player-name') != null) ? document.getElementById('player-name').value : '';
        this.playerColor = (document.getElementById('player-color') != null) ? document.getElementById('player-color').value : '';
        this.playerClubs = document.getElementById('player-clubs');
        this.urlClub = (document.getElementById('url-club') != null) ? document.getElementById('url-club').value.replace('0/', '') : '';
        $scope.apiPlayersUrl = (document.getElementById('api-players-url') != null) ? document.getElementById('api-players-url').value : '';
        $scope.limited = false; // user is not limited by default
        $scope.activeSeason = -1; // all seasons selected by default (index of all seasons is -1)
        $scope.playersToCompare = [];
        $scope.radarPlayers = []; // array of players to compare in radar chart
        $scope.playerToCompare = { // last found player to compare with
            id: this.compare_to
        };
        $scope.currentPlayerObject = { // object of current player
            id: self.playerId,
            title: self.playerName,
            color: self.playerColor ? self.playerColor : "#408e3a"
        };
        $scope.dataType = 'graph-serial'; // we'll be on serial chart tab by default

        $scope.setDataType = function(type, event){
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
                $timeout(function(){
                    $scope.createRadar();
                }, 100)
            } else {
                if(event.originalEvent != null){
                    $timeout(function(){
                        $scope.makeChart();
                    }, 100)
                }
            }
        };

        $scope.addRadarGraph = function(id, preventCreation){
            if(_.findWhere($scope.radarPlayers, {id: id})) return;
            $http.get($scope.apiPlayersUrl + id)
                .success(function(player){
                    $http.get($scope.apiPlayersUrl + id + '/indicators/?group_by=season')
                        .success(function(data){
                            $scope.radarPlayers.push({
                                id: id,
                                color: player.club.main_color || null,
                                fio: player.fio,
                                dataBySeason: data
                            })
                            if(preventCreation == null)
                            $scope.createRadar();
                            $scope.addGraph(id, true);
                        })
                })
        };

        $scope.$on('field-changed', function(event, preventList){
            $location.search('field', field);
            console.log(preventList)
            if(preventList == null)
            self.list();
        })

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

        $scope.setSelectedPlayer = function(selectedPlayer){
            if (selectedPlayer == null){
                $location.search('compare_to', null);
                $scope.playerToCompare = {}
            } else {
                $scope.playerToCompare = selectedPlayer.originalObject
            }
        }

        $scope.addGraph = function(id, preventCreation){
            if(!id || _.findWhere($scope.playersToCompare, {id: id})) return;
            $location.search('compare_to', id);
            $http.get($scope.apiPlayersUrl+id)
                .success(function(data){
                    $scope.playerToCompare.photo = data.photo;
                    $scope.playerToCompare.name = data.name + ' ' + data.lastname;
                    $scope.playerToCompare.club = data.club;
                    var playerObject = {
                        title: $scope.playerToCompare.name || id,
                        color: $scope.playerToCompare.club.main_color || getRandomColor(),
                        id: id,
                        link: $scope.apiPlayersUrl + id + '/indicators/'
                    };
                    var url = playerObject.link;
                    self.loader = true;
                    $http.get(url + '?group_by=month')
                        .success(function(data){
                            playerObject.dataByMonth = data;
                        }).then(function(){
                            $http.get(url + '?group_by=season')
                                .success(function(data){
                                    playerObject.dataBySeason = data;
                                    $scope.dataBySeason.results = _.sortBy($scope.dataBySeason.results.concat(_.filter(data.results, function(result){
                                        return !_.filter($scope.dataBySeason.results, function(el){
                                            return el.season.end_date === result.season.end_date
                                        }).length
                                    })), function(el){ return new Date(el.season.end_date.split('-'))})
                                    self.loader = false;
                                }).then(function(){
                                    $scope.playersToCompare.push(playerObject);
                                    $scope.addRadarGraph(id, true);
                                    if(preventCreation == null)
                                    $scope.makeChart();
                                })
                        })
                })
        };

        $scope.makeChart = function(){ // make column chart with multiple players
            if(self.chart)
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 365;
            var results = [];
            if($scope.activeSeason === -1){ //make chart grouped by seasons
                _.each($scope.playersToCompare, function(playerObject, index){
                    if(index === 0) return;
                    var newPlayerIndicatorsData = {
                        name: playerObject.title,
                        data: playerObject.dataBySeason.results.map(function(el){
                            return {
                                x: new Date(el.season.end_date.split('-')[0]).getTime(),
                                y: parseFloat(el[$scope.field]),
                                drilldown: el.season.end_date
                            }
                        }),
                        color: playerObject.color,
                        stack: playerObject.id
                    }
                    results.push(newPlayerIndicatorsData);
                    if(!_.findWhere(self.chart.series, {name: newPlayerIndicatorsData.name}))
                    self.chart.addSeries(newPlayerIndicatorsData);
                })
            } else { // make chart on some season
                _.each($scope.playersToCompare, function(playerObject, index){
                    if(playerObject.dataByMonth == null) return;
                    var versions = _.groupBy(playerObject.dataByMonth.results, function(result){
                        if (result.season != null)
                            if(result.season.end_date === $scope.drilldown)
                                return result.season.end_date;
                    })
                    if(versions[$scope.drilldown] != null)
                    results.push({
                        name: playerObject.title,
                        stack: playerObject.id,
                        data: versions[$scope.drilldown].map(function(el){
                            return {
                                x: new Date(el.date).getTime(),
                                y: parseFloat(el[$scope.field])
                            }
                        }),
                        color: playerObject.color
                    })
                })

                playerIndicatorsChart.init('chartdiv', results, $scope.field)
                playerIndicatorsChart.setContext($scope);
                playerIndicatorsChart.setPeriod(30);
                playerIndicatorsChart.draw();
                self.chart = $('#chartdiv').highcharts();
            }
        };

        $scope.isDisabled = function(season){
            return _.contains(KHL_NEWEST_FIELDS, $scope.field) && (parseInt(season.end_date.split('-')[0]) < 2009 );
        };

        $scope.setGroupBy = function(groupby){
            self.groupBy = groupby;
            self.data = (groupby === 'month') ? $scope.dataByMonth : $scope.dataBySeason;
            $scope.onSeason = false;
            self.list();
            $scope.activeSeason = -1;
        };

        $scope.moveToSeason = function(season, index, date, fromAnotherChart){
            if(index !== -1 && _.contains(KHL_NEWEST_FIELDS, $scope.field) && (parseInt(season.end_date.split('-')[0]) < 2009 )) return;
            var chart = $('#chartdiv').highcharts();
            if(index === -1 || $scope.activeSeason === index && !fromAnotherChart) {
                $scope.activeSeason = -1;
                self.list();
                return;
            }
            $scope.activeSeason = index;
            self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
            if ($scope.currentPlayerObject.dataByMonth != null){
                $scope.drilldown = (date != null) ? date : $scope.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                $scope.makeChart()
            } else {
                $scope.getPlayerDataByMonth().then(function(){
                    $scope.drilldown = (date != null) ? date : $scope.dataBySeason.results[index].season.end_date; //self.chart.series[0].points[index].drilldown;
                    $scope.makeChart()
                })
            }
        };

        this.list = function() {

            if($scope.selectedClub) return this.listAvergePlayer();
            if($('.club-id').length !== 0) return this.listClubs();

            if($scope.initialDataBySeason == null) return
            if($scope.activeSeason !== -1) return $scope.makeChart();

            var newPlayerIndicatorsData = [{
                name: $scope.currentPlayerObject.title,
                data: $scope.initialDataBySeason.results.map(function(el){
                    return {
                        x: new Date(el.season.end_date.split('-')[0]).getTime(),
                        y: parseFloat(el[$scope.field]),
                        drilldown: el.season.end_date
                    }
                }),
                color: $scope.currentPlayerObject.color,
                stack: 'hi'
            }]

            self.loader = false;

            playerIndicatorsChart.init('chartdiv', newPlayerIndicatorsData, $scope.field)
            playerIndicatorsChart.setContext($scope);
            playerIndicatorsChart.draw();
            self.chart = $('#chartdiv').highcharts();
            if ($scope.playersToCompare.length > 1) {
                if($scope.activeSeason === -1){
                    $scope.makeChart(); //player comparison
                }
            }
            //self.chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;

            $scope.lastSeason = Math.max.apply(Math,$scope.dataBySeason.results.map(function(o){return parseInt(o.season.end_date.substr(0, 4));})).toString();
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

            /*if ($scope.limited) { //not registered users
             $scope.chart.chartCursor = null;
             $scope.chart.chartScrollbar = null;
             $scope.chart.startDuration = null;
             for(var i = 0; i < $scope.chart.graphs.length; i ++){
             $scope.chart.graphs[i].balloonText = '';
             $scope.chart.graphs[i].visibleInLegend = false;
             }
             delete $scope.chart.exportConfig
             }*/

        };

        this.listClubs = function(){

            var queries = [];
            var clubs = [];
            var graphs = [];
            //TODO заменить на обращение к апи
            $('.club-id').each(function(index, value){
                var club = $(value).attr('id').split('_');
                var params = '?group_by=season&club=' + club[1];
                clubs.push({
                    title: club[0],
                    pk: club[1],
                    main_color: club[2]
                });
                queries.push($http.get(url + params))
            });
            self.loader = true;
            $q.all(queries).then(function(results, a){
                _.each(results, function(result){
                    _.each(clubs, function(club){
                        if(club.pk === getParameterByName(result.config.url, 'club')){
                            club.seasons = [];
                            club.results = result.data.results;
                            _.each(result.data.results, function(clubResult){
                                club.seasons.push (new Date(clubResult.season.end_date).getFullYear());
                            })
                        }
                    })
                });

                var newData = [];
                _.each(clubs, function(club){
                    var object = {
                        name: club.title,
                        stack: 'season',
                        data: club.results.map(function(clubResult){
                            return [new Date(clubResult.season.end_date.split('-')[0]).getTime(), parseFloat(clubResult[$scope.field])]
                        }),
                        club: club,
                        color: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? "#699c97" : "#408e3a" ) : (club.main_color.length === 0) ? null : club.main_color,
                        showInLegend: (self.club != null) ? ((club.pk.toString() === self.club.toString()) ? true : false ) : null,
                    }
                    newData.push(object)
                })

                if(document.getElementById('isPlayerShort') == null){ //player-clubs page

                    self.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsChart('chartdiv', newData, $scope.field);
                    playerClubsChart.draw();
                    document.getElementById('chartdiv').style.marginLeft = '-15px'

                } else {
                    var newDataPie = newData.map(function(el){
                        return {
                            name: el.name,
                            y: _.reduce(el.data, function(pv, cv){ return pv + cv[1] }, 0),
                            pk: el.club.pk,
                            url: self.urlClub + el.club.pk + '?season=' + toSeason(el.club.seasons[0])
                        };
                    })
                    self.loader = false;
                    var playerClubsChart = new HighchartsFactory.PlayerClubsPieChart('chartdiv', newDataPie, $scope.field);
                    playerClubsChart.draw();
                }

            })

        }; //List clubs

        $scope.initialPlayerObject = {}
        $scope.getPlayerData = function(){
            self.loader = true;
            if($('#clubs-compare').length > 0) return $scope.addAverageClubPlayerData();
            $http.get(url + '?group_by=season')
                .success(function(data, status, headers) {
                    //if(data.is_limited) $scope.limited = true;
                    self.locale = headers()['content-language']; // determine language locale
                    $scope.localeObject = LocaleFactory['locale_'+self.locale]; // set locale object to use in js
                    $scope.initialDataBySeason = {};
                    angular.copy(data, $scope.initialDataBySeason);
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
                        $scope.playersToCompare.push($scope.currentPlayerObject);
                        self.list();
                    }
                })
        };

        $scope.getPlayerDataByMonth = function(callback){
            var deferred = $q.defer();
            if($scope.dataByMonth != null) deferred.resolve(true)
            else{
                self.loader = true;
                $http.get(url + '?group_by=month')
                    .success(function(data){
                        self.loader = false;
                        $scope.dataByMonth = data;
                        $scope.currentPlayerObject.dataByMonth = data;
                        deferred.resolve(data);
                    })
            }
            return deferred.promise;
        };

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
            if(self.club == null) return self.listClubs();
            var params = '?group_by=season&club=' + self.club;
            self.loader = true;
            $http.get(url + params)
                .success(function(data) {
                    $scope.clubData = data;
                    self.loader = false;
                    self.list();
                })
        };

        $scope.availableFields = _.toArray(LocaleFactory.locale_ru.fieldNames); // generate available fields
        _.each($scope.availableFields, function(object){
            object.ticked = !!(object.field === 'points' || object.field === 'goals' || object.field === 'assists' || object.field === 'plus_minus');
        });

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
            if(newval && $scope.lastSeason && $scope.dataType === 'graph-radar'){
                $scope.createRadar()
            }
        }, true);

        $scope.$watch('lastSeason', function(newval){
            if(newval && $scope.dataType === 'graph-radar'){
                $scope.createRadar()
            }
        });

        $scope.createRadar = function(){ // function to create radar chart for one or multiple players
            var categories = $scope.selectedRadarFields.map(function(el){ return el['field']; });
            var data = $scope.initialDataBySeason.results.map(function(el){
                if(el.season.end_date.indexOf($scope.lastSeason) > -1){
                    return {
                        name: self.playerName,
                        data: categories.map(function(category){
                            if(category === 'shots') return (parseInt(el[category])/10) / parseInt(el['count']);
                            return parseInt(el[category]) / parseInt(el['count']);
                        }),
                        pointPlacement: 'on',
                        color: $scope.currentPlayerObject.color
                    }
                }
            }).filter(function(toFilter){ return toFilter != undefined; });
            $scope.playerSeasons = $scope.dataBySeason.results.map(function(e){ return e.season.end_date.substr(0,4); });

            $scope.playerStatsSpiderChart = new HighchartsFactory.PlayerStatsSpiderChart('chartdiv2', data, categories, $scope.lastSeason);
            $scope.playerStatsSpiderChart.setContext($scope);
            $scope.playerStatsSpiderChart.setLocaleObject($scope.localeObject);
            $scope.playerStatsSpiderChart.draw();
            self.spiderChart = $("#chartdiv2").highcharts();

            if($scope.radarPlayers.length > 0){
                _.each($scope.radarPlayers, function(playerObject){
                    var data = playerObject.dataBySeason.results.map(function(el){
                        if(el.season.end_date.indexOf($scope.lastSeason) > -1){
                            return {
                                name: playerObject.fio,
                                data: categories.map(function(category){
                                    if(category === 'shots') return (parseInt(el[category])/10) / parseInt(el['count']);
                                    return parseInt(el[category]) / parseInt(el['count']);
                                }),
                                pointPlacement: 'on'
                            }
                        }
                    }).filter(function(toFilter){ return toFilter != undefined; });
                    self.spiderChart.addSeries(data[0]);
                    var playerSeasons = playerObject.dataBySeason.results.map(function (e) { return e.season.end_date.substr(0, 4); });
                    $scope.playerSeasons = _.uniq($scope.playerSeasons.concat(playerSeasons)).sort();
                })
            }
        };

        // RUN

        $scope.getPlayerData();
    })

    function toSeason(value){
        //TODO заменить
        var seasons = {
            s2002: 1,
            s2003: 2,
            s2001: 3,
            s2004: 4,
            s2000: 5,
            s1999: 6,
            s1998: 7,
            s2005: 8,
            s2006: 9,
            s1997: 10,
            s2007: 11,
            s2008: 12,
            s2009: 13,
            s2010: 14,
            s2011: 15,
            s2012: 16,
            s2013: 17,
            s2014: 18,
            s2015: 19
        }
        return seasons['s'+value];
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
                    $scope.loaded = false;
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
                            $scope.loaded = true;
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

angular.module('Sportomatics').controller('PlayersSearch2Controller', [
  '$http', '$scope', '$location', 'PlayersSearchService', 'tags', '$timeout', function($http, $scope, $location, PlayersSearchService, tags, $timeout) {
    $scope.tags = tags;
    $timeout(function() {
      return $('.ui.dropdown').dropdown();
    }, 0);
    $scope.loadCountries = function(query) {
      return $scope.tags.loadCountries($scope.countriesURL, query);
    };
    $scope.loadClubs = function(query) {
      return $scope.tags.loadClubs($scope.clubsURL, query);
    };
    $scope.loadPlayers = function(query) {
      return $scope.tags.loadPlayers($scope.playersURL, query);
    };
    $scope.loadLeagues = function(query) {
      return $http.get($scope.leaguesURL);
    };
    $scope.PlayersSearchService = PlayersSearchService;
    $scope.$location = $location;
    $scope.data = {};
    $scope.countries = [];
    $scope.loader = false;
    $scope.params = $location.search();
    if ($scope.params.citizenship) {
      $scope.citizenship = JSON.parse($scope.params.citizenship);
    }
    if ($scope.params.club) {
      $scope.club = JSON.parse($scope.params.club);
    }
    if ($scope.params.league2) {
      $scope.league2 = JSON.parse($scope.params.league2);
    }
    if ($("#ageRange").length) {
      $("#ageRange").ionRangeSlider({
        'hide_min_max': true,
        'keyboard': true,
        'min': 15,
        'max': 65,
        'from': $scope.params.age__lte || 15,
        'to': $scope.params.age__gte || 65,
        'type': 'double',
        'step': 1,
        'grid': false
      });
    }
    if ($("#relatedRange").length) {
      $("#relatedRange").ionRangeSlider({
        'hide_min_max': true,
        'keyboard': true,
        'min': 0,
        'max': 100,
        'from': $scope.params.related_value__gte || 40,
        'to': $scope.params.related_value__lte || 80,
        'type': 'double',
        'step': 1,
        'grid': false
      });
    }
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
    $scope.setCountry = function(country) {
      $scope.setLeague('');
      $location.search('country', country || null);
      $timeout(function() {
        return $('.ui.dropdown.leagues').dropdown();
      }, 0);
    };
    $scope.setLeague = function(league) {
      if (!league) {
        $('.ui.dropdown.leagues .text').text('');
      }
      $location.search('league', league || null);
    };
  }
]);

angular.module('Sportomatics').controller('PlayersSearchController', [
  '$http', '$scope', '$location', 'PlayersSearchService', 'tags', '$timeout', function($http, $scope, $location, PlayersSearchService, tags, $timeout) {
    $scope.tags = tags;
    $timeout(function() {
      return $('.ui.dropdown').dropdown();
    }, 0);
    $scope.loadCountries = function(query) {
      return $scope.tags.loadCountries($scope.countriesURL, query);
    };
    $scope.loadClubs = function(query) {
      return $scope.tags.loadClubs($scope.clubsURL, query);
    };
    $scope.loadPlayers = function(query) {
      return $scope.tags.loadPlayers($scope.playersURL, query);
    };
    $scope.loadLeagues = function(query) {
      return $http.get($scope.leaguesURL);
    };
    $scope.getUnchecker = function(isDefault, defaultValue) {
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
    if ($scope.params.citizenship) {
      $scope.citizenship = JSON.parse($scope.params.citizenship);
    }
    if ($scope.params.club) {
      $scope.club = JSON.parse($scope.params.club);
    }
    if ($scope.params.league2) {
      $scope.league2 = JSON.parse($scope.params.league2);
    }
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
        $('input[name="line"]').each($scope.getUnchecker(isDefault, defaultValue));
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
        $('input[name="contract_types"]').each($scope.getUnchecker(isDefault, ''));
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
    $scope.setCountry = function(country) {
      $scope.setLeague('');
      $location.search('country', country || null);
      $timeout(function() {
        return $('.ui.dropdown.leagues').dropdown();
      }, 0);
    };
    $scope.setLeague = function(league) {
      if (!league) {
        $('.ui.dropdown.leagues .text').text('');
      }
      $location.search('league', league || null);
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

angular.module('Sportomatics').controller('ClubCoachesController', function($scope, $timeout) {
  $scope.seasonsData = [];
  $scope.seasonsDataInitial = [
    {
      title: 'Сезон 2014-2015',
      coaches: [
        {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }
      ]
    }, {
      title: 'Сезон 2013-2014',
      coaches: [
        {
          fio: 'Иванов Вячеслав',
          role: 'помощник тренера'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }, {
          fio: 'Иванов Вячеслав',
          role: 'главный тренер'
        }
      ]
    }
  ];
  $scope.loadSeason = function() {
    var loader;
    $scope.loader = true;
    loader = $('.loader');
    loader.addClass('active');
    return $timeout(function() {
      $scope.seasonsData.push($scope.seasonsDataInitial[0]);
      return loader.removeClass('active');
    }, 1000);
  };
  $('.b-tabs-content').visibility({
    once: false,
    observeChanges: true,
    onBottomVisible: function() {
      console.log('bottom');
      return $scope.loadSeason();
    }
  });
});

angular.module('Sportomatics').controller('ClubGeographyController', function($http, MapService) {
  var clubTeamApi;
  clubTeamApi = document.getElementById("club-team-api").value;
  $http.get(clubTeamApi + '?season=19').success(function(data) {
    if (MapService.isRendered() === true) {
      MapService.remove();
    }
    return MapService.createClubsMap(data.all_players, 'players');
  });
});
