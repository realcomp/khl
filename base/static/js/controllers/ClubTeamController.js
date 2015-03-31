angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope', '$timeout',
    function($http, $scope, $timeout) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        popup = null;
        $scope.type = 'photos';
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

        self.PLAYERS_TABLE = [ // table indexes, null is an empty filler
            // row 1
            [['defender', 0], ['defender', null], ['defender', 1], ['defender', null],
             ['defender', 2], ['defender', null], ['defender', 3],
             ['forward', null], ['forward', 0], ['forward', null],
             ['goalkeeper', 0]],
            // row 2
            [['defender', null], ['defender', 4], ['defender', null],
             ['forward', 1], ['forward', null], ['forward', 2], ['forward', null],
             ['forward', 3], ['forward', null], ['forward', 4],
             ['goalkeeper', null]],
            // row 3
            [['defender', 5], ['defender', null], ['defender', 6],
             ['forward', null], ['forward', 5], ['forward', null], ['forward', 6],
             ['forward', null], ['forward', 7], ['forward', null],
             ['goalkeeper', 1]],
            // row 4
            [['defender', null], ['defender', 7], ['defender', null],
             ['forward', 8], ['forward', null], ['forward', 9], ['forward', null],
             ['forward', 10], ['forward', null], ['forward', 11],
             ['goalkeeper', null]],
            // row 5
            [['defender', 8], ['defender', null], ['defender', 9],
             ['forward', null], ['forward', 12], ['forward', null], ['forward', 13],
             ['forward', null], ['forward', 14], ['forward', null],
             ['goalkeeper', 2]],
            // row 6
            [['defender', null], ['defender', 10], ['defender', null],
             ['forward', 15], ['forward', null], ['forward', 16], ['forward', null],
             ['forward', 17], ['forward', null], ['forward', 18],
             ['goalkeeper', null]],
            // row 7
            [['defender', 11], ['defender', null], ['defender', 12],
             ['forward', null], ['forward', 19], ['forward', null], ['forward', 20],
             ['forward', null], ['forward', 21], ['forward', null],
             ['goalkeeper', 3]],
            // row 8
            [['defender', null], ['defender', 13], ['defender', null],
             ['forward', 22], ['forward', null], ['forward', 23], ['forward', null],
             ['forward', 24], ['forward', null], ['forward', 25],
             ['goalkeeper', null]],
            // row 9
            [['defender', 13], ['defender', null], ['defender', 14],
             ['trainer', null], ['trainer', 0], ['trainer', null], ['trainer', 1],
             ['trainer', null], ['trainer', 2], ['trainer', null],
             ['goalkeeper', 4]],
            // row 10
            [['defender', null], ['defender', 15], ['defender', null],
             ['trainer', 3], ['trainer', null], ['trainer', 4], ['trainer', null],
             ['trainer', 5], ['trainer', null], ['trainer', 6],
             ['goalkeeper', null]],
        ];

        self.CLUBS_TABLE = [ // table indexes, null is an empty filler
            // row 1
            [['club', 0], ['club', null], ['club', 1], ['club', null],
             ['club', 2], ['club', null], ['club', 3], ['club', null],
             ['club', 4], ['club', null], ['club', 5]],
            // row 1
            [['club', null], ['club', 6], ['club', null], ['club', 7],
             ['club', null], ['club', 8], ['club', null], ['club', 9],
             ['club', null], ['club', 10],  ['club', null]],
            // row 3
            [['club', 11], ['club', null], ['club', 12], ['club', null],
             ['club', 13], ['club', null], ['club', 14], ['club', null],
             ['club', 15], ['club', null], ['club', 16]],
            // row 4
            [['club', null], ['club', 17], ['club', null], ['club', 18],
             ['club', null], ['club', 19], ['club', null], ['club', 20],
             ['club', null], ['club', 21],  ['club', null]],
            // row 5
            [['club', 22], ['club', null], ['club', 23], ['club', null],
             ['club', 24], ['club', null], ['club', 25], ['club', null],
             ['club', 26], ['club', null], ['club', 27]],
            // row 6
            [['club', null], ['club', 28], ['club', null], ['club', 29],
             ['club', null], ['club', 30], ['club', null], ['club', 31],
             ['club', null], ['club', 32],  ['club', null]]
        ];

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
            var goalkeeper_players = data.goalkeeper_players;
            var defender_players = data.defender_players;
            var offender_players = data.offender_players;
            var players = [];
            //console.log('def', defender_players)
            _.each(offender_players, function(player){
                players.push(player.pk);
            });
            _.each(defender_players, function(player){
                players.push(player.pk);
            });
            _.each(goalkeeper_players, function(player){
                players.push(player.pk);
            });
            //console.log(players)
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
                }

                    $scope.workWithData(data);
                self.players.loader = false;
                if (typeof callback === 'function') {
                    callback(callbackArg);
                }
            });
        };

        this.compare = function(arg) {
            //console.log('a')
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
                if (data.leagues.length) {
                    self.clubs.clubs.push({
                        'data': data,
                        'table': {
                            'club': data.leagues[0].clubs
                        },
                        'league': data.leagues[0]
                    });
                }
                self.clubs.loader = false;
                if(arg !== false){

                }
            });
        };

        $scope.makeTransferArrows = function(){
            createTransferArrow('#club_2', '#playerd_3', 1);
            createTransferArrow('#club_4', '#playerd_2', 2);
            $( ".player-item" ).each(function() {
                if($(this).attr('id') !== 'playerd_3' && $(this).attr('id') !== 'playerd_2')
                $( this ).addClass("opacity-30");
            });
        };
        $scope.unMakeTransferArrows = function(){
            $('canvas').remove();
            $( ".player-item" ).each(function() {
                $( this ).removeClass("opacity-30");
            });
        };
        this.list(this.compare, false);

        function canvas_arrow(context, fromx, fromy, tox, toy){
            var headlen = 10;   // length of head in pixels
            var angle = Math.atan2(toy-fromy,tox-fromx);
            context.moveTo(fromx, fromy);
            context.lineTo(tox, toy);
            //context.moveTo(tox, toy);
            context.lineTo(tox-headlen*Math.cos(angle-Math.PI/6),toy-headlen*Math.sin(angle-Math.PI/6));
            context.moveTo(tox, toy);
            context.lineTo(tox-headlen*Math.cos(angle+Math.PI/6),toy-headlen*Math.sin(angle+Math.PI/6));
        }
        function drawArr(c, fromx, fromy, tox, toy){
            //variables to be used when creating the arrow
            var ctx = c;
            var headlen = 10;
            var angle = Math.atan2(toy-fromy,tox-fromx);
            //starting path of the arrow from the start square to the end square and drawing the stroke
            ctx.beginPath();
            ctx.moveTo(fromx, fromy);
            var amount = 0;
            (function myLoop (amount) {
               setTimeout(function () {
                   amount += 0.05; // change to alter duration
                    ctx.lineWidth = 10;
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
                        ctx.lineWidth = 10;
                        ctx.stroke();
                        ctx.fillStyle = "red";

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
                var c = $('<canvas id="'+id+'" />').attr({
                    'width': p.x1 - p.x + 20 ,
                    'height': p.y1 - p.y + 20
                }).css({
                    'position': 'absolute',
                    'left': p.x,
                    'top': p.y,
                    'z-index': 1
                }).appendTo($('body'))[0].getContext('2d');

                // draw line
                var x1 = ofrom.x - p.x ;
                var y1 = ofrom.y - p.y - 30;
                var x2 = oto.x - p.x +20;
                var y2 = oto.y - p.y + 20;
                c.strokeStyle = '#000';
                //c.lineWidth = 20;
                c.beginPath();
                 /*c.moveTo(x1,y1 );
                 c.lineTo(x2,y2 );
                c.moveTo(x2, y2);
                c.rotate(Math.PI /2)
                c.lineTo(x2+20, y2);*/
                drawArr(c, x1,y1,x2,y2,1,2)
                //canvas_arrow(c,x1,y1,x2,y2)
                c.stroke();
        }
    }
]);
