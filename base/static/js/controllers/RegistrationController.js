angular.module('Sportomatics')
    .controller('RegistrationController', ['$http', '$scope','$templateCache','$q','tags', function($http, $scope, $templateCache, $q, tags) {
        $scope.selectedType = 'regular';
        $scope.user = {};
        $scope.personal = {};
        $scope.currentStep = 2;
        $scope.currentStepTemplate = 'step2';
        $scope.subscribe = true;
        $scope.personalInfo = true;
        $scope.preferencesInfo = true;
        $scope.selectedRegistrationType = 'social';
        $scope.preferencesSports = {
            'hockey': true,
            'football': false,
            'backetball': false
        };
        $scope.tags = [];
        $scope.countries = [];
        $scope.loadTagsCountries = function (query) {
            return tags.loadCountries(query);
        };
        $scope.loadTags = function(query) {
            return tags.loadClubs(query);
        };
        $scope.$watch('countries', function(newval, oldval){
            console.log(newval);
        }, true);
        $scope.log = function(){
            console.log($scope.preferencesSports);
        };
        $scope.selectType = function(type){
            $scope.selectedType = type;
        };
        $scope.checkStep = function(){
            switch($scope.currentStep){
                case 1:
                    return $scope.user.login && $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);

                case 2:
                    return true;
            }
            return false;
        };
        $scope.comparePasswords = function(){
            if($scope.user.password && $scope.user.password2){
                if($scope.user.password == $scope.user.password2) {
                    $scope.passwordsMatch = true;
                    return true;
                }
            }
            $scope.passwordsMatch = false;
            return false;
        };
        $scope.nextStep = function(){
            if($scope.checkStep()) {
                $scope.currentStep += 1;
                $scope.currentStepTemplate = 'step'+ $scope.currentStep;
            }
            else alert('Введите все данные');
        }
    }])
        function validateEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }