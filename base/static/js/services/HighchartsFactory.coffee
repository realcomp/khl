angular.module('Sportomatics').factory 'HighchartsFactory', () ->

    class HighchartsClubGamesChart

        constructor: (@divId, @data) ->

        setLocaleObject: (@localeObject) ->

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    alignTicks: false
                title:
                    'Счет в матчах'
                xAxis: [
                    {
                        labels:
                            enabled: false
                            align: 'center'
                            autoRotation: false
                            step: 1
                        reversed: false
                        lineColor: '#FFFFFF'
                        tickInterval: 1
                        min: -0.5
                        max: 54.5
                    },
                    {
                        opposite: true,
                        reversed: false,
                        linkedTo: 0,
                        labels:
                            enabled: false
                            step: 1
                        lineColor: '#FFFFFF'
                        min: -0.5
                        max: 54.5
                    }
                ]
                yAxis:
                    title: 'Счет'
                    allowDecimals: false
                    labels:
                        formatter: () ->
                            return Math.abs this.value
                    stackLabels:
                        formatter: () ->
                            return this
                #scrollbar:
                    #enabled: true
                legend:
                    margin: 30
                tooltip:
                    #shared: true
                    useHTML: true
                    formatter: () ->
                        return '<div class="text-center"> <b>Матч <br>' + this.point.name + '<b> <br><br>' + this.point.date + '<br> Счет <br>' + this.point.score
                plotOptions:
                    series:
                        stacking: 'normal'
                series: @data


    class HighchartsPlayerClubsChart

        constructor: (@divId, @data, @field) ->

        setLocaleObject: (@localeObject) ->

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    options3d:
                        enabled: true
                        alpha: 15
                        beta: 15
                        viewDistance: 25
                        depth: 40
                title:
                    text: @localeObject.fieldNames[@field].fullName.toUpperCase()
                xAxis:
                    "type": "datetime"
                    labels:
                        align: 'center'
                        autoRotation: false
                        formatter: () ->
                            (new Date(this.value).getFullYear()-1).toString().substr(2, 2) + '/' + (new Date(this.value).getFullYear()).toString().substr(2, 2)
                    tickInterval: 24 * 3600 * 1000 * 365
                    gridLineColor: '#FFFFFF'
                yAxis:
                    allowDecimals: false
                    min: 0
                    title:
                        text: ''
                    gridLineColor: '#FFFFFF'
                    labels:
                        enabled: false
                legend:
                    margin: 30
                tooltip:
                    headerFormat: '<b>{point.key}</b><br>'
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: {point.y} / {point.stackTotal}'
                    formatter: () ->
                        s = '<b>Сезон ' + (new Date(this.x).getFullYear()-1) + '/'+ new Date(this.x).getFullYear() + '</b>';
                        sum = 0;
                        $.each this.points, () ->
                            sum+= this.y;
                            s += '<br/>' + this.series.name + ': ' + this.y ;
                        s += '<br/><b>Всего: ' + sum
                    shared: true
                plotOptions:
                    column:
                        stacking: 'normal'
                        ###depth: 20
                        pointWidth: 20
                        pointPadding: 2
                        groupPadding: 20###
                        pointRange: 24 * 3600 * 1000 * 365
                series: @data


    class HighchartsPlayerClubsPieChart

        constructor: (@divId, @data) ->

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    plotBackgroundColor: null,
                    plotBorderWidth: null,
                    plotShadow: false
                title:
                    text: ''
                tooltip:
                    enabled: false
                plotOptions:
                    pie:
                        allowPointSelect: true,
                        cursor: 'pointer',
                        dataLabels:
                            enabled: true,
                            format: '<b>{point.name}</b>: {point.percentage:.1f} %',
                            style:
                                color: (Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black'
                series: [
                    type: 'pie',
                    name: 'Клубная карьера',
                    data: @data
                    point:
                        events:
                            click: (event) ->
                                if this.selected
                                    window.location.href = this.url
                ]


    class HighchartsPlayerIndicatorsChart

        constructor: (@divId, @data, @field) ->
            @period = self.period = 365
            self.field = @field

        setLocaleObject: (@localeObject) ->
            self.localeObject = @localeObject

        setPeriod: (@period) ->
            self.period = @period

        setContext: (@context) ->
            self.context = @context

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    options3d:
                        enabled: true
                        alpha: 0
                        beta: 15
                        viewDistance: 25
                        depth: 60
                    marginLeft: 0
                    events:
                        drilldown: (e) ->
                            if not e.seriesOptions
                                chart = @
                                ###points = this.options.series[0].data.map (el) ->
                                    return el.drilldown
                                return if not _.contains points, e.point.drilldown###
                                chart.showLoading 'Загрузка данных по месяцам ...'
                                if not self.context.dataByMonth?
                                    self.context.getPlayerDataByMonth().then (dataByMonth) ->
                                        chart.hideLoading()
                                        chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30
                                        self.context.moveToSeason(e.point.index, e.point.index, e.point.drilldown);
                                else
                                    chart.hideLoading()
                                    chart.options.plotOptions.column.pointRange = 24 * 3600 * 1000 * 30;
                                    self.context.moveToSeason(e.point.index, e.point.index, e.point.drilldown);
                title:
                    text: @localeObject.fieldNames[@field].fullName.toUpperCase()
                xAxis:
                    "type": "datetime"
                    labels:
                        align: 'center'
                        formatter: () ->
                            if this.dateTimeLabelFormat is '%Y'
                                return (new Date(this.value).getFullYear()-1).toString().substr(2, 2) + '/' + (new Date(this.value).getFullYear()).toString().substr(2, 2)
                            else
                                return self.localeObject.monthNames[new Date(this.value).getMonth()] + ' ' + (new Date(this.value).getFullYear()).toString().substr(2, 2)
                    tickInterval: 24 * 3600 * 1000 * 30
                yAxis:
                    allowDecimals: false
                    title:
                        text: ''
                    maxPadding: 0.02
                legend:
                    margin: 30
                tooltip:
                    headerFormat: '<b>{point.key}</b><br>'
                    pointFormat: '<span style="color:{series.color}">\u25CF</span> {series.name}: {point.y} / {point.stackTotal}'
                    formatter: () ->
                        if this.points[0].point.drilldown?
                            s = '<b>Сезон ' + (new Date(this.x).getFullYear()-1) + '/'+ new Date(this.x).getFullYear() + '</b>';
                            $.each this.points, () ->
                                s += '<br/>' + this.series.name + ': ' + this.y ;
                            return s
                        else
                            s = '<b>' + self.localeObject.monthNamesFull[new Date(this.x).getMonth()] + ' '+ new Date(this.x).getFullYear() + '</b>';
                            $.each this.points, () ->
                                s += '<br/>' + this.series.name + ': ' + this.y ;
                            return s
                    shared: true
                plotOptions:
                    column:
                        stacking: 'normal'
                        pointRange: 24 * 3600 * 1000 * self.period
                series: @data
                drilldown:
                    series: @drilldownSeries

        getChart: ()->
            @chart


    return (
        ClubGamesChart: HighchartsClubGamesChart
        PlayerClubsChart: HighchartsPlayerClubsChart
        PlayerClubsPieChart: HighchartsPlayerClubsPieChart
        PlayerIndicatorsChart: HighchartsPlayerIndicatorsChart
    )
