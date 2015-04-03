angular.module('Sportomatics').service 'MapService', ($q, $timeout) ->
  self = this
  startCoordinate1 = 55.749792
  # Moscow latitude
  startCoordinate2 = 37.632495
  # Moscow longitude
  # Variables:
  self.mapsDivName = 'clubs-map'
  @clubs_map = document.getElementById(self.mapsDivName)
  @rendered = false
  @map = null
  @geocoder = new (google.maps.Geocoder)
  @addedMarkers = []
  # Methods:

  @createClubsMap = (data, dataLabel) ->
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
    self.markers = new (L.MarkerClusterGroup)(showCoverageOnHover: false)
    switch dataLabel
      when 'clubs'
        self.markersFunctionClubs data
      when 'players'
        self.markersFunctionPlayers data
      when 'trips'
        self.markersFunctionClubGames data
    self.map.addLayer self.markers
    @rendered = true
    return

  @markersFunctionClubs = (clubs) ->
    countOfGeocoded = 0
    _.each clubs, (club, index) ->
      clubIcon = L.icon(
        iconUrl: if club.logo then 'http://dev.sportomatics.ru' + club.logo else '/static/abc.jpg'
        iconSize: [
          20
          20
        ]
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
        shadowSize: [
          34
          48
      ])
      return if !club.arena
      coords = club.arena.coords
      if `coords != null`
        coordinate1 = coords.split(',')[0]
        coordinate2 = coords.split(',')[1]
      if !club.arena.coords
        self.googleGeocode(club.arena.contacts, countOfGeocoded).then (result) ->
          self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: clubIcon).bindPopup(club.title + '<br>')
          return
        countOfGeocoded++
      if coordinate1 and coordinate2
        self.markers.addLayer new (L.marker)(new (L.LatLng)(coordinate1, coordinate2), icon: clubIcon).bindPopup(club.title + '<br>')
      return
    return

  @markersFunctionClubGames = (games) ->
    countOfGeocoded = 0
    clubs = []
    _.each games, (game, index) ->
      if game.is_guest
        club = game.home_team
        if !club.arena
          return
        if _.findWhere(clubs, 'title': club.title)
          return
        # prevent duplicate clubs
        clubs.push club
        clubIcon = L.icon(
          iconUrl: if club.logo then 'http://dev.sportomatics.ru' + club.logo else '/static/abc.jpg'
          iconSize: [
            20
            20
          ]
          shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
          shadowSize: [
            34
            48
          ])
        coords = club.arena.coords
        if `coords != null`
          coordinate1 = coords.split(',')[0]
          coordinate2 = coords.split(',')[1]
        clubDates = []
        _.each games, (game) ->
          if `game.home_team.title == club.title`
            clubDates.push new Date(game.date).yyyymmddFormatted()
          return
        clubDatesString = clubDates.join(' <br> ')
        popup = L.popup(className: 'map-popup').setContent('<div class="bold">' + club.title + '</div><br> Матчи:<br>' + clubDatesString)
        if !club.arena.coords
          self.googleGeocode(club.arena.contacts, countOfGeocoded).then (result) ->
            self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: clubIcon).bindPopup(popup)
            return
          countOfGeocoded++
        if coordinate1 and coordinate2
          self.markers.addLayer new (L.marker)(new (L.LatLng)(coordinate1, coordinate2), icon: clubIcon).bindPopup(popup)
      return
    return

  @markersFunctionPlayers = (players) ->
    countOfGeocoded = 0
    _.each players, (player, index) ->
      if !player.birth_place
        return
      playerIcon = L.icon(
        iconUrl: if player.photo then player.photo else '/static/abc.jpg'
        iconSize: [
          20
          20
        ]
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png'
        shadowSize: [
          34
          48
        ])
      self.googleGeocode(player.birth_place, countOfGeocoded).then (result) ->
        self.markers.addLayer new (L.marker)(new (L.LatLng)(result[0], result[1]), icon: playerIcon).bindPopup(player.fio + '<br> Место рождения: ' + player.birth_place)
        return
      countOfGeocoded++
      return
    return

  @isRendered = ->
    # return map rendered state
    @rendered

  @setRendered = (value) ->
    # set boolean state for map rendered variable
    return if `value != true` and `value != false`
    @rendered = value
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
        if `status == google.maps.GeocoderStatus.OK`
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

# ---
# generated by js2coffee 2.0.3