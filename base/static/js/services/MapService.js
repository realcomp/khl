angular.module('Sportomatics').service('MapService', function($q, $timeout) {
  var self, startCoordinate1, startCoordinate2;
  self = this;
  startCoordinate1 = 55.749792;
  startCoordinate2 = 37.632495;
  this.mapsDivName = 'clubs-map';
  this.clubs_map = document.getElementById(self.mapsDivName);
  this.rendered = false;
  this.map = null;
  this.geocoder = new google.maps.Geocoder;
  this.addedMarkers = [];
  this.createClubsMap = function(data, dataLabel) {
    var ggl, osm;
    self.map = L.map(self.mapsDivName, {
      scrollWheelZoom: false
    }).setView([startCoordinate1, startCoordinate2], 4);
    osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
    ggl = new L.Google('ROADMAP');
    self.map.addLayer(ggl);
    self.map.addControl(new L.Control.Layers({
      'Google': ggl,
      'OpenStreetMap': osm
    }, {}));
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false
    });
    switch (dataLabel) {
      case 'clubs':
        self.markersFunctionClubs(data);
        break;
      case 'players':
        self.markersFunctionPlayers(data);
        break;
      case 'trips':
        self.markersFunctionClubGames(data);
    }
    self.map.addLayer(self.markers);
    this.rendered = true;
  };
  this.markersFunctionClubs = function(clubs) {
    var countOfGeocoded;
    countOfGeocoded = 0;
    _.each(clubs, function(club, index) {
      var clubIcon, coordinate1, coordinate2, coords;
      clubIcon = L.icon({
        iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
        iconSize: [20, 20],
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
        shadowSize: [34, 48]
      });
      if (!club.arena) {
        return;
      }
      coords = club.arena.coords;
      if (coords !== null) {
        coordinate1 = coords.split(',')[0];
        coordinate2 = coords.split(',')[1];
      }
      if (!club.arena.coords) {
        self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result) {
          self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
            icon: clubIcon
          }).bindPopup(club.title + '<br>'));
        });
        countOfGeocoded++;
      }
      if (coordinate1 && coordinate2) {
        self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {
          icon: clubIcon
        }).bindPopup(club.title + '<br>'));
      }
    });
  };
  this.markersFunctionClubGames = function(games) {
    var clubs, countOfGeocoded;
    countOfGeocoded = 0;
    clubs = [];
    _.each(games, function(game, index) {
      var club, clubDates, clubDatesString, clubIcon, coordinate1, coordinate2, coords, popup;
      if (game.is_guest) {
        club = game.home_team;
        if (!club.arena || _.findWhere(clubs, {
          'title': club.title
        })) {
          return;
        }
        clubs.push(club);
        clubIcon = L.icon({
          iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
          iconSize: [20, 20],
          shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
          shadowSize: [34, 48]
        });
        coords = club.arena.coords;
        if (coords !== null) {
          coordinate1 = coords.split(',')[0];
          coordinate2 = coords.split(',')[1];
        }
        clubDates = [];
        _.each(games, function(game) {
          if (game.home_team.title === club.title) {
            clubDates.push(new Date(game.date).yyyymmddFormatted());
          }
        });
        clubDatesString = clubDates.join(' <br> ');
        popup = L.popup({
          className: 'map-popup'
        }).setContent('<div class="bold">' + club.title + '</div><br> Матчи:<br>' + clubDatesString);
        if (!club.arena.coords) {
          self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result) {
            self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
              icon: clubIcon
            }).bindPopup(popup));
          });
          countOfGeocoded++;
        }
        if (coordinate1 && coordinate2) {
          self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {
            icon: clubIcon
          }).bindPopup(popup));
        }
      }
    });
  };
  this.markersFunctionPlayers = function(players) {
    var countOfGeocoded;
    countOfGeocoded = 0;
    _.each(players, function(player, index) {
      var playerIcon;
      if (!player.birth_place) {
        return;
      }
      playerIcon = L.icon({
        iconUrl: player.photo ? player.photo : '/static/abc.jpg',
        iconSize: [20, 20],
        shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
        shadowSize: [34, 48]
      });
      self.googleGeocode(player.birth_place, countOfGeocoded).then(function(result) {
        self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
          icon: playerIcon
        }).bindPopup(player.fio + '<br> Место рождения: ' + player.birth_place));
      });
      countOfGeocoded++;
    });
  };
  this.isRendered = function() {
    return this.rendered;
  };
  this.setRendered = function(value) {
    if (value !== true && value !== false) {
      return;
    }
    this.rendered = value;
  };
  this.remove = function() {
    $('#' + self.mapsDivName).remove();
    $('#' + self.mapsDivName + '-container').append('<div id="' + self.mapsDivName + '"></div>');
  };
  this.googleGeocode = function(address, delay) {
    var deferred;
    deferred = $q.defer();
    address = address.substr(address.indexOf(' ') + 1).replace('ул.', '').replace('д.', '').replace('Московская обл.,', '');
    if (address.indexOf('Телефон') > -1) {
      address = address.substring(0, address.indexOf('Телефон'));
    }
    $timeout((function() {
      self.geocoder.geocode({
        'address': address
      }, function(results, status) {
        var coordinate1, coordinate2;
        if (status === google.maps.GeocoderStatus.OK) {
          coordinate1 = results[0].geometry.location.B;
          coordinate2 = results[0].geometry.location.k;
          deferred.resolve([coordinate2, coordinate1]);
        } else {
          deferred.reject();
          console.log(address, 'Geocode was not successful for the following reason: ' + status);
        }
      });
    }), 400 * delay);
    return deferred.promise;
  };
});
