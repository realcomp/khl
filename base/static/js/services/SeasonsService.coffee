angular.module('Sportomatics').service('SeasonsService', () ->
    @isSeasonActive = (season, pk, isFirst) ->
        if season
            return +season == +pk
        else
            return isFirst

    @getDefaultSeason = () ->
        es = $('.menu.seasons .item')
        if es
            e = $(es[0])
            if e
                return e.attr('data-value')

    @getSeasonTitle = (season) ->
        # get season title by id
        pk = season
        if not pk
            pk = @getDefaultSeason()
        e = $('.menu.seasons .item[data-value="' + pk + '"]')
        if e
            return e.text().trim()

    return
)
