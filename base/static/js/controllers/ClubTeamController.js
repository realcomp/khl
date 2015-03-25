angular.module('Sportomatics').controller('ClubTeamController', [
    '$http', '$scope',
    function($http, $scope) {
        var self = this,
        url = $('#ClubTeamForm').attr('action'),
        popup = null;

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
            console.log('def', defender_players)
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

        self.list = function(callback) {
            var params = $('#ClubTeamForm').serialize();
            self.players.data = null;
            self.players.table = null;
            self.players.loader = true;
            self.clubs.clubs = [];
            $http.get(url + '?' + params)
            .success(function(data) {
                    $scope.workWithData(data);
                    $scope.players = data;
                self.players.data = data;
                self.players.table = {
                    'goalkeeper': data.goalkeeper_players,
                    'defender': data.defender_players,
                    'forward': data.offender_players,
                    'trainer': data.coaches
                }
                self.players.loader = false;
                if (typeof callback === 'function') {
                    callback();
                }
            });
        };

        this.compare = function() {
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
            });
        };

        this.list(this.compare);
    }
]);
