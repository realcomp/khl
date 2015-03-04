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
    return $resource("{% url 'api:hockey:cip_list' %}", {}, {
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
.controller('PhotosController', function($scope, ClubInstaPhoto, InstagramUser, $resource){

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
                club: $scope.club_id
            };
            $scope.photoDataLoader = true;
            ClubInstaPhoto.query(get_params).$promise.then(function (data) {
                $scope.photoDataLoader = false;
                $.each(data.results, function (index, value) {
                    $scope.photos.push(value)
                });
                setTimeout(function(){
                    playerClubsMasonry.imagesLoaded(function(){
                        playerClubsMasonry.masonry({
                            itemSelector: '.item',
                            gutterWidth: 20
                        })
                    });
                }, 100);
                $scope.next_page = data.next_page;
                if (!$scope.next_page && $('#nextpagebutton').length) {
                    $('#nextpagebutton').remove();
                }
            });
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
                //$scope.PhotoPopup.data = ClubInstaPhoto.get({id:id}, function(photo) {
            console.log(index)
            $scope.currentIndex = index;
            var photo = $scope.photos[index];
           // console.log($scope.photos[index]);
            $scope.PhotoPopup.data = $scope.photos[index];
            $scope.photoDataLoader = true;
                $scope.PhotoPopup.instagramUser = InstagramUser.get({id: photo.photo.instagram_user}, function(){
                    $scope.photoDataLoader = false;
                    $scope.PhotoPopup.userStr = photo.photo.user_str;
                    $(".instagram-user-str").val(photo.photo.user_str);
                    $scope.PhotoPopup.data.players = '';
                    /*if(photo.arena){
                     $scope.PhotoPopup.arena = Arena.get({id:photo.arena}, function(arena){
                     $.each(arena.club_set, function(index, value){
                     Club.get({id:value}, function(club){
                     $scope.PhotoPopup.clubSet.push(club);
                     })
                     })
                     })
                     }*/
                    var params = {date:photo.photo.created, arena:photo.arena};
                    $scope.lastSucceedIndex = index;
                    /*}, function(a){
                     console.log(a)
                     });*/
                    $scope.PhotoPopup.index = index;
                    $('.overlay-black').css('visibility', 'visible');
                    $('.photo-popup').show();
                });

        };
        $scope.nextPhoto = function(){
            var index = $scope.PhotoPopup.index + 1;
            if($scope.photos[index]){
                $scope.PhotoPopup.domIndex = $scope.photos[index].id;
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'next');
            }
        };
        $scope.prevPhoto = function(){
            var index = $scope.PhotoPopup.index - 1;
            if($scope.photos[index]){
                $scope.PhotoPopup.domIndex = $scope.photos[index].id;
                $scope.PhotoPopupShow($scope.photos[index].id, index, null, 'prev');
            }
        };

        $scope.getPage();
})