# -*- coding: utf-8 -*-
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics

from base.models import Season

from . import NumbersList
from ...models import Player, ClubPlayer
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
        _season = self.request.query_params.get('season')

        qs = qs.filter(
            season=_season or Season.objects.get_current_season(),
            club=self.kwargs['club_id'])

        players = Player.objects.filter(pk__in=qs.values_list('player'))

        class_fields = {
            # Бомбардир - максимальное кол-во очков (Ш+А)
            _('Bombardier'): 'points_total',
            # Снайпер - максимальное кол-во шайб (Ш)
            _('Sniper'): 'goals_total',
            # Плюс/Минус - максимальный +/-
            _('Plus/Minus'): 'plus_minus_total',
            # Ассистент - максимальное кол-во очков (О)
            _('Assistant'): 'assists_total',
            # Штраф - максимальное штрафное время (Ш)
            _('Penalty'): 'penalty_time_total',
            # Вратарь - максимальное кол-во отраженных бросков (%ОБ)
            _('Goalkeeper'): 'saves_total',
        }

        def players_by_class(class_, field, q=None):
            filtered_players = players.filter(**{'%s__isnull' % field: False})
            if q:
                filtered_players = filtered_players.filter(q)
            player = filtered_players.order_by(field).last()
            return {
                'class': class_,
                'player': player,
                'value': getattr(player, field),
                'matches_total': player.matches_total,
            }

        classes = [players_by_class(k, v) for k, v in class_fields.items()]

        # Бомбардир-защитник - защитник, с максимальным кол-вом очков (Ш+А)
        classes.append(players_by_class(
            _('Bombardier-Defender'), 'points_total', q=Q(line=2)))

        # Железный человек - игрок (кроме вратаря),
        # поучаствовавший во всех матчах сезона
        # classes.append ... _('Ironman') ... players.exclude(line=1)

        return classes
