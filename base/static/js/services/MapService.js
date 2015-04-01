angular.module('Sportomatics').service('MapService', function($q, $timeout){
        var self = this;
        var startCoordinate1 = 55.749792; // Moscow latitude
        var startCoordinate2 = 37.632495; // Moscow longitude

        // Variables:

        self.mapsDivName = 'clubs-map';
        this.clubs_map = document.getElementById(self.mapsDivName);
        this.rendered = false;
        this.map = null;
        this.geocoder = new google.maps.Geocoder();
        this.addedMarkers = [];

        // Methods:

        this.createClubsMap = function(data, dataLabel){ // creates clubs map inside maps-div marked as mapsDivName
            self.map = L.map(self.mapsDivName, {
                scrollWheelZoom: false
            }).setView([startCoordinate1, startCoordinate2], 4);
            var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
            var ggl = new L.Google('ROADMAP');
            self.map.addLayer(ggl);
            self.map.addControl(new L.Control.Layers( {'Google':ggl, 'OpenStreetMap': osm}, {}));
            self.markers = new L.MarkerClusterGroup({ showCoverageOnHover: false });
            dataLabel === 'clubs' ? self.markersFunctionClubs(data) : self.markersFunctionPlayers(data);
            self.map.addLayer(self.markers);
            this.rendered = true;
        };

        this.markersFunctionClubs = function(clubs){
            var countOfGeocoded = 0;
            _.each(clubs, function(club, index){
                var clubIcon = L.icon({
                    iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
                    iconSize: [20, 20],
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48]
                });
                if(!club.arena) return;
                var coords = club.arena.coords;
                if(coords != null){
                    var coordinate1 = coords.split(',')[0];
                    var coordinate2 = coords.split(',')[1];
                }
                if(!club.arena.coords){
                    self.googleGeocode(club.arena.contacts, countOfGeocoded).then(function(result){
                       self.markers.addLayer(new L.marker(new L.LatLng(result[0], result[1]), {icon: clubIcon}).bindPopup(club.title + '<br>'));
                    });
                    countOfGeocoded++;
                }
                if(coordinate1 && coordinate2){
                    self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {icon: clubIcon}).bindPopup(club.title + '<br>'));
                }
            });
        };

        this.markersFunctionClubGames = function(){

        };

        this.markersFunctionPlayers = function(players){
            _.each(players, function(player, index){
                var playerIcon = L.icon({
                    iconUrl: player.photo.file ? 'http://dev.sportomatics.ru' + player.photo.file : '/static/abc.jpg',
                    iconSize: [20, 20],
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48]
                });
                if(!player.birth_place) return;
                var coords = player.birth_place.coords;
                if(coords != null){
                    var coordinate1 = coords.split(',')[0];
                    var coordinate2 = coords.split(',')[1];
                }
                if(coordinate1 && coordinate2){
                    self.markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {icon: playerIcon}).bindPopup(player.fio + '<br>'));
                }
            });
        };

        this.isRendered = function(){ // return map rendered state
            return this.rendered;
        };

        this.setRendered = function(value){ // set boolean state for map rendered variable
            if(value !== true && value !== false) return;
            this.rendered = value;
        };

        this.remove = function(){
            $('#'+self.mapsDivName).remove();
            $('#'+self.mapsDivName + '-container').append('<div id="' + self.mapsDivName + '"></div>');
        };

        this.googleGeocode = function(address, delay){
            var deferred = $q.defer();
            address = address.substr(address.indexOf(" ") + 1).replace('ул.', "").replace('д.', '').replace('Московская обл.,', '')
            if(address.indexOf('Телефон') > -1) address = address.substring(0, address.indexOf('Телефон'));
            $timeout(function(){
                self.geocoder.geocode({'address': address}, function(results, status) {
                    if (status == google.maps.GeocoderStatus.OK) {
                        var coordinate1 = results[0].geometry.location.B;
                        var coordinate2 = results[0].geometry.location.k;
                        deferred.resolve([coordinate2, coordinate1]);
                    } else {
                        deferred.reject();
                        console.log(address, 'Geocode was not successful for the following reason: ' + status);
                    }
                });
            }, 400 * delay);

            return deferred.promise;
        }
});