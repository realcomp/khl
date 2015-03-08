angular.module('Sportomatics')
    .config(['$resourceProvider', function($resourceProvider) {
        // Don't strip trailing slashes from calculated URLs
        $resourceProvider.defaults.stripTrailingSlashes = false;
    }])
.factory('ClubInstaPhoto', function($resource){
    return $resource("/ru/api/hockey/clubinstaphoto/"+":id/", {}, {
        query: {method:'GET', params:{processed: 1, id: null}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('PlayerInstaPhoto', function($resource){
    return $resource("/ru/api/hockey/playerinstaphoto/", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('ArenaInstaPhoto', function($resource){
    return $resource("{% url 'api:hockey:cip_list' %}", {}, {
        query: {method:'GET', params:{processed: 1}},
        get: { method: 'GET'},
        update: { method: 'PATCH'},
        delete: { method: 'DELETE'}
    });
})
.factory('InstagramUser', function($resource){
    return $resource("/ru/api/base/instagram_user/"+":id/", {}, {
        query: {method:'GET', params:{id:null}, isArray:true},
        get: { method: 'GET'}
    });
})
.controller('PhotosController', function($scope, ClubInstaPhoto, InstagramUser,PlayerInstaPhoto, $resource){

        var playerClubsMasonry = $('.masonry-clubs-photos');
        var closePopupBtn = $('#close-popup-btn');


        closePopupBtn.on('click', function(e) {
            e.preventDefault();
            $(this).parent().hide();
            $scope.clearPopupFields();
            $('.overlay-black').css('visibility', 'hidden');
            $scope.selectedClub = null;
        });
        $('.overlay-black').on('click', function(event){
            $('.photo-popup').hide();
            $('.overlay-black').css('visibility', 'hidden');
        });

        $scope.club_id = $('#team-id').val();
        $scope.player_id = $('#player-id').val();

        $scope.photos = [];
        $scope.next_page = 1;
        $scope.currentIndex = 0;

        $scope.getPage = function(){
            var get_params = {
                page: $scope.next_page,
                min_id: 0,
                max_id: 10000000,
                club: $scope.club_id,
                player: $scope.player_id
            };
            $scope.photoDataLoader = true;
            if($scope.club_id){
                ClubInstaPhoto.query(get_params).$promise.then(function (data) {
                    $scope.photoDataLoader = false;
                    $.each(data.results, function (index, value) {
                        value.created = new Date(value.photo.created).instagramDateFormat();
                        $scope.photos.push(value)
                    });
                    setTimeout(function(){
                        $('.photo-square').hover(function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '1');
                        }, function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '0');
                        });
                    }, 100);
                    $scope.next_page = data.next_page;
                    if (!$scope.next_page && $('#nextpagebutton').length) {
                        $('#nextpagebutton').remove();
                    }
                });
            } else if ($scope.player_id){
                PlayerInstaPhoto.query(get_params).$promise.then(function (data) {
                    $scope.photoDataLoader = false;
                    $.each(data.results, function (index, value) {
                        value.created = new Date(value.photo.created).instagramDateFormat();
                        $scope.photos.push(value)
                    });
                    setTimeout(function(){
                        $('.photo-square').hover(function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '1');
                        }, function(){
                            var id = $(this).attr('id');
                            $('#instaphoto-header-time_'+id+', #instaphoto-footer-stats_'+id).css('opacity', '0');
                        });
                    }, 100);
                    $scope.next_page = data.next_page;
                    if (!$scope.next_page && $('#nextpagebutton').length) {
                        $('#nextpagebutton').remove();
                    }
                }, function(){
                    $scope.photoDataLoader = false;
                });
            }
        };

        $scope.nextPage = function(){
            if($scope.next_page) {
                $scope.getPage();
            }
        };

        $scope.PhotoPopup = {
            data: null,
            index: null
        };

        $scope.PhotoPopupShow = function(id, index, event, position){
            $scope.currentIndex = index;
            var photo = $scope.photos[index];
            $scope.PhotoPopup.data = $scope.photos[index];
            $scope.PhotoPopup.instagramUser = InstagramUser.get({id: photo.photo.instagram_user}, function(){

            });
            $scope.PhotoPopup.comment = photo.photo.comment;
            $(".instagram-comment").val(photo.photo.comment);
            $('.overlay-black').css('visibility', 'visible');
            $('.photo-popup').show();
            $scope.PhotoPopup.index = index;

        };
        $scope.nextPhoto = function(){
            var index = $scope.PhotoPopup.index + 1;
            $scope.currentIndex++;
            if($scope.photos[index]){
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'next');
            }
        };
        $scope.prevPhoto = function(){
            var index = $scope.PhotoPopup.index - 1;
            if($scope.photos[index]){
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'prev');
            }
        };

        $scope.getPage();

        Date.prototype.instagramDateFormat = function(){
            var monthsRu = ["января", "февраля", "марта", "апреля", "мая","июня","июля", "августа", "сентября", "октября", "ноября", "декабря"];
            return this.getDate() + ' ' + monthsRu[this.getMonth()] + ' ' + this.getFullYear();
        }
})