# -*- coding: utf-8 -*-
from rest_framework import generics

from . import NumbersList
from ...models import ClubPlayer
from ...serializers.clubs import NumbersSerializer, BestPlayersSerilizer


class PlayerNumbers(NumbersList):
    serializer_class = NumbersSerializer

    def filter_queryset(self, qs):
        qs = super(PlayerNumbers, self).filter_queryset(qs)

        _club = self.request.GET.get('club')
        if _club:
            qs = qs.filter(club=_club)

        _season = self.request.GET.get('season')
        if _season:
            qs = qs.filter(season=_season)

        players_by_number = {}
        for clubplayer in qs.order_by('-season__start_date'):
            player = clubplayer.player
            number = clubplayer.number
            if number not in players_by_number:
                players_by_number[number] = {
                    'players': [],
                    'number': int(number or 0),
                }
            if player in players_by_number[number]['players']:
                i = players_by_number[number]['players'].index(player)
                p = players_by_number[number]['players'][i]
                if clubplayer not in p.clubplayers:
                    p.clubplayers.append(clubplayer)
            else:
                player.clubplayers = []
                player.clubplayers.append(clubplayer)
                players_by_number[number]['players'].append(player)

        return sorted(players_by_number.values(), key=lambda x: x['number'])


class BestPlayers(generics.ListAPIView):
    '''
    Best players of the club
    '''
    queryset = ClubPlayer.objects.all()
    serializer_class = BestPlayersSerilizer

    def filter_queryset(self, qs):
        qs = super(BestPlayers, self).filter_queryset(qs)
        qs = qs.filter(club=self.kwargs['club_id'])

        return qs
