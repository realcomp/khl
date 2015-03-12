angular.module('Sportomatics').controller('RegistrationController', [
    '$http', '$scope','$templateCache','$q', '$cookies', 'tags', 'ProfileService',
    function($http, $scope, $templateCache, $q, $cookies, tags, ProfileService) {
        $scope.selectedType = 'social';
        $scope.user = {};
        $scope.personal = {};
        $scope.rememberPasswordData = {};
        $scope.preferences = {};
        $scope.currentStep = 1;
        $scope.currentStepTemplate = 'step1';
        $scope.subscribe = true;
        $scope.personalInfo = true;
        $scope.preferencesInfo = true;
        $scope.rememberWithLogin = true;
        $scope.selectedRegistrationType = 'social';
        $scope.preferencesSports = {
            'hockey': true,
            'football': false,
            'basketball': false
        };
        $scope.tags = [];
        $scope.countries = [];
        $scope.setAvatar = ProfileService.setAvatar;
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
        $scope.saveStep = function(){
            switch($scope.currentStep){
                case 0:
                    if($scope.personalInfo){
                        var userToLocalStorage;
                        angular.copy($scope.user, userToLocalStorage);
                        userToLocalStorage.password = undefined;
                        userToLocalStorage.password2 = undefined;
                        localStorage.setItem('sportomatics_registrationUserInfo', JSON.stringify(userToLocalStorage));
                        $scope.currentStep += 1;
                        $scope.currentStepTemplate = 'step'+ $scope.currentStep;
                    }
                    break;
                case 1:
                    if($scope.personalInfo){
                        var data = {
                            username: $scope.user.email,
                            password: $scope.user.password
                        }, config = {
                            'headers': {
                                'X-CSRFToken': $cookies.csrftoken
                            },
                        };
                        localStorage.setItem('sportomatics_registrationPersonalInfo', JSON.stringify($scope.personal));
                        $http.post('/ru/accounts/api/signup/', data, config).success(function(data) {
                            $scope.currentStep += 1;
                            $scope.currentStepTemplate = 'step'+ $scope.currentStep;
                        });
                    }
                    break;
                case 2:
                    if($scope.personalInfo){
                        console.log($scope.personal);
                        // $scope.currentStep += 1;
                        // $scope.currentStepTemplate = 'step'+ $scope.currentStep;
                    }
                    break;
            }
        };
        $scope.nextStep = function(){
            if($scope.checkStep()) {
                // $scope.currentStep += 1;
                // $scope.currentStepTemplate = 'step'+ $scope.currentStep;
                $scope.saveStep();
            }
            else alert('Введите все данные');
        };
        $scope.prevStep = function(){
            // $scope.currentStep -= 1;
            // $scope.currentStepTemplate = 'step'+ $scope.currentStep;
        }
    }
]);
        function validateEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
