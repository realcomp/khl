(function() {
    var app = angular.module('SportomaticsClubsTeam', []);

    app.controller('ClubTeamController', ['$http', '$scope', function($http, $scope) {
        var self = this,
        url = $('#ClubTeamForm').attr('action');

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
             ['trainer', null], ['trainer', 0], ['trainer', null], ['trainer', 1],
             ['trainer', null], ['trainer', 2], ['trainer', null],
             ['goalkeeper', 2]],
            // row 6
            [['defender', null], ['defender', 10], ['defender', null],
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

        self.players = {
            'getPreviousSeason': function(season) {
                var i;
                for (i = 0; i < this.data.seasons.length; i++) {
                    if (this.data.seasons[i].pk === season.pk) {
                        return this.data.seasons[i + 1];
                    }
                }
            }
        };
        self.clubs = {
            'getLastClub': function() {
                if (this.clubs.length) {
                    return this.clubs[this.clubs.length - 1];
                }
            },
            'clubs': []
        }

        $scope.setSeason = function(e) {
            self.list(self.compare);
        }

        self.getCell = function(table, cell_id) {
            if (table.table && cell_id && Array.isArray(cell_id)) {
                row = table.table[cell_id[0]];
                if (row) {
                    return table.table[cell_id[0]][cell_id[1]];
                }
            }
        }

        self.isVisible = function(table, cell_id) {
            var cell = this.getCell(table, cell_id);
            switch (self.players.status) {
                default:
                    return true;
                case 'joined':
                    return person.is_joined;
                case 'left':
                    return person.is_left;
                case 'legionnaire':
                    return person.is_legionnaire;
            }
        };

        self.list = function(callback) {
            var params = $('#ClubTeamForm').serialize();
            self.players.data = null;
            self.players.table = null;
            self.players.loader = true;
            self.clubs.clubs = [];
            $http.get(url + '?' + params)
            .success(function(data) {
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
            params = 'season=' + self.players.data.season.pk,
            club = self.clubs.getLastClub();
            if (club) {
                params += '&prev_season=' + self.players.getPreviousSeason(club.data.prev_season).pk;
            } else {
                params += '&prev_season=' + self.players.data.prev_season.pk;
            }
            self.clubs.loader = true;
            $http.get(url + '?' + params)
            .success(function(data) {
                self.clubs.clubs.push({
                    'data': data,
                    'league': 'khl',
                    'table': {
                        'club': data.clubs
                    }
                });
                self.clubs.loader = false;
            });
        };

        this.list(this.compare);
    }]);

})();
