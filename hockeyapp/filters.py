# -*- coding: utf-8 -*-
import datetime

from dateutil.relativedelta import relativedelta

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
        if 'order_by' in request.query_params:
            reverse = request.query_params.get('reversed', 'false') == 'true'
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
        if request.query_params.get('order_by', '') == 'rating':
            field = request.GET['rated_by']
            reverse = request.query_params.get('reversed', 'false') == 'true'
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
        _season = request.query_params.get('season')
        _season_start = request.query_params.get('season_start')
        _season_end = request.query_params.get('season_end')
        _clubs = request.query_params.getlist('club')
        _is_playing = request.query_params.get('is_playing')
        _number = request.query_params.get('number')
        _contract_type = request.query_params.get('contract_type')
        _contract_types = request.query_params.getlist('contract_types')
        _contract_to = request.query_params.get('contract_to')
        _height = request.query_params.get('height')
        _weight = request.query_params.get('weight')
        _grip = request.query_params.get('grip')
        _contract_type__isnull = request.query_params.get('contract_type__isnull', '').lower() == 'true'
        _age__lte = request.query_params.get('age__lte')
        _age__gte = request.query_params.get('age__gte')
        _match_count = request.query_params.get('match_count')
        _gamingtime = request.query_params.get('gamingtime')
        _player_id = request.query_params.get('player')
        _leagues = request.query_params.getlist('league')
        _lines = request.query_params.getlist('line')
        _citizenships = request.query_params.getlist('citizenship')

        if _player_id and _player_id.isdigit():
            q &= Q(pk=_player_id)

        if _season:
            q &= Q(clubplayer__season=_season)
        elif _season_start and _season_end:
            q &= Q(
                clubplayer__season__start_date__gte=_season_start,
                clubplayer__season__end_date__lte=_season_end)
        elif _is_playing:
            q &= Q(clubplayer__season=Season.objects.get_current_season())

        if _number:
            q &= Q(clubplayer__number=_number)

        if _leagues:
            q &= Q(clubplayer__league__in=_leagues)

        if _lines:
            q &= Q(line__in=_lines)

        if _clubs:
            if _is_playing:
                q &= Q(club__in=_clubs)
            else:
                q &= Q(clubplayer__club__in=_clubs)

        if _height and _height.isdigit():
            q &= Q(height__gte=_height)

        if _weight and _weight.isdigit():
            q &= Q(weight__gte=_weight)

        if _grip:
            q &= Q(grip=_grip)

        if _contract_type__isnull:
            q &= Q(contract_type__isnull=True)
        else:
            if _contract_type:
                q &= Q(contract_type=_contract_type)
            if _contract_types:
                q &= Q(contract_type__in=_contract_types)
            if _contract_to:
                date = datetime.datetime.strptime(
                    _contract_to, '%Y-%m-%d').date()
                q &= Q(contract_to__lte=date)

        if _age__lte and _age__lte.isdigit():
            date = datetime.datetime.now() - relativedelta(
                years=int(_age__lte))
            q &= Q(birth_date__lte=date)

        if _age__gte and _age__gte.isdigit():
            date = datetime.datetime.now() - relativedelta(
                years=int(_age__gte))
            q &= Q(birth_date__gte=date)

        if _match_count and _match_count.isdigit():
            q &= Q(matches_total__gte=_match_count)

        if _gamingtime and _gamingtime.isdigit():
            q &= Q(gamingtime_total__gte=_gamingtime)

        q_citizenship = Q()
        if _citizenships:
            if 'citizenship_reversed' in request.query_params:
                q_citizenship &= ~Q(citizenship__in=_citizenships)
            else:
                q_citizenship &= Q(citizenship__in=_citizenships)
        if 'citizenship_other' in request.query_params:
            q_citizenship |= ~Q(citizenship__ru_title=b'Россия')
        if q_citizenship:
            q &= q_citizenship

        _qs = qs.filter(q)

        _s = request.query_params.get('%s_lastname__startswith')
        if _s:
            _qs = _qs.filter(**{
                '{}_lastname__startswith'.format(request.LANGUAGE_CODE): _s,
            })
            
        qs_ids = _qs.values_list('pk', flat=True)
        return qs.filter(pk__in=qs_ids)
