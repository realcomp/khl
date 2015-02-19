angular.module('Sportomatics')
.controller('PlayersSearchController', ['$http', '$scope', 'PlayersSearchService',
    function($http, $scope, PlayersSearchService) {
    var self = this,
        getUnchecker = function(isDefault, defaultValue) {
            return function() {
                if ((isDefault && $(this).attr('value') !== defaultValue) ||
                    (!isDefault && $(this).attr('value') === defaultValue)) {
                    $(this).attr('checked', false);
                }
            };
        };

    $scope.PlayersSearchService = PlayersSearchService;

    $scope.data = {};
    $scope.countries = null;
    $scope.loader = false;

    $scope.params = {
        orderBy: '[%22%s_lastname%22,%22%s_name%22]',
        orderByReversed: false,
        ratedBy: '',
        alphabetFilter: null,
        isPlaying: true,
        playersFilter: null,
        clubsFilter: null,
        countriesSelected: [],
        leaguesSelected: []
    };

    $scope.PlayerPartnersPopup = {
        data: null,
        isClubsVisible: false
    };

    $scope.PlayerPartnersPopupShow = function(e, event) {
        var popup = $('.player-partners-popup:hidden'),
        url = $('#PlayerCardLink').attr('href');
        if (popup.length) {
            $scope.PlayerPartnersPopup.data = null;
            $http.get(url.replace(0, this.player.pk))
            .success(function(data) {
                $scope.PlayerPartnersPopup.data = data;
            });
            $('.player-partners-popup:hidden').show(500).offset({
                left: event.pageX,
                top: event.pageY
            });
        }
    };

    $scope.moreClubs = function(e) {
        $(e).closest('td').toggleClass('show-more-clubs')
    };

    $scope.lineCheck = function(e) {
        var defaultValue = '[0,1,2,3]',
            isDefault;
        isDefault = $(e).attr('value') === defaultValue;
        if ($(e).is(':checked')) {
            $('input[name="line"]').each(getUnchecker(isDefault, defaultValue));
        }
    };

    $scope.setCitizenship = function(event) {
        if (event.target.id === 'isCitizenshipAll' && event.target.checked) {
            $('#isCitizenshipRussia').attr('checked', false);
            $('#isCitizenshipOther').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipRussia' && event.target.checked) {
            $('#isCitizenshipAll').attr('checked', false);
        }
        if (event.target.id === 'isCitizenshipOther' && event.target.checked) {
            self.isCitizenshipOther = event.target.checked;
            self.isCitizenshipAll = false;
            $('#isCitizenshipAll').attr('checked', false);
        }
    }

    $scope.contractCheck = function(e) {
        var isDefault = $(e).attr('value') === '';
        if ($(e).is(':checked')) {
            $('input[name="contract"]').each(getUnchecker(isDefault, ''));
        }
    };

    $scope.setPlayersFilter = function(obj) {
        PlayersSearchService.setPlayersFilter($scope, obj);
    };

    $scope.setClubsFilter = function(obj) {
        PlayersSearchService.setClubsFilter($scope, obj);
    };

    PlayersSearchService.search($scope);
}]);
