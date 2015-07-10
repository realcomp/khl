angular.module('Sportomatics').service 'MapService', ($q, $timeout) ->
    self = this
    # Moscow latitude
    startCoordinate1 = 55.749792
    # Moscow longitude
    startCoordinate2 = 37.632495

    # Variables:

    @mapsDivName = 'clubs-map'
    @clubs_map = document.getElementById(self.mapsDivName)
    @rendered = false
    @map = null
    @geocoder = new (google.maps.Geocoder)
    @addedMarkers = []

    # Methods:

    @createClubsMap = (data, dataLabel) ->
        deferred = $q.defer()
        # creates clubs map inside maps-div marked as mapsDivName
        self.map = L.map(self.mapsDivName, scrollWheelZoom: false).setView([
            startCoordinate1
            startCoordinate2
        ], 4)
        osm = new (L.TileLayer)('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png')
        ggl = new (L.Google)('ROADMAP')
        self.map.addLayer ggl
        self.map.addControl new (L.Control.Layers)({
            'Google': ggl
            'OpenStreetMap': osm
        }, {})
        self.markers = new (L.MarkerClusterGroup)(showCoverageOnHover: false, zoomToBoundsOnClick: false, animateAddingMarkers: true, maxClusterRadius: 120)
        switch dataLabel
            when 'clubs'
                self.markersFunctionClubs data
            when 'players'
                self.markersFunctionPlayers data
            when 'trips'
                self.markersFunctionClubGames data
            when 'fans'
                self.markersFunctionFans data
        self.map.addLayer self.markers
        @rendered = true
        deferred.resolve true
        return deferred.promise

    @cityClickFunction = (event) ->
        self.context.selectedPlace = event.target.options.title.split('_')[0].toUpperCase();
        $timeout ->
            return
        , 100
        return

    @clusterClickClubs = (a) ->
        self.a = a;
        cluster = a.layer.getAllChildMarkers()
        return if self.map.getZoom() is self.map.getMaxZoom()
        self.popup = L.popup()
        .setLatLng(a.layer._latlng)
        .setContent('<div class="text-center">'+ cluster[0].options.title + ' и еще '+ (cluster.length-1) + ' клубов <br> <a class="link pointer" id="show-all">показать все</a></div>')
        .openOn self.map
        document.getElementById('show-all').onclick = () ->
            self.moveToClusterBounds(self.a)
        return

    @moveToClusterBounds = (cluster) ->
        cluster.layer.zoomToBounds()
        self.map.closePopup self.popup
        self.map.zoomOut 2 if self.map.getZoom() is self.map.getMaxZoom()
        return

    @markersFunctionClubs = (clubs) ->
        countOfGeocoded = 0
        _.each clubs, (club, index) ->
            clubIcon = L.icon(
                iconUrl: if club.logo then 'http://dev.sportomatics.ru' + club.logo else '/static/abc.jpg'
                iconSize: [ 20, 20 ]
                shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
                shadowSize: [ 34, 48]
            )
            return if !club.arena
            coords = club.arena.coords
            if coords != null
                coordinate1 = coords.split(',')[0]
                coordinate2 = coords.split(',')[1]
            if !club.arena.coords
                self.googleGeocode(club.arena.contacts, countOfGeocoded).then (result) ->
                    self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: clubIcon, title: club.title).bindPopup(club.title + '<br>')
                    return
                countOfGeocoded++
            if coordinate1 and coordinate2
                self.markers.addLayer new (L.marker)(new (L.LatLng)(coordinate1, coordinate2), icon: clubIcon, title: club.title).bindPopup(club.title + '<br>')
            return

        self.markers.on 'clusterclick',  @clusterClickClubs
        return

    @markersFunctionClubGames = (games) ->
        self.markers = new (L.MarkerClusterGroup)(showCoverageOnHover: false)
        countOfGeocoded = 0
        clubs = []
        _.each games, (game, index) ->
            if game.is_guest
                club = game.home_team
                return if !club.arena or _.findWhere(clubs, 'title': club.title)
                # prevent duplicate clubs
                clubs.push club
                clubIcon = L.icon(
                    iconUrl: if club.logo then 'http://dev.sportomatics.ru' + club.logo else '/static/abc.jpg'
                    iconSize: [ 20, 20 ]
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
                    shadowSize: [ 34, 48]
                )
                coords = club.arena.coords
                if coords != null
                    coordinate1 = coords.split(',')[0]
                    coordinate2 = coords.split(',')[1]
                clubDates = []
                _.each games, (game) ->
                    if game.home_team.title is club.title
                        clubDates.push new Date(game.date).yyyymmddFormatted()
                    return
                clubDatesString = clubDates.join(' <br> ')
                popup = L.popup(className: 'map-popup').setContent('<div class="bold">' + club.title + '</div><br> Матчи:<br>' + clubDatesString)
                if !club.arena.coords
                    self.googleGeocode(club.arena.contacts, countOfGeocoded).then (result) ->
                        self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: clubIcon).bindPopup popup
                        return
                    countOfGeocoded++
                if coordinate1 and coordinate2
                    self.markers.addLayer new (L.marker)(new (L.LatLng)(coordinate1, coordinate2), icon: clubIcon).bindPopup popup
            return
        return

    @markersFunctionPlayers = (players) ->
        self.markers = new (L.MarkerClusterGroup)(showCoverageOnHover: false)
        countOfGeocoded = 0
        _.each players, (player, index) ->
            return if !player.birth_place
            playerIcon = L.icon(
                iconUrl: if player.photo then player.photo else '/static/abc.jpg'
                iconSize: [ 20, 20 ]
                shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
                shadowSize: [ 34, 48 ]
            )
            self.googleGeocode(player.birth_place, countOfGeocoded).then (result) ->
                self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: playerIcon).bindPopup(player.fio + '<br> Место рождения: ' + player.birth_place)
                return
            countOfGeocoded++
            return
        return

    @markersFunctionFans = (fans) ->
        countOfGeocoded = 0;
        locations = [];
        self.markers = new (L.MarkerClusterGroup)(
            showCoverageOnHover: false
            iconCreateFunction: (cluster) ->
                sum = 0
                c = ' marker-cluster-';
                markers = cluster.getAllChildMarkers();
                _.each markers, (marker) ->
                    sum += Number(marker.options.title.split('_')[1]) if marker.options.title.length isnt 0
                    c = ' marker-cluster-';
                    if -1 < sum < 10 then c+='small' else c+='large'
                    return
                return new L.DivIcon({ html: '<div><span>' + sum + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
        )
        _.each fans, (fan, index) ->
            if(fan.location not in locations.map (l) -> l.name)
            then locations.push (name: fan.location, count: 1)
            else locations.map (location) ->
                if location.name is fan.location then location.count = location.count+1
                return location
            return

        _.each locations, (location, index) ->
            self.googleGeocode(location.name, countOfGeocoded).then (result) ->
                c = ' marker-cluster-';
                if 0 < location.count < 10 then c+='small' else c+='large'
                playerIcon = new L.DivIcon({ html: '<div><span>' + location.count + '</span></div>', className: 'marker-cluster' + c, iconSize: new L.Point(40, 40) });
                self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: playerIcon, title: location.name+'_'+location.count ).on('click', self.cityClickFunction)#.bindLabel(String(location.count), {noHide: true}).bindPopup(location.name + '<br>' + location.count)
                return
            countOfGeocoded++
        return

    @isRendered = ->
        # return map rendered state
        @rendered

    @setRendered = (value) ->
        # set boolean state for map rendered variable
        return if value != true and value != false
        @rendered = value
        return

    @setContext = (context) ->
        @context = context;
        return

    @remove = ->
        $('#' + self.mapsDivName).remove()
        $('#' + self.mapsDivName + '-container').append '<div id="' + self.mapsDivName + '"></div>'
        return

    @googleGeocode = (address, delay) ->
        deferred = $q.defer()
        address = address.substr(address.indexOf(' ') + 1).replace('ул.', '').replace('д.', '').replace('Московская обл.,', '')
        if address.indexOf('Телефон') > -1
            address = address.substring(0, address.indexOf('Телефон'))
        $timeout (->
            self.geocoder.geocode { 'address': address }, (results, status) ->
                if status is google.maps.GeocoderStatus.OK
                    coordinate1 = results[0].geometry.location.B
                    coordinate2 = results[0].geometry.location.k
                    deferred.resolve [
                        coordinate2
                        coordinate1
                    ]
                else
                    deferred.reject()
                    console.log address, 'Geocode was not successful for the following reason: ' + status
                return
            return
        ), 400 * delay
        deferred.promise

    return
