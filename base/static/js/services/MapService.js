var indexOf = [].indexOf || function(item) { for (var i = 0, l = this.length; i < l; i++) { if (i in this && this[i] === item) return i; } return -1; };

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
    var deferred, ggl, osm;
    deferred = $q.defer();
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
      showCoverageOnHover: false,
      zoomToBoundsOnClick: false,
      animateAddingMarkers: true,
      maxClusterRadius: 120
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
        break;
      case 'fans':
        self.markersFunctionFans(data);
    }
    self.map.addLayer(self.markers);
    this.rendered = true;
    deferred.resolve(true);
    return deferred.promise;
  };
  this.cityClickFunction = function(event) {
    self.context.selectedPlace = event.target.options.title.split('_')[0].toUpperCase();
    $timeout(function() {}, 100);
  };
  this.clusterClickClubs = function(a) {
    var cluster;
    self.a = a;
    cluster = a.layer.getAllChildMarkers();
    if (self.map.getZoom() === self.map.getMaxZoom()) {
      return;
    }
    self.popup = L.popup().setLatLng(a.layer._latlng).setContent('<div class="text-center">' + cluster[0].options.title + ' и еще ' + (cluster.length - 1) + ' клубов <br> <a class="link pointer" id="show-all">показать все</a></div>').openOn(self.map);
    document.getElementById('show-all').onclick = function() {
      return self.moveToClusterBounds(self.a);
    };
  };
  this.moveToClusterBounds = function(cluster) {
    cluster.layer.zoomToBounds();
    self.map.closePopup(self.popup);
    if (self.map.getZoom() === self.map.getMaxZoom()) {
      self.map.zoomOut(2);
    }
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
            icon: clubIcon,
            title: club.title
          }).bindPopup(club.title + '<br>'));
        });
        countOfGeocoded++;
      }
      if (coordinate1 && coordinate2) {
        self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {
          icon: clubIcon,
          title: club.title
        }).bindPopup(club.title + '<br>'));
      }
    });
    self.markers.on('clusterclick', this.clusterClickClubs);
  };
  this.markersFunctionClubGames = function(games) {
    var clubs, countOfGeocoded;
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false
    });
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
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false
    });
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
  this.markersFunctionFans = function(fans) {
    var countOfGeocoded, locations;
    countOfGeocoded = 0;
    locations = [];
    self.markers = new L.MarkerClusterGroup({
      showCoverageOnHover: false,
      iconCreateFunction: function(cluster) {
        var c, markers, sum;
        sum = 0;
        c = ' marker-cluster-';
        markers = cluster.getAllChildMarkers();
        _.each(markers, function(marker) {
          if (marker.options.title.length !== 0) {
            sum += Number(marker.options.title.split('_')[1]);
          }
          c = ' marker-cluster-';
          if ((-1 < sum && sum < 10)) {
            c += 'small';
          } else {
            c += 'large';
          }
        });
        return new L.DivIcon({
          html: '<div><span>' + sum + '</span></div>',
          className: 'marker-cluster' + c,
          iconSize: new L.Point(40, 40)
        });
      }
    });
    _.each(fans, function(fan, index) {
      var ref;
      if ((ref = fan.location, indexOf.call(locations.map(function(l) {
        return l.name;
      }), ref) < 0)) {
        locations.push({
          name: fan.location,
          count: 1
        });
      } else {
        locations.map(function(location) {
          if (location.name === fan.location) {
            location.count = location.count + 1;
          }
          return location;
        });
      }
    });
    _.each(locations, function(location, index) {
      self.googleGeocode(location.name, countOfGeocoded).then(function(result) {
        var c, playerIcon, ref;
        c = ' marker-cluster-';
        if ((0 < (ref = location.count) && ref < 10)) {
          c += 'small';
        } else {
          c += 'large';
        }
        playerIcon = new L.DivIcon({
          html: '<div><span>' + location.count + '</span></div>',
          className: 'marker-cluster' + c,
          iconSize: new L.Point(40, 40)
        });
        self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {
          icon: playerIcon,
          title: location.name + '_' + location.count
        }).on('click', self.cityClickFunction));
      });
      return countOfGeocoded++;
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
  this.setContext = function(context) {
    this.context = context;
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
