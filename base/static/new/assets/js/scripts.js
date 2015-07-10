
var ismobile = (/iphone|ipad|ipod|android|blackberry|mini|windows\sce|palm/i.test(navigator.userAgent.toLowerCase()));

$(document).ready(function() {


//-------------------------no mobile devicies
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


//-----------accordion
	$('.ui.accordion').accordion();


//-----------push mobile menu
	//-------new mlPushMenu( document.getElementById( 'mp-menu' ), document.getElementById( 'trigger' ) );



//-----------search variants

	var content = [
	  { title: 'Andorrs' },
	  { title: 'United Arab Emirates' },
	  { title: 'Afghanistas' },
	  { title: 'Antigus' },
	  { title: 'Anguills' },
	  { title: 'Albanis' },
	  { title: 'Armenis' },
	  { title: 'Netherlands Antilles' },
	  { title: 'Angols' },
	  { title: 'Argentins' },
	  { title: 'American Samos' },
	  { title: 'Austris' },
	  { title: 'Australis' },
	  { title: 'Arubs' },
	  { title: 'Aland Islands' },
	  { title: 'Azerbaijas' }
	];
	$('.result').search({
	    source: content
	  });

});

//-----------sticky menu
$(window).bind('scroll', function() {
	var scrollPos = $(window).scrollTop();
	if(scrollPos > 164 && !ismobile) {
		$('main').addClass('w-sticky');
	} else {
		$('main').removeClass('w-sticky');
	}
});