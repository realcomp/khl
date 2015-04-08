angular.module('Sportomatics').factory 'ClubChartsFactory', ($q, $timeout, AmChartsFactory, zoomData) ->

    class PlayerClubsChart

        constructor: (@data, @graphs) ->

        init: () ->

        #data should be an array with values
        setData: (@data) ->

        create: (field, chartData, localeObject, graphs, player) ->
            # Method accepts
            deferred = $q.defer()
            chart = undefined
            AmChartsFactory.ready().then ->
                data = chartData.data
                # SERIAL CHART
                chart = new (AmCharts.AmSerialChart)
                chart.pathToImages = 'http://www.amcharts.com/lib/images/'
                chart.dataProvider = data
                chart.categoryField = 'end_date'
                chart.cursorColor = '#DADADA'
                chart.startDuration = 0.5
                chart.startEffect = 'easeOutSine'
                chart.addClassNames = true
                chart.depth3D = 60
                chart.angle = 30
                chart.exportConfig =
                    'menuTop': '45px'
                    'menuRight': '5px'
                    'menuItems': [ {
                        'icon': 'http://www.amcharts.com/lib/3/images/export.png'
                        'format': 'png'
                    } ]
                # listen for "dataUpdated" event (fired when chart is inited) and call zoomChart method when it happens
                chart.addListener 'dataUpdated', zoomChart
                chart.addListener 'zoomed', (chart) ->
                    zoomData.startDate = chart.startDate
                    zoomData.endDate = chart.endDate
                    return
                # AXES
                # category
                categoryAxis = chart.categoryAxis
                categoryAxis.parseDates = true
                categoryAxis.minPeriod = if `chartData.groupBy == 'month'` then 'MM' else 'YYYY'
                categoryAxis.equalSpacing = true
                categoryAxis.minHorizontalGap = 40
                categoryAxis.gridAlpha = 0
                categoryAxis.boldPeriodBeginning = false
                categoryAxis.axisColor = '#DADADA'
                categoryAxis.markPeriodChange = false
                categoryAxis.dateFormats = [
                    {
                        period: 'MM'
                        format: 'MMM'
                    }
                    {
                        period: 'YYYY'
                        format: 'YYYY'
                    }
                ]

                categoryAxis.labelFunction = (valueText, date, categoryAxis) ->
                    value = new Date(date)
                    if `chartData.groupBy == 'season'`
                        endDate = valueText.substr(2, 2)
                        startDate = if `endDate == '00'` then '99' else (parseInt(endDate) - 1).toString()
                        if `startDate.length == 1`
                            startDate = '0' + startDate
                        return startDate + '/' + endDate
                    if `valueText == 'Jan'`
                        return localeObject.monthNames[value.getMonth()] + '\n' + value.getFullYear()
                    localeObject.monthNames[value.getMonth()]

                currMax = Math.max.apply(Math, data.map((e) ->
                    e['values']
                ))
                currMin = Math.min.apply(Math, data.map((e) ->
                    e['values']
                ))

                # VALUE AXIS
                valueAxis1 = new (AmCharts.ValueAxis)()
                valueAxis1.axisColor = '#408e3a'
                valueAxis1.axisThickness = 1
                valueAxis1.stackType = "regular"
                valueAxis1.axisAlpha = 0
                valueAxis1.gridAlpha = 0
                chart.addValueAxis valueAxis1

                if graphs and graphs.length
                    oneBalloon = '<p style=\'text-align: left;\'><span style=\'font-size:14px; color:#000000;\'>[[value]]</span></p>'
                    balloons = '<div class=\'inline-block text-left\'><p style=\'text-align: left;\'><span style=\'font-size:14px; color:#000000;\'><b>' + localeObject.fieldNames[field].fullName + '</b></span></p>'
                    _.each graphs, (graph, index) ->
                        balloons += createBalloon(graph.valueField, graph.title)
                        graph.valueAxis = valueAxis1
                        #graph.balloonText = if index < graphs.length - 1 then '' else balloons + '</div><div class="inline-block season-balloon"><div class="balloon-div">Сезон 06/07</div></div> '
                        return
                    _.each graphs, (graph, index) ->
                        #graph.balloonText = balloons; #+ '</div><div class="inline-block season-balloon"><div class="balloon-div">Сезон 06/07</div></div> '
                        graph.lineColorField = 'lineColor'
                        graph.fillColorsField = 'lineColor'
                        chart.addGraph graph
                        return

                # SCROLLBAR
                chartScrollbar = new (AmCharts.ChartScrollbar)
                chartScrollbar.autoGridCount = true
                chartScrollbar.color = '#000000'
                chart.addChartScrollbar chartScrollbar

                # LEGEND
                legend = new (AmCharts.AmLegend)
                legend.marginLeft = 110
                legend.useGraphSettings = true
                chart.addLegend legend
                # LABEL
                chart.allLabels = [ {
                    align: 'center'
                    y: 60
                    alpha: 0.7
                    bold: true
                    text: localeObject.fieldNames[field].fullName.toUpperCase()
                } ]
                # CURSOR
                chartCursor = new (AmCharts.ChartCursor)
                chartCursor.cursorAlpha = 1
                chartCursor.cursorColor = '#8ebd5d'
                #chartCursor.avoidBalloonOverlapping = false;
                chartCursor.oneBalloonOnly = true

                chartCursor.categoryBalloonFunction = (value) ->
                    if `chartData.groupBy == 'month'`
                        localeObject.monthNames[value.getMonth()] + ' ' + value.getFullYear()
                    else
                        localeObject.words.season + (value.getFullYear() - 1).toString().substr(2, 2) + '/' + value.getFullYear().toString().substr(2, 2)

                chart.addChartCursor chartCursor
                deferred.resolve chart
                return
            deferred.promise

    return PlayerClubsChart: PlayerClubsChart