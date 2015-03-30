angular.module('Sportomatics').service('ClubsMapService', function(){
        var startCoordinate1 = 55.749792; // Moscow latitude
        var startCoordinate2 = 37.632495; // Moscow longitude

        // Variables:
        this.mapsDivName = 'clubs-map';
        this.clubs_map = document.getElementById(this.mapsDivName);
        this.rendered = false;

        // Methods:
        this.createClubsMap = function(clubs){ // creates clubs map inside maps-div marked as mapsDivName
            // create a map in the "map" div, set the view to a given place and zoom
            var map = L.map(this.mapsDivName).setView([startCoordinate1, startCoordinate2], 4);
            // add an OpenStreetMap tile layer
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);
            // add a marker in the given location, attach some popup content to it and open the popup
            _.each(clubs, function(club, index){
                var coords = club.arena.coords;
                if(coords != null){
                    var coordinate1 = coords.split(',')[0];
                    var coordinate2 = coords.split(',')[1];
                }
                var clubIcon = L.icon({
                    iconUrl: 'http://dev.sportomatics.ru'+ club.logo,
                    iconSize: [24, 24],
                    iconAnchor: [22, 94],
                    popupAnchor: [-4, -76],
                    shadowUrl: 'http://127.0.0.1:8000/static/leaflet-0.7.3/images/marker-icon-2x.png',
                    shadowSize: [34, 48],
                    shadowAnchor: [27, 94]
                });
                if(coordinate1 && coordinate2){
                    L.marker([coordinate1, coordinate2], {icon: clubIcon}).addTo(map).bindPopup(club.title + '<br>');
                }
            });
            this.rendered = true;
        };

        this.isRendered = function(){ // return map rendered state
            return this.rendered;
        };

        this.setRendered = function(value){ // set boolean state for map rendered variable
            if(value !== true && value !== false) return;
            this.rendered = value;
        }
});