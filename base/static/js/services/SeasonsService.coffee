angular.module('Sportomatics').service('SeasonsService', () ->
    @isSeasonActive = (season, pk, isFirst) ->
        if season
            return +season == +pk
        else
            return isFirst

    @getSeason = (season) ->
        # get season title by id
        if season
            e = $('.menu.seasons .item[data-value="' + season + '"]')
        else
            es = $('.menu.seasons .item')
            if es
                e = $(es[0])
        if e
            return e.text().trim()

    return
)
