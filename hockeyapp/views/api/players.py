from . import NumbersList
from ...serializers.players import NumbersSerializer


class PlayerNumbers(NumbersList):
    serializer_class = NumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _player = self.request.GET.get('player')
        if _player:
            qs = qs.filter(player=_player)

        _season = self.request.GET.get('season')
        if _season:
            qs = qs.filter(season=_season)

        clubs_by_number = {}
        for clubplayer in qs.order_by('-season__start_date'):
            club = clubplayer.club
            number = clubplayer.number
            if number not in clubs_by_number:
                clubs_by_number[number] = {
                    'clubs': [],
                    'number': int(number or 0),
                }
            if club in clubs_by_number[number]['clubs']:
                i = clubs_by_number[number]['clubs'].index(club)
                c = clubs_by_number[number]['clubs'][i]
                if clubplayer not in c.clubplayers:
                    c.clubplayers.append(clubplayer)
            else:
                club.clubplayers = []
                club.clubplayers.append(clubplayer)
                clubs_by_number[number]['clubs'].append(club)

        return sorted(clubs_by_number.values(), key=lambda x: x['number'])
