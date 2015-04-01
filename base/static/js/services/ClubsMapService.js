angular.module('Sportomatics').service('ClubsMapService', function(){
        var self = this;
        var startCoordinate1 = 55.749792; // Moscow latitude
        var startCoordinate2 = 37.632495; // Moscow longitude

        // Variables:
        self.mapsDivName = 'clubs-map';
        this.clubs_map = document.getElementById(self.mapsDivName);
        this.rendered = false;
        self.map = null;

        // Methods:
        this.createClubsMap = function(clubs){ // creates clubs map inside maps-div marked as mapsDivName
            self.map = L.map(self.mapsDivName).setView([startCoordinate1, startCoordinate2], 4);
            var osm = new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png');
            var ggl = new L.Google('ROADMAP');
            self.map.addLayer(ggl);
            self.map.addControl(new L.Control.Layers( {'Google':ggl, 'OpenStreetMap': osm}, {}));
            var markers = new L.MarkerClusterGroup({ showCoverageOnHover: false });

            _.each(clubs, function(club, index){
                if(club.arena)
                var coords = club.arena.coords;
                if(coords != null){
                    var coordinate1 = coords.split(',')[0];
                    var coordinate2 = coords.split(',')[1];
                }
                var clubIcon = L.icon({
                    iconUrl: club.logo ? 'http://dev.sportomatics.ru' + club.logo : '/static/abc.jpg',
                    iconSize: [20, 20],
                    shadowUrl: '/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48]
                });
                if(coordinate1 && coordinate2){
                    markers.addLayer(new L.marker(new L.LatLng(coordinate1, coordinate2), {icon: clubIcon}).bindPopup(club.title + '<br>'));
                }
            });
            self.map.addLayer(markers);
            this.rendered = true;
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
});