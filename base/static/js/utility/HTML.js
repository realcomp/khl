var HTML_CLUB_GAMES_DIV, HTML_CLUB_HOME_ATTENDANCE_DIV, HTML_INDICATORS_LIST_ITEM;

HTML_INDICATORS_LIST_ITEM = function(result, title, image, color) {
  var imgHtml = image ? '<a class="ui image" ><img class="ui image b-diagram__legend__image" src="' + image + '" width="32" height="32"></a>' : '';
  return '<li class="" style="border-right: 5px solid ' + color + ';"> <div class="b-inline b-diagram__legend__table-style__item"> <div class="b-inline hidden-xs">' + imgHtml + '</div> <div class="b-inline"> <p class=""> <a class="no-decoration default-a pointer">' + title + '</a> </p> </div> </div> <p class="b-inline b-diagram__legend__table-style__games">' + result + '</p> </li>';
};

HTML_CLUB_GAMES_DIV = function(title, score, date, leftLogo, rightLogo, color) {
  return '<div class="w-command-calendar__item w-command-calendar__item-bg"> <div class="b-header b-header__xs"> <h5 class="b-header__text">' + title + '</h5> </div> <div class="row"> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + leftLogo + '"> </a> </div> <p class="col-sm-2 col-md-12 col-lg-4 b-score" style="color: ' + color + '">' + score + '</p> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + rightLogo + '"> </a> </div> </div> <div class="w-command-calendar__info"> <p class="date">' + date + ' МСК </p> </div> </div>';
};

HTML_CLUB_HOME_ATTENDANCE_DIV = function(title, count, date, leftLogo, rightLogo) {
  return '<div class="w-command-calendar__item w-command-calendar__item-bg"> <div class="b-header b-header__xs"> <h5 class="b-header__text">' + title + '</h5> </div> <div class="row"> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + leftLogo + '"> </a> </div> <p class="col-sm-2 col-md-12 col-lg-4 b-score">' + count + '</p> <div class="col-sm-4 col-md-12 col-lg-4"> <a href="#" class="ui image"> <img class="ui circular image" src="' + rightLogo + '"> </a> </div> </div> <div class="w-command-calendar__info"> <p class="date">' + date + ' МСК </p> </div> </div>';
};
