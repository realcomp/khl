angular.module('Sportomatics').controller('RegistrationController', [
    '$http', '$scope','$templateCache','$q', '$cookies', '$location', 'tags', 'ProfileService',
    function($http, $scope, $templateCache, $q, $cookies, $location, tags, ProfileService) {
        $scope.$location = $location;
        if (($location.search().uidb64 && $location.search().token) || $location.search().remember) {
            $scope.selectedType = 'remember';
        } else {
            $scope.selectedType = 'social';
        }
        $scope.user = {};
        $scope.avatar = null;
        $scope.userCreated = false;
        $scope.errors = {};
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
                    // return $scope.user.login && $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);
                    return $scope.user.password && $scope.user.password2 && $scope.user.password == $scope.user.password2 && $scope.user.email && validateEmail($scope.user.email);
                case 2:
                    return true;
                case 3:
                    return true;
            }
            return false;
        };
        $scope.comparePasswords = function(password, password2) {
            if(password && password2){
                if(password === password2) {
                    // $scope.passwordsMatch = true;
                    return true;
                } else {
                    return false;
                }
            }
            // $scope.passwordsMatch = false;
            return false;
        };
        $scope.saveStep = function(){
            var config = {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken
                },
            },
            data;

            switch($scope.currentStep){
                case 0:
                    if($scope.personalInfo){
                        var userToLocalStorage;
                        angular.copy($scope.user, userToLocalStorage);
                        userToLocalStorage.password = undefined;
                        userToLocalStorage.password2 = undefined;
                        localStorage.setItem('sportomatics_registrationUserInfo', JSON.stringify(userToLocalStorage));
                        $scope.currentStep += 1;
                        $scope.currentStepTemplate = 'step' + $scope.currentStep;
                    }
                    break;
                case 1:
                    if($scope.personalInfo){
                        data = {
                            username: $scope.user.email,
                            password: $scope.user.password,
                            email_notification: $scope.subscribe
                        };
                        localStorage.setItem('sportomatics_registrationPersonalInfo', JSON.stringify($scope.personal));
                        if ($scope.userCreated) {
                            $http.patch($scope.profileURL, data, config).success(function(data) {
                                $scope.errors = {};
                                $scope.currentStep += 1;
                                $scope.currentStepTemplate = 'step' + $scope.currentStep;
                            }).error(function(data) {
                                $scope.errors = data;
                            });
                        } else {
                            $http.post($scope.registrationURL, data, config).success(function(data) {
                                $scope.userCreated = true;
                                $scope.errors = {};
                                $scope.currentStep += 1;
                                $scope.currentStepTemplate = 'step' + $scope.currentStep;
                            }).error(function(data) {
                                $scope.errors = data;
                            });
                        }
                    }
                    break;
                case 2:
                    if($scope.personalInfo){
                        data = {
                            fio: $scope.personal.name,
                            name_visible: !$scope.personal.hideName,
                            website: $scope.personal.website
                        };
                        $http.patch($scope.profileURL, data, config).success(function(data) {
                            $scope.errors = {};
                            $scope.currentStep += 1;
                            $scope.currentStepTemplate = 'step' + $scope.currentStep;
                        }).error(function(data) {
                            $scope.errors = data;
                        });
                    }
                    break;
                case 3:
                    if($scope.personalInfo){
                        data = {
                            sport_hockey: $scope.preferencesSports.hockey,
                            sport_football: $scope.preferencesSports.football,
                            sport_basketball: $scope.preferencesSports.basketball,
                            countries: [],
                            clubs: []
                        };
                        $.each($scope.countries, function() {
                            data.countries.push(+this.pk);
                        });
                        $.each($scope.tags, function() {
                            data.clubs.push(+this.pk);
                        });
                        $http.patch($scope.profileURL, data, config).success(function(data) {
                            document.location = $scope.redirectURL;
                        });
                    }
                    break;
            }
        };
        $scope.nextStep = function(skip){
            if (skip) {
                if ($scope.currentStep !== 3) {
                    $scope.currentStep += 1;
                    $scope.currentStepTemplate = 'step' + $scope.currentStep;
                } else {
                    document.location = $scope.redirectURL;
                }
            } else {
                if($scope.checkStep()) {
                    $scope.saveStep();
                } else {
                    alert('Введите все данные');
                }
            }
        };
        $scope.prevStep = function(){
            $scope.currentStep -= 1;
            $scope.currentStepTemplate = 'step'+ $scope.currentStep;
        };
        $scope.getAjaxConfig = function() {
            return {
                'headers': {
                    'X-CSRFToken': $cookies.csrftoken
                },
            };
        };
        $scope.remindPassword = function() {
            var data = {
                email: $scope.rememberPasswordData.email
            };
            $http.post($scope.passwordResetURL, data, $scope.getAjaxConfig()).success(function(data) {
                $scope.rememberPasswordData.isSent = true;
                $scope.rememberPasswordData.errors = null;
            }).error(function(data) {
                $scope.rememberPasswordData.errors = data;
            });
        };
        $scope.setPassword = function() {
            var data = {
                uidb64: $location.search().uidb64,
                token: $location.search().token,
                password: $scope.rememberPasswordData.password
            };
            if ($scope.rememberPasswordData.password && $scope.rememberPasswordData.password2 &&
                   $scope.rememberPasswordData.password === $scope.rememberPasswordData.password2) {
                $http.post($scope.passwordResetConfirmURL, data, $scope.getAjaxConfig()).success(function(data) {
                    $scope.rememberPasswordData.isComplete = true;
                    $scope.rememberPasswordData.errors = null;
                }).error(function(data) {
                    $scope.rememberPasswordData.errors = data;
                });
            }
        };
    }
]);
        function validateEmail(email) {
            var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
            return re.test(email);
        }
