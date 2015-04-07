$(function () {
    $('.ui.dropdown').dropdown();
    $('.checkbox').checkbox();
    $('#search-select').dropdown();
    $('#checkCountry').checkbox();
    $('#checkC').checkbox();
    $('#datepicker').datepicker();

    $("#range").ionRangeSlider({
        hide_min_max: true,
        keyboard: true,
        min: 15,
        max: 45,
        from: 28,
        to: 32,
        type: 'double',
        step: 1,
        grid: false
    });

    $("#rangeTwo").ionRangeSlider({
        hide_min_max: true,
        keyboard: true,
        min: 0,
        max: 100,
        from: 40,
        to: 80,
        type: 'double',
        step: 1,
        grid: false
    });

    $(function() {
        $('select').styler();
    });

    (jQuery);
    jQuery(function(){
        jQuery('.jq-select-multiple ul').jScrollPane({
            verticalDragMinHeight: 20,
            verticalDragMaxHeight: 20
        });
    });
});
