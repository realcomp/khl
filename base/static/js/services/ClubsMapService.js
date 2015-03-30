angular.module('Sportomatics').service('ClubsMapService', function(){
        var coordinates = document.getElementById('coordinates');
        var clubs_map = document.getElementById('clubs-map');
        var title = $('#place-title').val();
        var coordinate1 = 59;
        var coordinate2 = 38;
        this.a = 'abc';
        this.rendered = false;


        this.createClubsMap = function(clubs){
            // create a map in the "map" div, set the view to a given place and zoom
            var map = L.map('clubs-map').setView([coordinate1, coordinate2], 4);
            // add an OpenStreetMap tile layer
            L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            // add a marker in the given location, attach some popup content to it and open the popup

            var myIcon = L.icon({
                iconUrl: 'http://dev.sportomatics.ru/media/filer_public/cf/4b/cf4b1a63-4f02-4f84-8953-27185077e6cc/7b84c940f884393f3b79dbd94dd9fa15.jpg',
                iconSize: [24, 24],
                iconAnchor: [22, 94],
                popupAnchor: [-4, -76],
                shadowUrl: 'http://127.0.0.1:8000/static/leaflet-0.7.3/images/marker-icon-2x.png',
                shadowSize: [34, 48],
                shadowAnchor: [27, 94]
            });
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
            //L.marker([50.505, 30.57], {icon: myIcon}).addTo(map).bindPopup('Авангард' + '<br>');
            this.rendered = true;
        }
    this.isRendered = function(){
        return this.rendered;
    }
});