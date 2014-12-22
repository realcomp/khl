$(document).ready(function(){

    var playerPartnersLink = $('.player-partners-link'),
        playerPartnersPopup = $('.player-partners-popup'),
        closePopupBtn = $('.close-popup-btn'),
        playerPhotosMasonry = $('.masonry-player-photos'),
        playerNewsMasonry = $('.masonry-player-news'),
        playerCardMoreBtn = $('.player-card-more-btn'),
        playerCardListMore = $('.player-card-list-more'),
        moreClubsBtn = $('.more-clubs-btn'),
        clubsCountriesMenu = $('.clubs-countries-menu-list'),
        showClubsCountriesMenuBtn = $('.show-clubs-countries-menu-btn');

    $('.ui.dropdown').dropdown();
    // $('.tabular .item').tab({history:false});
    $('.ui.selection.dropdown').dropdown();
    $('.ui.checkbox').checkbox();
    $('.payment-block_new').tabs();
    $('.payment-block_old').tabs();
    $('.team-calendar').tabs();
    $('.clubs-tabs').tabs();

    $(".players-diff-year-slider" ).slider({
        range: true,
        min: 1975,
        max: 2014,
        values: [ 2001, 2014 ],
        slide: function( event, ui ) {
            $(".players-diff-first-year-amount").val( ui.values[ 0 ]);
            $(".players-diff-second-year-amount").val( ui.values[ 1 ]);
        }
    });

    $(".players-diff-first-year-amount").val( $(".players-diff-year-slider").slider("values", 0));
    $(".players-diff-second-year-amount").val( $(".players-diff-year-slider").slider("values", 1));
    $(".players-diff-slider-limits .slider-limits-min").text( $(".players-diff-year-slider").slider("option", "min"));
    $(".players-diff-slider-limits .slider-limits-max").text( $(".players-diff-year-slider").slider("option", "max"));

    $(".players-graph-slider" ).slider({
        orientation: "vertical",
        range: "min",
        min: 2001,
        max: 2015,
        value: 2007,
        slide: function( event, ui ) {
            $(".players-graph-year").val( ui.value);
        }
    });
    
    $(".players-graph-year").val( $(".players-graph-slider").slider("values", 0));
    $(".players-graph-slider-limits .slider-limits-min").text( $(".players-graph-slider").slider("option", "min"));
    $(".players-graph-slider-limits .slider-limits-max").text( $(".players-graph-slider").slider("option", "max"));

    $(".home-main-slider").slides({
        generateNextPrev: false,
        generatePagination: false
    });

    $(".player-photos-slider").slides({
        generateNextPrev: false,
        generatePagination: false
    });

    $(".clubs-photos-slider").slides({
        generateNextPrev: false,
        generatePagination: false
    });

    $(".player-news-slider").slides({
        generateNextPrev: false,
        generatePagination: false
    });

    $(".player-achievement-slider").slides({
        generateNextPrev: false,
        generatePagination: false
    });

    $( ".datepicker" ).datepicker();

    playerPartnersLink.on('click', function(e) {
        e.preventDefault();

        playerPartnersPopup.show(300);
    });

    closePopupBtn.on('click', function(e) {
        e.preventDefault();
        
        $(this).parent().hide(300);
    });

    playerPhotosMasonry.imagesLoaded(function(){
        playerPhotosMasonry.masonry({
            itemSelector: '.item',
            gutterWidth: 20
        });
    });

    playerNewsMasonry.imagesLoaded(function(){
        playerNewsMasonry.masonry({
            itemSelector: '.item',
            gutterWidth: 20
        });
    });

    //submit language form on click
    $('div.menu > a').click(function(e) {
        e.stopPropagation();
        $('#languageselect input[name=language]').val($(this).attr('href').substring(1));
        $('#languageselect').submit();
    });

    playerCardMoreBtn.on('click', function(e) {
        e.preventDefault();

        playerCardListMore.toggle(300);
    });

    moreClubsBtn.on('click', function(e) {
        e.preventDefault();
        
        $(this).closest('td').toggleClass('show-more-clubs');
    });

    showClubsCountriesMenuBtn.on('click', function(e) {
        e.preventDefault();
        
        clubsCountriesMenu.toggleClass('clubs-countries-menu-list_all');
    });
});