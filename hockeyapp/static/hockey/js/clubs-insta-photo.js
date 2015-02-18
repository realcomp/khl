(function() {
    var app = angular.module('SportomaticsAdminClubPhotos', []);

    app.controller('AdminClubPhotoController', ['$http', '$scope', function($http, $scope) {
        url = $('#photos-new').attr('apiurl');

        $scope.loadPhotos = function(callback) {
            $http.get(url).success(function(data) {
                $scope.photos = data;
                if (typeof callback === 'function') {
                    callback();
                }
            });
        };
        $scope.loadPhotos();
    }]);
})();
