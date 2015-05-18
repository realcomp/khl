angular.module('Sportomatics').factory('HighchartsFactory', function($timeout, LocaleFactory, $location, $rootScope) {
  var HighchartsArenaVisitorsChart, HighchartsClubGamesChart, HighchartsPlayerClubsChart, HighchartsPlayerClubsPieChart, HighchartsPlayerIndicatorsChart, HighchartsSpiderChart, clubGamesFormatterDiv, indicatorsListItem;
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
          alignTicks: false,
          marginBottom: 180
        },
        title: {
          text: ''
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
          gridLineWidth: 1,
          gridLineColor: '#f7f7f7',
          minorGridLineWidth: 1,
          minorGridLineColor: '#f7f7f7',
          minorTickInterval: 'auto',
          minorTickLength: 10,
          minorTickWidth: 1,
          plotLines: [
            {
              color: '#000000',
              width: 1,
              value: 0,
              zIndex: 1
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
          hideDelay: 5000,
          shared: true,
          useHTML: true,
          crosshairs: true,
          borderWidth: 0,
          style: {
            padding: 0
          },
          shadow: false,
          positioner: function(a, b, p) {
            return {
              y: 240,
              x: p.plotX
            };
          },
          formatter: function() {
            return clubGamesFormatterDiv(this.points[0].key, this.points[0].point.score, new Date(this.points[0].point.date).yyyymmddHHMMFormatted(), this.points[0].point.leftLogo, this.points[0].point.rightLogo, this.points[0].point.color);
          }
        },
        plotOptions: {
          series: {
            stacking: 'normal',
            borderWidth: 0,
            pointWidth: 6,
            pointPadding: 2,
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
            var content, header, s;
            header = '<b>' + LocaleFactory.selectedLocale.fieldNames[self.field].fullName.toUpperCase() + '</b>';
            if (this.points[0].point.drilldown != null) {
              header = LocaleFactory.selectedLocale.fieldNames[self.field].fullName.toUpperCase() + '<br> СЕЗОН ' + (new Date(this.x).getFullYear() - 1) + '/' + (new Date(this.x).getFullYear()).toString().substr(2, 4);
              $('#legend-header').html(header);
              content = '';
              $.each(this.points, function() {
                return content += indicatorsListItem(this.y, this.series.name, this.series.options.logo, this.series.options.color);
              });
              $('#legend-content').html(content);
              return false;
            } else {
              s = '<div class="inline-block tooltip-block"><b>' + LocaleFactory.selectedLocale.monthNamesFull[new Date(this.x).getMonth()] + ' <br>' + new Date(this.x).getFullYear() + '</b></div>';
              $.each(this.points, function() {
                return s += '<div class="inline-block tooltip-block"><b>' + this.series.name + '</b>:<br>' + '<span class="tooltip-value">' + this.y + '</span></div>';
              });
              $('#legend-content').html(s);
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
  clubGamesFormatterDiv = function(title, score, date, leftLogo, rightLogo, color) {
    return '<div class="w-command-calendar__item w-command-calendar__item-bg"> <div class="b-header b-header__xs"> <h5 class="b-header__text">' + title + '</h5> </div> <div class="row"> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + leftLogo + '"> </a> </div> <p class="col-sm-2 col-md-12 col-lg-4 b-score" style="color: ' + color + '">' + score + '</p> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + rightLogo + '"> </a> </div> </div> <div class="w-command-calendar__info"> <p class="date">' + date + ' МСК </p> </div> </div>';
  };
  indicatorsListItem = function(result, title, image, color) {

    /*<p class="">
        нападающий
    </p>
     */
    return '<li class="" style="border-right: 5px solid ' + color + ';"> <div class="b-inline b-diagram__legend__table-style__item"> <div class="b-inline hidden-xs"> <a class="ui image" ><img class="ui image b-diagram__legend__image" src="' + image + '" width="32" height="32"></a> </div> <div class="b-inline"> <p class=""> <a href="#">' + title + '</a> <!--<i class="flag cz i-top-2 hidden-xs"></i>--> </p> </div> </div> <p class="b-inline b-diagram__legend__table-style__games">' + result + '</p> </li>';
  };
  return {
    PlayerStatsSpiderChart: HighchartsSpiderChart,
    ClubGamesChart: HighchartsClubGamesChart,
    ArenaVisitorsChart: HighchartsArenaVisitorsChart,
    PlayerClubsChart: HighchartsPlayerClubsChart,
    PlayerClubsPieChart: HighchartsPlayerClubsPieChart,
    PlayerIndicatorsChart: HighchartsPlayerIndicatorsChart
  };
});
