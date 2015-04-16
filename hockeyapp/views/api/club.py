from . import NumbersList
from ...serializers.players import ClubPlayerNumbersSerializer


class PlayerNumbers(NumbersList):
    serializer_class = ClubPlayerNumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _club = self.request.GET.get('club')
        if _club:
            qs = qs.filter(club=_club)

        players_by_number = {}
        for clubplayer in qs.order_by('season__start_date'):
            player = clubplayer.player
            number = clubplayer.number
            if number not in players_by_number:
                players_by_number[number] = {
                    'players': [],
                    'number': int(number or 0),
                }
            if player not in players_by_number[number]['players']:
                players_by_number[number]['players'].append(player)

        return sorted(players_by_number.values(), key=lambda x: x['number'])
