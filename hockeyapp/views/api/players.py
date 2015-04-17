from . import NumbersList
from ...serializers.players import PlayerNumbersSerializer


class PlayerNumbers(NumbersList):
    serializer_class = PlayerNumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _player = self.request.GET.get('player')
        if _player:
            qs = qs.filter(player=_player)

        _season = self.request.GET.get('season')
        if _season:
            qs = qs.filter(season=_season)

        clubs_by_number = {}
        for clubplayer in qs.order_by('season__start_date'):
            club = clubplayer.club
            number = clubplayer.number
            season = clubplayer.season
            if number not in clubs_by_number:
                clubs_by_number[number] = {
                    'clubs': [],
                    'number': int(number or 0),
                }
            if club in clubs_by_number[number]['clubs']:
                i = clubs_by_number[number]['clubs'].index(club)
                c = clubs_by_number[number]['clubs'][i]
                if not hasattr(c, 'seasons'):
                    c.seasons = []
                if season not in c.seasons:
                    c.seasons.append(season)
            else:
                clubs_by_number[number]['clubs'].append(club)

        return sorted(clubs_by_number.values(), key=lambda x: x['number'])
