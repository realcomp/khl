angular.module('Sportomatics').factory 'HighchartsFactory', ($timeout, LocaleFactory, $location, $rootScope) ->

    class HighchartsSpiderChart

        constructor: (@divId, @data, @categories, @season) ->
            self.divId = @divId
            self.season = @season

        setLocaleObject: (@localeObject) ->
            self.localeObject = @localeObject

        setContext: (@context) ->
            self.context = @context

        setFormattedData: (data) ->
            @data = data

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    polar: true
                    type: 'line'
                title:
                    text: ''
                xAxis:
                    categories: @categories
                    tickmarkPlacement: 'on'
                    lineWidth: 0
                    labels:
                        formatter: () ->
                            if not self.localeObject?
                                return this.value
                            if not $.isNumeric this.value
                                return LocaleFactory.selectedLocale.fieldNames[this.value].fullName
                tooltip:
                    shared: true
                    formatter: () ->
                        s = '<span style="color:black">'+LocaleFactory.selectedLocale.fieldNames[this.x].fullName+', Сезон '+(parseInt(self.season)-1)+'/'+parseInt(self.season)+'</span><br/>'
                        field = this.x
                        _.each this.points, (point, index) ->
                            value = if field is 'shots' then point.point.y*10 else point.point.y
                            s += '<span style="color:'+point.series.color+'">'+point.series.name+': <b>'+ parseFloat(value).toFixed(3)+'</b><br/>'
                        return s
                plotOptions:
                    series:
                        cursor: 'pointer'
                        point:
                            events:
                                click: () ->
                                    $('#return-control').click()
                                    $timeout () =>
                                        self.context.setField this.category, true
                                        seasonIndex = 0
                                        _.map self.context.dataBySeason.results, (element, index) ->
                                            if element.season.end_date.indexOf(self.context.lastSeason) > -1
                                                seasonIndex = index
                                            return element
                                        self.context.moveToSeason null, seasonIndex, null, true
                                        return ''
                                    , 200
                                    return ''

                series: @data


    class HighchartsClubGamesChart

        constructor: (@divId, @data) ->

        setLocaleObject: (@localeObject) ->

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    alignTicks: false
                    marginTop: 230
                title:
                    text: ''
                xAxis: [
                    {
                        labels:
                            enabled: false
                            align: 'center'
                            autoRotation: false
                        reversed: false
                        lineColor: '#FFFFFF'
                        max: 100
                    },
                    {
                        opposite: true,
                        reversed: false,
                        linkedTo: 0,
                        labels:
                            enabled: false
                        lineColor: '#FFFFFF'
                        gridZIndex: 4
                        min: -0.5
                    }
                ]
                yAxis:
                    gridLineWidth: 0
                    plotLines: [
                        color: '#141414'
                        width: 1
                        value: 0
                    ]
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
                    enabled: false
                    margin: 30
                tooltip:
                    shared: true
                    useHTML: true
                    crosshairs: true
                    borderWidth: 0
                    style:
                        padding: 0
                    shadow: false
                    positioner: (a,b,p) ->
                        return (
                            y: 50
                            x: p.plotX
                        )
                    #formatter: () ->
                    #    return '<div class="text-center"> <div class="tooltip-header"><b>' + this.key + '<b></div><a class="score">' + this.point.score + '</a><br><a class="match-date">' + (new Date(this.point.date).yyyymmddHHMMFormatted()) + '</a>'
                    formatter: () ->
                        return clubGamesFormatterDiv(this.points[0].key, this.points[0].point.score, (new Date(this.points[0].point.date).yyyymmddHHMMFormatted()),this.points[0].point.leftLogo, this.points[0].point.rightLogo )#'<div class="text-center"> <div class="tooltip-header"><b>' + this.points[0].key + '<b></div><a class="score">' + this.points[0].point.score + '</a><br><a class="match-date">' + (new Date(this.points[0].point.date).yyyymmddHHMMFormatted()) + '</a>'
                plotOptions:
                    series:
                        stacking: 'normal'
                        borderWidth: 0
                        pointWidth: 5
                        pointPlacement: "on"
                    column:
                        pointPadding: 0,
                        groupPadding: 0,
                        borderWidth: 1
                        pointWidth: 4
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
                    text: LocaleFactory.selectedLocale.fieldNames[@field].fullName.toUpperCase()
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


    class HighchartsArenaVisitorsChart

        constructor: (@divId, @data, @max) ->

        setLocaleObject: (@localeObject) ->

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    alignTicks: false
                title:
                    text: 'Посещаемость'
                xAxis:
                    labels:
                        enabled: false
                        align: 'center'
                        autoRotation: false
                    reversed: false
                    lineColor: '#FFFFFF'
                    max: 100
                yAxis:
                    gridLineWidth: 0
                    plotLines: [
                        {
                            color: '#141414'
                            width: 1
                            value: 0
                        },
                        {
                            value: @max
                            width: 1
                            color: '#141414'
                            label:
                                text: 'Вместимость'
                        }
                    ]
                    title: 'Счет'
                    allowDecimals: false
                    labels:
                        formatter: () ->
                            return Math.abs this.value
                    stackLabels:
                        formatter: () ->
                            return this
                    #max: @max
                #scrollbar:
                    #enabled: true
                legend:
                    enabled: false
                    margin: 30
                tooltip:
                    shared: true
                    useHTML: true
                    crosshairs: true
                    style:
                        padding: 0
                    #formatter: () ->
                    #    return '<div class="text-center"> <div class="tooltip-header"><b>' + this.key + '<b></div><a class="score">' + this.point.score + '</a><br><a class="match-date">' + (new Date(this.point.date).yyyymmddHHMMFormatted()) + '</a>'
                    formatter: () ->
                        return '<div class="text-center"> <div class="tooltip-header"><b>' + this.points[0].key + '<b></div><a class="score">' + this.points[0].point.spectators + '</a><br><a class="match-date">' + (new Date(this.points[0].point.date).yyyymmddHHMMFormatted()) + '</a>'
                plotOptions:
                    series:
                        stacking: 'normal'
                        borderWidth: 0
                        pointWidth: 5
                        pointPlacement: "on"
                    column:
                        pointPadding: 0,
                        groupPadding: 0,
                        borderWidth: 1
                        pointWidth: 4
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

        constructor: () ->
            @period = self.period = 365
            @field = if $location.search()['field'] then $location.search()['field'] else 'count'
            @dataType = 'graph-serial'
            self.field = @field

        init: (@divId, @data) ->

        setPeriod: (@period) ->
            self.period = @period

        setContext: (@context) ->
            self.context = @context

        setField: (@field, preventList) ->
            self.field = @field
            $('#chart-tooltip-content').html ''
            $rootScope.$broadcast 'field-changed', preventList

        getField: () ->
            @field

        setDataType: (@dataType) ->

        getDataType: () ->
            @dataType

        draw: () ->
            $('#'+@divId).highcharts
                chart:
                    type: 'column'
                    options3d:
                        enabled: true
                        alpha: 0
                        beta: 15
                        viewDistance: 25
                        depth: 100
                    marginLeft: 0
                    events:
                        drilldown: (e) ->
                            if not e.seriesOptions
                                chart = @
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
                    text: ''#@localeObject.fieldNames[@field].fullName.toUpperCase()
                xAxis:
                    "type": "datetime"
                    labels:
                        align: 'center'
                        formatter: () ->
                            if this.dateTimeLabelFormat is '%Y'
                                return (new Date(this.value).getFullYear()-1).toString().substr(2, 2) + '/' + (new Date(this.value).getFullYear()).toString().substr(2, 2)
                            else
                                return LocaleFactory.selectedLocale.monthNames[new Date(this.value).getMonth()] + ' ' + (new Date(this.value).getFullYear()).toString().substr(2, 2)
                    tickInterval: 24 * 3600 * 1000 * 30
                yAxis:
                    allowDecimals: false
                    title:
                        text: ''
                    maxPadding: 0.02
                legend:
                    margin: 30
                tooltip:
                    followPointer: true
                    crosshairs: true
                    formatter: () ->
                        header = '<b>' + LocaleFactory.selectedLocale.fieldNames[self.field].fullName.toUpperCase() + '</b>'
                        if this.points[0].point.drilldown?
                            header = LocaleFactory.selectedLocale.fieldNames[self.field].fullName.toUpperCase() + '<br> СЕЗОН ' + (new Date(this.x).getFullYear()-1) + '/'+ (new Date(this.x).getFullYear()).toString().substr(2,4);
                            $('#legend-header').html(header)
                            content = ''
                            $.each this.points, () ->
                                content += indicatorsListItem(this.y, this.series.name, this.series.options.logo, this.series.options.color) #'<div class="inline-block tooltip-block"><b>' + this.series.name + '</b>:<br>' + '<span class="tooltip-value">' + this.y  + '</span></div>'
                            $('#legend-content').html(content)
                            return false
                        else
                            s = '<div class="inline-block tooltip-block"><b>' + LocaleFactory.selectedLocale.monthNamesFull[new Date(this.x).getMonth()] + ' <br>'+ new Date(this.x).getFullYear() + '</b></div>';
                            $.each this.points, () ->
                                s += '<div class="inline-block tooltip-block"><b>' + this.series.name + '</b>:<br>' + '<span class="tooltip-value">' + this.y + '</span></div>';
                            $('#legend-content').html(s)
                            return false;
                    shared: true
                plotOptions:
                    column:
                        stacking: 'normal'
                        pointRange: 24 * 3600 * 1000 * self.period
                        states:
                            hover:
                                brightness: -0.2
                series: @data
                drilldown:
                    series: @drilldownSeries

        getChart: ()->
            @chart

    clubGamesFormatterDiv = (title, score, date, leftLogo, rightLogo) ->
        return '<div class="w-command-calendar__item w-command-calendar__item-bg">
            <div class="b-header b-header__xs">
                <h5 class="b-header__text">
                    ' + title + '
                </h5>
            </div>
            <div class="row">
                <div class="col-sm-4 col-md-12 col-lg-4">
                    <a href="#" class="ui image">
                        <img class="ui circular image" src="'+leftLogo+'">
                    </a>
                </div>

                <p class="col-sm-2 col-md-12 col-lg-4 b-score b-win-text">
                    '+score+'
                </p>

                <div class="col-sm-4 col-md-12 col-lg-4">
                    <a href="#" class="ui image">
                        <img class="ui circular image" src="'+rightLogo+'">
                    </a>
                </div>
            </div>
            <div class="w-command-calendar__info">
                <p class="date">
                    '+ date + ' МСК
                </p>
            </div>
        </div>'

    indicatorsListItem = (result, title, image, color) ->
        ###<p class="">
            нападающий
        </p>###
        return '<li class="" style="border-right: 5px solid '+color+';">
            <div class="b-inline b-diagram__legend__table-style__item">
                <div class="b-inline hidden-xs">
                    <a class="ui image" ><img class="ui image b-diagram__legend__image" src="'+image+'" width="32" height="32"></a>
                </div>

                <div class="b-inline">
                    <p class="">
                        <a href="#">'+title+'</a> <!--<i class="flag cz i-top-2 hidden-xs"></i>-->
                    </p>
                </div>
            </div>

            <p class="b-inline b-diagram__legend__table-style__games">
                '+result+'
            </p>
        </li>'


    return (
        PlayerStatsSpiderChart: HighchartsSpiderChart
        ClubGamesChart: HighchartsClubGamesChart
        ArenaVisitorsChart: HighchartsArenaVisitorsChart
        PlayerClubsChart: HighchartsPlayerClubsChart
        PlayerClubsPieChart: HighchartsPlayerClubsPieChart
        PlayerIndicatorsChart: HighchartsPlayerIndicatorsChart
    )
