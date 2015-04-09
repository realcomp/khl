angular.module('Sportomatics').factory 'PieChartFactory', ($q, $timeout, AmChartsFactory, zoomData) ->

    class PlayerClubsChart

        constructor: (@data, @graphs) ->

        init: () ->

        setData: (@data) ->

        create: (chartData) ->
            # Method accepts
            deferred = $q.defer()
            AmChartsFactory.ready().then ->

                chart = new AmCharts.AmPieChart()
                chart.dataProvider = chartData
                chart.titleField = "clubTitle"
                chart.valueField = "value"
                chart.outlineColor = "#FFFFFF"
                chart.outlineAlpha = 0.8
                chart.outlineThickness = 2
                chart.urlField = "clubUrl"
                chart.startDuration = 0.3
                balloonText =  "[[title]]<br><span style='font-size:14px'><b>[[value]]</b> ([[percents]]%)</span>"
                deferred.resolve chart
                return

            deferred.promise

    return PlayerClubsChart: PlayerClubsChart