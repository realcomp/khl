# -*- coding: utf-8 -*-
import json

from django.db.models import Q

from rest_framework import filters

from base.models import Season


class OrderFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        qs = self.ordering_queryset(request, qs, view)
        return qs

    def ordering_queryset(self, request, qs, view):
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
        q = Q()
        _season = request.GET.get('season')
        _club = request.GET.get('club')
        _is_playing = 'is_playing' in request.GET

        if _season:
            q &= Q(clubplayer__season=_season)
        elif _is_playing:
            q &= Q(clubplayer__season=Season.objects.latest('start_date'))

        _leagues = request.GET.getlist('league')
        if _leagues:
            q &= Q(clubplayer__league__in=_leagues)

        _lines = request.GET.getlist('line')
        if _lines:
            q &= Q(line__in=_lines)

        if _club:
            if _is_playing:
                q &= Q(club=_club)
            else:
                q &= Q(clubplayer__club=_club)
        _qs = qs.filter(q)

        _citizenships = request.GET.getlist('citizenship')
        q_citizenships = Q()
        if _citizenships:
            q_citizenships |= Q(citizenship__in=_citizenships)
        if 'citizenship_other' in request.GET:
            q_citizenships |= ~Q(citizenship__ru_title=b'Россия')
        if q_citizenships: _qs = _qs.filter(q)

        _s = request.GET.get('%s_lastname__startswith')
        if _s:
            _qs = _qs.filter(**{
                '{}_lastname__startswith'.format(request.LANGUAGE_CODE): _s,
            })

        _pk = request.GET.get('player')
        if _pk:
            _pk = int(_pk)
            _qs = _qs.ranged_filter(lambda player: player.pk == _pk, 5)

        qs_ids = set(_qs.values_list('pk', flat=True))
        return qs.filter(pk__in=qs_ids)