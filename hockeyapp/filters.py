# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.db.models import Q

from rest_framework import filters

from base.models import Season


class OrderFilter(filters.BaseFilterBackend):
    ORDER_FIELDS = (
        '%s_lastname',
        '%s_name',
        'last_club__%s_title',
        'birth_date',
        'contract_to',
        'matches_total',
        'address__%s_title',
        '%s_title',
        'arena__%s_title',
        'coach__%s_fio',
        'seasons_total',
        'matches_total',
        'goals_total',
        'assists_total',
        'points_total',
        'penalty_time_total',
        'plus_minus_total',
        'goals_average',
        'assists_average',
        'points_average',
        'penalty_time_average',
        'plus_minus_average',
    )

    def filter_queryset(self, request, qs, view):
        qs = self.ordering_queryset(request, qs, view)
        return qs

    def ordering_queryset(self, request, qs, view):
        if 'order_by' in request.GET:
            reverse = request.GET.get('reversed', 'false') == 'true'
            lc = request.LANGUAGE_CODE
            if lc not in zip(*settings.LANGUAGES)[0]:
                lc = 'en'
            fields = (
                ('-' if reverse else '') + (f % lc if '%s' in f else f)
                for f in request.GET['order_by'].split(',')
                if f in self.ORDER_FIELDS)
            return qs.order_by(*fields)
        return qs


class PlayersSearchOrderFilter(OrderFilter):
    def filter_queryset(self, request, qs, view):
        if request.GET.get('order_by', '') == 'rating':
            field = request.GET['rated_by']
            reverse = request.GET.get('reversed', 'false') == 'true'
            if field in self.ORDER_FIELDS:
                return qs.order_by('%s%s' % ('-' if reverse else '', field))
            else:
                return qs
        else:
            return super(PlayersSearchOrderFilter, self).filter_queryset(
                request, qs, view)


class PlayersSearchFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, qs, view):
        q = Q()
        _season = request.GET.get('season')
        _club = request.GET.get('club')
        _is_playing = request.GET.get('is_playing')
        _number = request.GET.get('number')
        _contract_type = request.GET.get('contract_type')
        _contract_to = request.GET.get('contract_to')
        _height = request.GET.get('height')
        _weight = request.GET.get('weight')
        _grip = request.GET.get('grip')

        if _season:
            q &= Q(clubplayer__season=_season)
        elif _is_playing:
            q &= Q(clubplayer__season=Season.objects.latest('start_date'))

        if _number:
            q &= Q(clubplayer__number=_number)

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

        if _contract_type:
            _qs = _qs.filter(contract_type=_contract_type)

        if _contract_to:
            _qs = _qs.filter(contract_to__lte=datetime.datetime.strptime(
                _contract_to, '%Y-%m-%d').date())

        if _height and _height.isdigit():
            _qs = _qs.filter(height__gte=_height)

        if _weight and _weight.isdigit():
            _qs = _qs.filter(weight__gte=_weight)

        if _grip:
            _qs = _qs.filter(grip=_grip)

        # _pk = request.GET.get('player')
        # if _pk:
        #     _pk = int(_pk)
        #     _qs = _qs.ranged_filter(lambda player: player.pk == _pk, 5)

        qs_ids = set(_qs.values_list('pk', flat=True))
        return qs.filter(pk__in=qs_ids)
