angular.module('Sportomatics').factory 'IndicatorsFactory', () ->

    class PlayerIndicatorsChart

        constructor: () ->
            @field = 'count'
            @dataType = 'graph-serial'

        setField: (@field) ->

        getField: () ->
            @field

        setDataType: (@dataType) ->

        getDataType: () ->
            @dataType


    return (
        PlayerIndicatorsChart: PlayerIndicatorsChart
    )
