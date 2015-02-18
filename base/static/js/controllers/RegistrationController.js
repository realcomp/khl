angular.module('Sportomatics')
    .controller('RegistrationController', ['$http', '$scope', function($http, $scope) {

        $scope.selectedType = 'social';
        $scope.user = {};
        $scope.subscribe = true;
        $scope.selectedRegistrationType = 'social';
        $scope.selectType = function(type){
            $scope.selectedType = type;
        }
    }])