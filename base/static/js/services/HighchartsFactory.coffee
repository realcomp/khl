angular.module('Sportomatics').factory 'HighchartsFactory', () ->

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
                    maxPadding: 0.02
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
                        depth: 20
                        pointWidth: 20
                        pointPadding: 2
                        groupPadding: 20
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

        constructor: (@divId, @data) ->

        draw: () ->


    return (
        PlayerClubsChart: HighchartsPlayerClubsChart
        PlayerClubsPieChart: HighchartsPlayerClubsPieChart
    )