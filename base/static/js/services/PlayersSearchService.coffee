angular.module('Sportomatics').service('PlayersSearchService', ($http) ->
    @loadCountries = ($scope, $location, callback) ->
        url = $('#LeagueListLink').attr('href')
        if url
            $http.get(url
            ).success((data) ->
                $scope.countries = data
                if $scope.countries.length
                    country = $scope.countries[0]
                    if !$location.search().country
                        # $location.search('country', String(country.pk))
                        $scope.params = $location.search()
                    if (country.league_set.length and
                            !$location.search().league and
                            $location.search().league != '')
                        # $location.search('league', String(country.league_set[0].pk))
                        $scope.params = $location.search()
                if callback and typeof callback == 'function'
                    callback($scope)
            )
        else if callback and typeof callback == 'function'
            callback($scope)
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
        if !$scope.loader
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

    @setPlaying = ($scope, is_playing) ->
        if !$scope.loader and $scope.params.is_playing != is_playing
            if is_playing == 'false'
                $scope.$location.search('is_playing', is_playing)
            else
                $scope.$location.search('is_playing', null)
            @search($scope)
        return

    @setRatedBy = ($scope, rated_by) ->
        if !$scope.loader and $scope.params.rated_by != rated_by
            $scope.$location.search('alphabet', null)
            $scope.$location.search('rated_by', rated_by || null)
            if rated_by # by rating -> set ordering
                $scope.$location.search('order_by', 'rating')
                $scope.$location.search('reversed', 'true')
                this.search($scope)
            else # by alphabet -> reset ordering
                this.setOrderBy($scope, '')
        return

    @setAlphabetFilter = ($scope, alphabet) ->
        if !$scope.loader && $scope.params.alphabet != alphabet
            $scope.$location.search('alphabet', alphabet)
            this.search($scope)
        return

    @setPlayersFilter = ($scope, obj) ->
        if obj
            value = String(obj.originalObject.pk)
        else
            value = null
        if !$scope.loader and $scope.params.player != value
            $scope.$location.search('player', value)
            this.search($scope)
        return

    @setClubsFilter = ($scope, obj) ->
        if obj
            value = String(obj.originalObject.pk)
        else
            value = null
        if !$scope.loader and $scope.params.club != value
            $scope.$location.search('club', value)
            this.search($scope)
        return

    @search = ($scope) ->
        url = $('#PlayersSearchLink').attr('href')
        params = ''

        if $('#isCitizenshipRussia').is(':checked')
            $scope.$location.search('citizenship1', $('#citizenshipRussia').val())
        else
            $scope.$location.search('citizenship1', null)
        if $('#isCitizenshipOther').is(':checked')
            $scope.$location.search('citizenship_other', 'true')
            if $scope.$location.search().citizenship2
                $('#citizenshipOther').val($scope.$location.search().citizenship2)
            if $('#citizenshipOther').val()
                $scope.$location.search('citizenship2', $('#citizenshipOther').val())
        else
            $scope.$location.search('citizenship_other', null)

        line = ($(e).val() for e in $('[name="line"]:checked') when $(e).val())
        $scope.$location.search('line', line or [])

        # if !$scope.leaguesLoaded
        #     $scope.leaguesLoaded = true
        #     if $scope.params.league
        #         if Array.isArray($scope.params.league)
        #             $scope.leaguesSelected = $scope.params.league
        #         else
        #             $scope.leaguesSelected = [$scope.params.league]
        # $scope.$location.search('league', $scope.leaguesSelected)

        $scope.$location.search(
            'contract_type__isnull',
            $('[name="contractTypeNull"]').is(':checked') or null)

        $scope.$location.search(
            'citizenship_reversed',
            $('[name="citizenshipReversed"]').is(':checked') or null)

        if $scope.citizenship
            $scope.$location.search('citizenship', (x['pk'] for x in $scope.citizenship))
        else
            $scope.$location.search('citizenship', null)

        if $scope.number
            $scope.$location.search('number', $scope.number)
        # if $scope.height
        #     $scope.$location.search('height', $scope.height)
        # if $scope.weight
        #     $scope.$location.search('weight', $scope.weight)

        age = $('[name="age"]').val().split(';')
        $scope.$location.search('age__lte', age[0])
        $scope.$location.search('age__gte', age[1])

        $scope.params = $scope.$location.search()

        params += 'order_by=' + ($scope.params.order_by or '%s_lastname,%s_name')
        if $scope.params.reversed
            params += '&reversed=true'
        if $scope.params.line.length
            params += '&line=' + $scope.params.line.join('&line=')
        if $scope.params.citizenship1
            params += '&citizenship=' + $scope.params.citizenship1
        if $scope.params.citizenship2
            params += '&citizenship=' + $scope.params.citizenship2
        if $scope.params.citizenship_other == 'true'
            params += '&citizenship_other=true'
        if $scope.params.rated_by
            params += '&rated_by=' + $scope.params.rated_by
        if $scope.params.is_playing != 'false'
            params += '&is_playing=true'
        if $scope.params.alphabet
            params += '&%s_lastname__startswith=' + $scope.params.alphabet
        if $scope.params.club
            params += '&club=' + $scope.params.club
        if $scope.params.player
            params += '&player=' + $scope.params.player
        if $scope.params.season
            params += '&season=' + $scope.params.season
        if $scope.params.league
            params += (('&league=' + league) for league in $scope.params.league).join('')
        if $scope.params.number
            params += '&number=' + $scope.params.number
        if $scope.params.contract_type
            params += '&contract_type=' + $scope.params.contract_type
        if $scope.params.contract_to
            d = $scope.params.contract_to.split('/')
            params += '&contract_to=' + d[2] + '-' + d[0] + '-' + d[1]
        if $scope.params.height
            params += '&height=' + $scope.params.height
        if $scope.params.weight
            params += '&weight=' + $scope.params.weight
        if $scope.params.grip
            params += '&grip=' + $scope.params.grip
        if $scope.params.contract_type__isnull
            params += '&contract_type__isnull=true'
        if $scope.params.age__lte
            params += '&age__lte=' + $scope.params.age__lte
        if $scope.params.age__gte
            params += '&age__gte=' + $scope.params.age__gte
        if $scope.params.citizenship_reversed
            params += '&citizenship_reversed=true'
        if $scope.params.citizenship
            params += (('&citizenship=' + x['pk']) for x in $scope.citizenship).join('')

        $scope.data = {}
        $scope.loader = true
        $http.get(url + '?' + params
        ).success((data) ->
            $scope.data = data
            $scope.loader = false
        )
        return

    @next = ($scope, isAll) ->
        url = $scope.data.next
        if isAll
            url = url.replace(/&page=\d+$/, '&paginate_by=' + $scope.data.count)
        $scope.loader = true
        $http.get(url
        ).success((data) ->
            if isAll
                $scope.data = data
            else
                $scope.data.next = data.next
                $scope.data.results = $scope.data.results.concat(data.results)
            $scope.loader = false
        )
        return

    return
)
