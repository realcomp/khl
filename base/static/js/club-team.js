$(function(){
$('.tab-photo-wrap .ui.button').click(function(){
   $('.active-photo-table').removeClass('active-photo-table').addClass('disactive-photo-table')
   $(this).removeClass('disactive-photo-table').addClass('active-photo-table')
   });

});