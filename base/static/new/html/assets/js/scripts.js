$(document).ready(function() {


//-------------------------no mobile devicies
var ismobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));
    if(!ismobile) {
    	$('body').removeClass('mobile-body').addClass('desktop-body');
    } else {
	    $('body').removeClass('desktop-body').addClass('mobile-body');
    }
//-------------------------no mobile devicies ends



//-----------dropdown
	$('.ui.dropdown').dropdown();



//-----------tabs
	$('.tabular.menu .item').tab();
	$('.tabular-xs.menu .item').tab();


//-----------checkbox
	$('.ui.checkbox').checkbox();


//-----------checkbox
	$('.w-tooltip').popup();


//-----------push mobile menu
	new mlPushMenu( document.getElementById( 'mp-menu' ), document.getElementById( 'trigger' ) );


});