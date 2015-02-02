# -*- coding: utf-8 -*-
import json
import operator

from django.db.models import Q

from rest_framework import filters

from base.models import Season

from .models import Club, ClubPlayer, LeagueClub


class PlayersSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        clubplayers = ClubPlayer.objects.all()

        if 'season' in request.GET:
            season = request.GET['season']
        else:
            season = Season.objects.latest('start_date')
        clubplayers = clubplayers.filter(season=season)

        if 'league' in request.GET:
            leagues = request.GET.getlist('league')
            clubs = (
                LeagueClub.objects
                .filter(season=season)
                .filter(league__in=leagues)
                .values_list('club_id', flat=True))
            clubplayers = clubplayers.filter(club__in=clubs)
            players = clubplayers.values_list('player_id', flat=True)
            qs = qs.filter(pk__in=players)

        if 'line' in request.GET:
            # union of sets
            lines = reduce(operator.or_, map(set, map(
                json.loads, request.GET.getlist('line'))))
            qs = qs.filter(line__in=lines)

        q_citizenship = None
        if 'citizenship' in request.GET:
            citizenship = filter(None, request.GET.getlist('citizenship'))
            if citizenship:
                q = Q(citizenship__in=citizenship)
                q_citizenship = (q_citizenship | q) if q_citizenship else q
        if ('citizenship_other' in request.GET and
                'citizenship_other_active' in request.GET):
            citizenship_other = filter(
                None, request.GET.getlist('citizenship_other'))
            if citizenship_other:
                q = Q(citizenship__in=citizenship_other)
            else:
                q = ~Q(citizenship__ru_title=b'Россия')
            q_citizenship = (q_citizenship | q) if q_citizenship else q
        if q_citizenship:
            qs = qs.filter(q_citizenship)

        # get clubs
        club_players2 = (
            ClubPlayer.objects
            .filter(player__in=qs)
            .order_by('-end_date')
            .values_list('player_id', 'club_id'))
        clubs_q = Q()
        if club_players2:
            clubs_q |= Q(pk__in=zip(*club_players2)[1])
        clubs = {
            club.pk: club for club in Club.objects.filter(clubs_q)}
        view.players_clubs = {}
        for player_id, club_id in filter(
                lambda x: x[1], club_players2):
            if player_id not in view.players_clubs:
                view.players_clubs[player_id] = []
            if clubs[club_id] not in view.players_clubs[player_id]:
                view.players_clubs[player_id].append(clubs[club_id])
        return qs
