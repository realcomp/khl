# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import copy

from django.db.models import Q, Sum
from django.utils.translation import ugettext_lazy as _

from rest_framework import generics

from base.models import Season

from . import NumbersList
from ...models import ClubPlayer, Match
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
        _club = self.kwargs['club_id']

        qs = qs.filter(
            season=_season or Season.objects.get_current_season(),
            club=_club)

        classes_init = [{
            # Бомбардир - максимальное кол-во очков (Ш+А)
            'class': _('Bombardier'),
            'field': 'points',
            'label': _('points'),
        }, {
            # Снайпер - максимальное кол-во шайб (Ш)
            'class': _('Sniper'),
            'field': 'goals',
            'label': _('goals'),
        }, {
            # Плюс/Минус - максимальный +/-
            'class': _('Plus/Minus'),
            'field': 'plus_minus',
            'label': _('points'),
        }, {
            # Ассистент - максимальное кол-во очков (О)
            'class': _('Assistant'),
            'field': 'assists',
            'label': _('points'),
        }, {
            # Штраф - максимальное штрафное время (Ш)
            'class': _('Penalty'),
            'field': 'penalty_time',
            'label': _('minutes'),
        }, {
            # Вратарь - максимальное кол-во отраженных бросков (%ОБ)
            'class': _('Goalkeeper'),
            'field': 'saves',
            'label': _('saved shots'),
        }]

        def calc_class(class_, q=None):
            c = copy.copy(class_)
            field_total = '%s__total' % c['field']
            cps = qs
            if q:
                cps = cps.filter(q)
            # cps = (
            #     cps
            #     .filter(**{'%s__isnull' % field: False})
            #     .annotate(**{field_total: Sum(field)})
            #     .order_by(field_total))
            # last_cp = cps.last()
            cp_values = {
                cp: cp.clubplayermatch_set.is_active().aggregate(**{field_total: Sum(c['field'])}).get(field_total, 0) or 0
                for cp in cps
            }
            if cp_values:
                last_cp, value = sorted(
                    cp_values.items(), key=lambda x: x[1])[-1]
                # if c['field'] == 'penalty_time':
                #     value /= 60
                c.update({
                    'player': last_cp.player,
                    'value': value,
                    'count': last_cp.clubplayermatch_set.is_active().count(),
                })
                return c

        classes = list(map(calc_class, classes_init))

        # Бомбардир-защитник - защитник, с максимальным кол-вом очков (Ш+А)
        classes.append(calc_class({
            'class': _('Bombardier-Defender'),
            'field': 'points',
            'label': _('points'),
         }, q=Q(line=2)))

        # Железный человек - игрок (кроме вратаря),
        # поучаствовавший во всех матчах сезона
        cp = qs.filter(
            clubplayermatch__match__isnull=False,
            clubplayermatch__match__challenge_type__isnull=False,
            clubplayermatch__match__challenge_type__gt=0)

        matches_count = (
            Match.objects
            .filter(Q(home_team=_club) | Q(guest_team=_club))
            .filter(challenge_type__isnull=False, challenge_type__gt=0)
            .filter(clubplayermatch__clubplayer__season=_season)
            .distinct('pk')
            .count())
        cp_values = {
            cp: cp.clubplayermatch_set.is_active().count()
            for cp in qs.exclude(line=1)
        }
        if cp_values:
            last_cp, value = sorted(
                cp_values.items(), key=lambda x: x[1])[-1]
            classes.append({
                'class': _('Ironman'),
                'player': last_cp.player,
                'value': value,
                'label': _('matches'),
                'count': matches_count,
            })

        return classes
