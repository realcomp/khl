angular.module('Sportomatics').service('PlayersSearchService', ($http, $timeout) ->
    @loadCountries = ($scope) ->
        url = $('#country-league-list-api').val()
        if url
            $http.get(url
            ).success((data) ->
                $scope.countries = data
                # $timeout(() ->
                #     $('.ui.dropdown.leagues').dropdown()
                # , 0)
                # if $scope.countries.length
                #     country = $scope.countries[0]
                #     if !$location.search().country
                #         # $location.search('country', String(country.pk))
                #         $scope.params = $location.search()
                #     if (country.league_set.length and
                #             !$location.search().league and
                #             $location.search().league != '')
                #         # $location.search('league', String(country.league_set[0].pk))
                #         $scope.params = $location.search()
            )
        return

    @setCountries = ($scope, countries) ->
        $scope.countriesSelected = countries
        $scope.leaguesSelected = []
        $scope.$location.search('country', countries or null)
        $scope.$location.search('league', null)
        return

    @setLeagues = ($scope, leagues) ->
        $scope.$location.search('league', leagues or null)
        return

    @getLeagues = (countries, selected) ->
        if countries and selected
            if not Array.isArray(selected)
                selected = [selected]
            selected = (+x for x in selected)
            league_sets = (country.league_set for country in countries when country.pk in selected)
            return [].concat.apply([], league_sets)  # flatten array of arrays
        return []

    @isMatchesTotalVisible = ($scope) ->
        return $scope.params.rated_by in [
            'goals_average',
            'assists_average',
            'points_average',
            'plus_minus_average']

    @setOrderBy = ($scope, order_by) ->
        if $scope.loaded
            if ($scope.params.order_by == order_by or
                    (!$scope.params.order_by and !order_by)) # same field -> reverse
                if ($scope.params.reversed == 'true')
                    $scope.$location.search('reversed', null)
                else
                    $scope.$location.search('reversed', 'true')
            else # other field -> reset
                $scope.$location.search('reversed', null)
            $scope.$location.search('order_by', order_by or null)
            @search($scope)
        return

    # @setPlaying = ($scope, is_playing) ->
    #     if $scope.loaded and $scope.params.is_playing != is_playing
    #         if is_playing == 'false'
    #             $scope.$location.search('is_playing', is_playing)
    #         else
    #             $scope.$location.search('is_playing', null)
    #         @search($scope)
    #     return

    @setRatedBy = ($scope, rated_by) ->
        if $scope.loaded and $scope.params.rated_by != rated_by
            $scope.$location.search('alphabet', null)
            $scope.$location.search('rated_by', rated_by || null)
            if rated_by # by rating -> set ordering
                $scope.$location.search('order_by', 'rating')
                $scope.$location.search('reversed', 'true')
                @search($scope)
            else # by alphabet -> reset ordering
                @setOrderBy($scope, '')
        return

    @setAlphabetFilter = ($scope, alphabet) ->
        if $scope.loaded && $scope.params.alphabet != alphabet
            $scope.$location.search('alphabet', alphabet)
            @search($scope)
        return

    @setPlayersFilter = ($scope, obj) ->
        if obj
            value = String(obj.originalObject.pk)
        else
            value = null
        if $scope.loaded and $scope.params.player != value
            $scope.$location.search('player', value)
            @search($scope)
        return

    @setClubsFilter = ($scope, obj) ->
        if obj
            value = [obj.originalObject]
        else
            value = null
        if $scope.loaded and $scope.club != value
            $scope.club = value
            @search($scope)
        return

    @search = ($scope) ->
        checkBox = ($scope, search, name, isUncheck) ->
            # checks checkbox and updates location search
            if not isUncheck
                $scope.$location.search(
                    search, $('[name="' + name + '"]').is(':checked') or null)
            else
                # checkbox is checked by default
                $scope.$location.search(
                    search, if $('[name="' + name + '"]').is(':checked') then null else 'false')
            return

        multiSelect = ($scope, search, value) ->
            # checks select and updates location search with serialized data
            if value and value.length
                $scope.$location.search(search, JSON.stringify(value))
            else
                $scope.$location.search(search, null)
            return

        url = $('#players-search-api').val()
        params = ''

        if $('#isCitizenshipRussia').is(':checked')
            $scope.$location.search('citizenship1', $('#citizenshipRussia').val())
        else
            $scope.$location.search('citizenship1', null)

        if $('#isCitizenshipOther').is(':checked')
            $scope.$location.search('citizenship_other', 'true')
            # if $scope.$location.search().citizenship2
            #     $('#citizenshipOther').val($scope.$location.search().citizenship2)
            # if $('#citizenshipOther').val()
            #     $scope.$location.search('citizenship2', $('#citizenshipOther').val())
        else
            $scope.$location.search('citizenship_other', null)

        lineAll = ($(e).val() for e in $('[name="line"]') when $(e).val())
        lineChecked = ($(e).val() for e in $('[name="line"]:checked') when $(e).val())
        lineUnchecked = (e for e in lineAll when e not in lineChecked)
        $scope.$location.search('line', (e for e in lineChecked when +e > 0) or [])
        $scope.$location.search('line', (e for e in lineUnchecked when +e < 0) or [])

        gripExAll = ($(e).val() for e in $('[name="grip_ex"]') when $(e).val())
        gripExChecked = ($(e).val() for e in $('[name="grip_ex"]:checked') when $(e).val())
        gripExUnchecked = (e for e in gripExAll when e not in gripExChecked)
        $scope.$location.search('grip_ex', gripExUnchecked)

        contractExAll = ($(e).val() for e in $('[name="contract_ex"]') when $(e).val())
        contractExChecked = ($(e).val() for e in $('[name="contract_ex"]:checked') when $(e).val())
        contractExUnchecked = (e for e in contractExAll when e not in contractExChecked)
        $scope.$location.search('contract_ex', contractExUnchecked)

        contract_types = ($(e).val() for e in $('[name="contract_types"]:checked') when $(e).val())
        $scope.$location.search('contract_types', contract_types or [])

        # if !$scope.leaguesLoaded
        #     $scope.leaguesLoaded = true
        #     if $scope.params.league
        #         if Array.isArray($scope.params.league)
        #             $scope.leaguesSelected = $scope.params.league
        #         else
        #             $scope.leaguesSelected = [$scope.params.league]
        # $scope.$location.search('league', $scope.leaguesSelected)

        checkBox($scope, 'contract_type__isnull', 'contractTypeNull')
        checkBox($scope, 'citizenship_reversed', 'citizenshipReversed')
        checkBox($scope, 'season_enabled', 'seasonEnabled')
        checkBox($scope, 'club_enabled', 'clubEnabled')
        checkBox($scope, 'league_enabled', 'league2Enabled')
        checkBox($scope, 'related_enabled', 'relatedEnabled')
        checkBox($scope, 'is_playing', 'is_playing', true)

        multiSelect($scope, 'citizenship', $scope.citizenship)
        multiSelect($scope, 'club', $scope.club)
        multiSelect($scope, 'league2', $scope.league2)
        multiSelect($scope, 'related_player', $scope.relatedPlayer)

        if $scope.number
            $scope.$location.search('number', $scope.number)

        if $('[name="age"]').length
            age = $('[name="age"]').val().split(';')
            $scope.$location.search('age__lte', age[0])
            $scope.$location.search('age__gte', age[1])

        if $('[name="relatedValue"]').length
            relatedValue = $('[name="relatedValue"]').val().split(';')
            $scope.$location.search('related_value__gte', relatedValue[0])
            $scope.$location.search('related_value__lte', relatedValue[1])

        $scope.params = $scope.$location.search()

        params += ((k + '=' + $scope.params[k]) for k in [
            'player', 'season', 'number', 'contract_type', 'fio',
            'height', 'height__gte', 'height__lte',
            'weight', 'weight__gte', 'weight__lte',
            'grip', 'match_count', 'rated_by',
            'age__lte', 'age__gte', 'gamingtime',
            'related_value__lte', 'related_value__gte',
        ] when $scope.params[k]).join('&')

        params += '&order_by=' + ($scope.params.order_by or '%s_lastname,%s_name')

        if $scope.params.reversed
            params += '&reversed=true'
        if lineChecked.length
            params += (('&line=' + Math.abs(+x)) for x in lineChecked).join('')
        if gripExChecked.length
            params += (('&grip=' + x) for x in gripExChecked).join('')
        if contractExChecked.length
            params += (('&contract_types=' + if x == '*' then '' else x) for x in contractExChecked).join('')
        if $scope.params.contract_types
            params += (('&contract_types=' + x) for x in $scope.params.contract_types).join('')
        if $scope.params.citizenship1
            params += '&citizenship=' + $scope.params.citizenship1
        if $scope.params.citizenship_other == 'true'
            if $scope.params.citizenship2
                params += '&citizenship=' + $scope.params.citizenship2
            else
                params += '&citizenship_other=true'
        # if $scope.params.is_playing != 'false'
        if $scope.params.is_playing == 'false'
            params += '&is_playing=false'
        if $scope.params.alphabet
            params += '&%s_lastname__startswith=' + $scope.params.alphabet
        if ($scope.club_enabled or $scope.params.club_enabled) and $scope.params.club
            params += (('&club=' + x['pk']) for x in JSON.parse($scope.params.club)).join('')
        # if $scope.params.league
        #     params += '&league=' + $scope.params.league
        if $scope.params.league
            params += (('&league=' + league) for league in $scope.params.league).join('')
        if $scope.params.contract_to
            d = $scope.params.contract_to.split('/')
            params += '&contract_to=' + d[2] + '-' + d[0] + '-' + d[1]
        if $scope.params.contract_type__isnull
            params += '&contract_type__isnull=true'
        if $scope.params.citizenship_reversed
            params += '&citizenship_reversed=true'
        if $scope.params.citizenship
            params += (('&citizenship=' + x['pk']) for x in JSON.parse($scope.params.citizenship)).join('')
        if $scope.params.league_enabled and $scope.params.league2
            params += (('&league=' + x['pk']) for x in JSON.parse($scope.params.league2)).join('')
        if $scope.params.season_enabled
            if $scope.params.season_start and $scope.params.season_end
                params += (
                    '&season_start=' + $scope.params.season_start +
                    '&season_end=' + $scope.params.season_end)
        if $scope.params.related_enabled and $scope.params.related_player and $scope.params.related_field
            params += (('&related_player=' + x['pk']) for x in JSON.parse($scope.params.related_player)).join('')
            params += '&related_field=' + $scope.params.related_field

        $scope.data = {}
        $scope.loaded = false
        $http.get(url + '?' + params
        ).success((data) ->
            $scope.data = data
            $scope.loaded = true
        )
        return

    @next = ($scope, isAll) ->
        url = $scope.data.next
        if isAll
            url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count)
        $scope.loaded = false
        $http.get(url
        ).success((data) ->
            if isAll
                $scope.data = data
            else
                $scope.data.next = data.next
                $scope.data.results = $scope.data.results.concat(data.results)
            $scope.loaded = true
        )
        return

    return
)
