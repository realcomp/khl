angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout', 'MapService',
    function($http, $scope, $timeout, MapService) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        popup = null;
        $scope.type = 'photos';
        $scope.cache_players = null;
        $scope.cache_clubs = null;
        $scope.notplaying_players = null;

        $scope.setType = function(type){
            $scope.type = type;
            $scope.unMakeTransferArrows()
        };

        $scope.go = function(path){
            window.location.href = path;
        };

        $scope.PlayerPartnersPopup = {
            data: null,
            isClubsVisible: true
        };

        $scope.PlayerPartnersPopupShow = function(e, event) {
            var popup = $('.player-partners-popup:hidden'),
            url = $('#PlayerCardLink').attr('href'),
            pk;
            if (popup.length && this.cell_id[0] !== 'trainer') {
                pk = self.getCell(self.players, this.cell_id).pk;
                $scope.PlayerPartnersPopup.data = null;
                $http.get(url.replace(0, pk))
                .success(function(data) {
                    $scope.PlayerPartnersPopup.data = data;
                });
                $('.player-partners-popup:hidden').show(500).offset({
                    left: event.pageX,
                    top: event.pageY
                });
            }
        };

        self.players = {};
        self.clubs = {
            'getLastClub': function() {
                if (this.clubs.length) {
                    return this.clubs[this.clubs.length - 1];
                }
            },
            'clubs': []
        };

        $scope.setSeason = function(e) {
            self.list(self.compare);
        };

        $scope.workWithData = function(data){
            console.log(data);

            if(MapService.isRendered()) MapService.remove();
            MapService.createClubsMap(data.all_players, 'players');

            var goalkeeper_players = data.goalkeeper_players;
            var defender_players = data.defender_players;
            var offender_players = data.offender_players;
            var players = [];
            _.each(offender_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
            _.each(defender_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
            _.each(goalkeeper_players, function(player){
                players.push(player.pk);
                if(player.citizenship){
                    if(!player.citizenship.code){
                        _.each($scope.countryCodes, function(country){
                            if(player.citizenship.title)
                            if(country.name === player.citizenship.title){
                                player.citizenship.code = country.code;
                            }
                        })
                    }
                }
            });
        };

        self.getCell = function(table, cell_id) {
            var group;
            if (table.table && cell_id && Array.isArray(cell_id) && cell_id[1] !== null) {
                group = table.table[cell_id[0]];
                if (group) {
                    return group[cell_id[1]];
                }
            }
        };

        self.isPersonVisible = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            if (cell) {
                switch (self.players.status) {
                    default:
                        return true;
                    case 'joined':
                        return cell.is_joined;
                    case 'left':
                        return cell.is_left;
                    case 'legionnaire':
                        return cell.is_legionnaire;
                    case 'home':
                        return cell.is_home;
                }
            } else {
                return false;
            }
        };

        self.isPersonInCell = function(table, cell_id) {
            var cell;
            cell = this.getCell(table, cell_id);
            return cell;
        };

        self.list = function(callback, callbackArg) {
            var params = $('#ClubTeamForm').serialize();
            self.players.data = null;
            self.players.table = null;
            self.players.loader = true;
            self.clubs.clubs = [];
            $http.get(url + '?' + params)
            .success(function(data) {
                $scope.players = data;
                self.players.data = data;
                self.players.table = {
                    'goalkeeper': data.goalkeeper_players,
                    'defender': data.defender_players,
                    'forward': data.offender_players,
                    'trainer': data.coaches
                };
                $http.get('/static/json/countries-json-ru-codes.json')
                .success(function(data){
                    $scope.countryCodes = data;
                }).then(function(){
                    $scope.workWithData($scope.players);
                });
                self.players.loader = false;
                if (typeof callback === 'function') {
                    callback(callbackArg);
                }
            });
        };

        this.compare = function(arg) {
            var url = $('#ClubTeamCompareLink').attr('href'),
            club = self.clubs.getLastClub(),
            params, leagues;
            if (club) {
                params = 'source_season=' + club.data.season.pk +
                    '&season=' + club.data.prev_season.pk;
            } else {
                params = 'source_season=' + self.players.data.season.pk +
                    '&season=' + self.players.data.prev_season.pk;
            }
            self.clubs.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                    console.log(data)
                if (data.leagues.length) {
                    var clubRows = [];
                    var clubsInRow = [];
                    var clubs = [];
                    $scope.clubplayers = [];
                    _.each(data.leagues, function(league, index){
                        clubs = clubs.concat(league.clubs);
                        $scope.clubplayers = $scope.clubplayers.concat(league.clubplayers);
                    });
                    _.each(clubs, function(club, index){
                        if(clubsInRow.length < 7){
                            clubsInRow.push(club)
                        }
                        if(index === clubs.length -1 || (index + 1) % 7 === 0){
                            clubRows.push(clubsInRow);
                            clubsInRow = [];
                        }
                    });
                    var clubsObject = {
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs
                        },
                        'league': data.leagues[0],
                        'clubRows': clubRows
                    };
                    self.clubs.clubs.push(clubsObject);
                }
                self.clubs.loader = false;
                if(arg !== false){
                }
            });
        };

        $scope.getFromCache = function() {
            if ($scope.cache_players) {
                $scope.players = $scope.cache_players;
                $scope.clubs = $scope.cache_clubs;
            }
        };

        $scope.makeTransferArrows = function(){
            $scope.getFromCache();
            _.each($scope.clubplayers, function(clubplayer){
                createTransferArrow('#club_'+clubplayer.club, '#player_'+clubplayer.player, clubplayer.pk);
            });
            $( ".player-item" ).each(function() {
                if(!_.findWhere($scope.clubplayers, {player: parseInt($(this).attr('id').split('_')[1]) })){
                    $( this ).addClass("opacity-30");
                } else {
                    var id = $(this).attr('id');
                    $(this).hover(function(){
                        $("canvas").each(function(){
                            if ($(this).attr('player') !== id)
                                $(this).addClass("opacity-10");
                        })
                    }, function(){
                        $("canvas").each(function(){
                            $(this).removeClass("opacity-10");
                        })
                    })
                }
            });
        };
        $scope.unMakeTransferArrows = function(){
            $scope.getFromCache();
            $('canvas').remove();
            $( ".player-item" ).each(function() {
                $( this ).removeClass("opacity-30");
            });
        };

        //this.list(this.compare, false);

        $scope.notPlayingNow = function(callback, callbackArg) {
            $scope.unMakeTransferArrows();
            $scope.players.loader = true;
            if ($scope.notplaying_players) {
                $scope.players = $scope.notplaying_players;
            } else {
                $http.get(url+'?notplaying=1').success(function(data) {
                    $scope.cache_players = $scope.players;
                    $scope.cache_clubs = $scope.clubs;
                    $scope.players = data;
                    $scope.players.data = data;
                    $scope.players.table = {
                        'goalkeeper': data.goalkeeper_players,
                        'defender': data.defender_players,
                        'forward': data.offender_players,
                        'trainer': data.coaches
                    };
                    $scope.notplaying_players = $scope.players;
                });
            }
            $scope.workWithData($scope.players);
            $scope.players.loader = false;
            if (typeof callback === 'function') {
                callback(callbackArg);
            }
        };

        function drawArr(c, fromx, fromy, tox, toy){
            //variables to be used when creating the arrow
            var ctx = c;
            var headlen = 5;
            var angle = Math.atan2(toy-fromy,tox-fromx);
            //starting path of the arrow from the start square to the end square and drawing the stroke
            ctx.beginPath();
            ctx.moveTo(fromx, fromy);
            var amount = 0;
            (function myLoop (amount) {
               setTimeout(function () {
                   amount += 0.05; // change to alter duration
                    ctx.lineWidth = 5;
                    ctx.lineTo(fromx + (tox - fromx) * amount,
                             fromy + (toy - fromy) * amount);
                    ctx.stroke();
                    if (amount < 1){
                       myLoop(amount);
                    }
                    else {
                         //starting a new path from the head of the arrow to one of the sides of the point
                        ctx.beginPath();
                        ctx.moveTo(tox, toy);
                        ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));

                        //path from the side point of the arrow, to the other side point
                        ctx.lineTo(tox-headlen*Math.cos(angle+Math.PI/7),toy-headlen*Math.sin(angle+Math.PI/7));

                        //path from the side point back to the tip of the arrow, and then again to the opposite side point
                        ctx.lineTo(tox, toy);
                        ctx.lineTo(tox-headlen*Math.cos(angle-Math.PI/7),toy-headlen*Math.sin(angle-Math.PI/7));

                        //draws the paths created above
                        //ctx.strokeStyle = "#cc0000";
                        ctx.lineWidth = 5;
                        ctx.stroke();
                        ctx.fill();
                    }
               }, 30)
            })(0);
            //ctx.lineTo(tox, toy);
            //ctx.strokeStyle = "#cc0000";
            //ctx.lineWidth = 10;
            //ctx.stroke();
        }

        function createTransferArrow(from, to, id){
                var $from = $(from);
                var $to = $(to);
                // find offset positions for the word (t = this) and image (i)
                var ofrom = {
                    x: $from.offset().left + $from.width() / 2,
                    y: $from.offset().top + $from.height() / 2
                };
                var oto = {
                    x: $to.offset().left + $to.width() / 2,
                    y: $to.offset().top + $to.height() / 2
                };
                // x,y = top left corner
                // x1,y1 = bottom right corner
                var p = {
                    x: ofrom.x < oto.x ? ofrom.x : oto.x,
                    x1: ofrom.x > oto.x ? ofrom.x : oto.x,
                    y: ofrom.y < oto.y ? ofrom.y : oto.y,
                    y1: ofrom.y > oto.y ? ofrom.y : oto.y
                };
                // create canvas between those potonts
                var c = $('<canvas id="'+id+'" player="'+ to.replace('#', '') + '" />').attr({
                    'width': p.x1 - p.x + 20 ,
                    'height': p.y1 - p.y + 20
                }).css({
                    'position': 'absolute',
                    'left': p.x,
                    'top': p.y,
                    'z-index': 1
                }).appendTo($('body'))[0].getContext('2d');

                // draw line
                var x1 = ofrom.x - p.x + 10;
                var y1 = ofrom.y - p.y - 30;
                var x2 = oto.x - p.x; //+20
                var y2 = oto.y - p.y + 40;

                drawArr(c, x1,y1,x2,y2,1,2);
        }

    }
]);