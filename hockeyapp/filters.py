# -*- coding: utf-8 -*-
import json
import operator

from django.db.models import Q

from rest_framework import filters

from base.models import Season

from .models import ClubPlayer


class OrderFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        if 'order_by' in request.GET:
            field = request.GET['order_by']
            reverse = field.startswith('-')
            lc = request.LANGUAGE_CODE
            is_array = (
                field.lstrip('-').startswith('[') and
                field.endswith(']'))
            if is_array:
                fields = json.loads(field.lstrip('-'))
            else:
                fields = [field.lstrip('-')]
            fields = map(
                lambda f: ('-' if reverse else '') + (f % lc if '%s' in f else f),
                fields)
            return qs.order_by(*fields)
        return qs


class PlayersSearchOrderFilter(OrderFilter):
    def filter_queryset(self, request, qs, view):
        if request.GET.get('order_by', '').lstrip('-') == 'rating':
            field = request.GET['rated_by']
            reverse = request.GET.get('order_by', '').startswith('-')
            return qs.order_by('%s%s' % ('-' if reverse else '', field))
        else:
            return super(PlayersSearchOrderFilter, self).filter_queryset(
                request, qs, view)


class PlayersSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        clubplayers = ClubPlayer.objects.all()

        if 'season' in request.GET:
            clubplayers = clubplayers.by_season(self.request.GET['season'])
        elif 'is_playing' in request.GET:
            clubplayers = clubplayers.by_season(
                Season.objects.latest('start_date'))

        if 'league' in request.GET:
            leagues = request.GET.getlist('league')
            clubplayers = clubplayers.filter(league__in=leagues)
            players = clubplayers.values_list('player_id', flat=True)
            qs = qs.filter(pk__in=players)

        if 'club' in request.GET:
            clubplayers = clubplayers.filter(club=request.GET['club'])
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

        return qs
