# -*- coding: utf-8 -*-
import datetime
import operator

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
        'address__city__%s_title',
        '%s_title',
        'arena__%s_title',
        'coach__%s_fio',
        'coach__%s_name',
        'coach__%s_lastname',
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
        'number',
        'club',
        'height',
        'weight',
        'grip',
        'birth_date',
        'ev_goals_total',
        'pp_goals_total',
        'es_goals_total',
        'overtime_goals_total',
        'win_goals_total',
        'bullet_goals_total',
        'shots_total',
        'pis_average',
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
        _is_playing = request.query_params.get('is_playing') != 'false'
        _number = request.query_params.get('number')
        _contract_type = request.query_params.get('contract_type')
        _contract_types = request.query_params.getlist('contract_types')
        _contract_to = request.query_params.get('contract_to')
        _height = request.query_params.get('height')
        _height__gte = request.query_params.get('height__gte')
        _height__lte = request.query_params.get('height__lte')
        _weight = request.query_params.get('weight')
        _weight__gte = request.query_params.get('weight__gte')
        _weight__lte = request.query_params.get('weight__lte')
        _grip = request.query_params.getlist('grip')
        _contract_type__isnull = request.query_params.get('contract_type__isnull', '').lower() == 'true'
        _age__gte = request.query_params.get('age__gte')
        _age__lte = request.query_params.get('age__lte')
        _related_field = request.query_params.get('related_field')
        _related_player = request.query_params.get('related_player')
        _related_value__lte = request.query_params.get('related_value__lte')
        _related_value__gte = request.query_params.get('related_value__gte')
        _match_count = request.query_params.get('match_count')
        _gamingtime = request.query_params.get('gamingtime')
        _player_id = request.query_params.get('player')
        _leagues = request.query_params.getlist('league')
        _lines = request.query_params.getlist('line')
        _citizenships = request.query_params.getlist('citizenship')
        _fio = request.query_params.get('fio')

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
            # q &= Q(clubplayer__number=_number)
            q &= Q(number=_number)

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
        if _height__gte and _height__gte.isdigit():
            q &= Q(height__gte=_height__gte)
        if _height__lte and _height__lte.isdigit():
            q &= Q(height__lte=_height__lte)

        if _weight and _weight.isdigit():
            q &= Q(weight__gte=_weight)
        if _weight__gte and _weight__gte.isdigit():
            q &= Q(weight__gte=_weight__gte)
        if _weight__lte and _weight__lte.isdigit():
            q &= Q(weight__lte=_weight__lte)

        if _grip:
            q &= Q(grip__in=_grip)

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
                q &= Q(contract_to__gte=date)

        if _age__gte and _age__gte.isdigit():
            date = datetime.datetime.now() - relativedelta(
                years=int(_age__gte))
            q &= Q(birth_date__lte=date)

        if _age__lte and _age__lte.isdigit():
            date = datetime.datetime.now() - relativedelta(
                years=int(_age__lte))
            q &= Q(birth_date__gte=date)

        if _related_player and _related_field in (
                'goals_value', 'assists_value', 'points_value',
                'penalty_time_value', 'plus_minus_value'):

            def get_q(field, value, player, cmp_):
                '''
                player2 -> relatedplayers2 -> player1
                player1 -> relatedplayers1 -> player2
                '''
                return operator.or_(*(Q(**{
                    'relatedplayers%d__%s__%s' % (x, field, cmp_): value,
                    'relatedplayers%d__player%d' % (x, y): player,
                }) for x, y in ((1, 2), (2, 1))))

            if _related_value__lte and _related_value__lte.isdigit():
                value = int(_related_value__lte) / 100.0
                q &= get_q(_related_field, value, _related_player, 'lte')
            if _related_value__gte and _related_value__gte.isdigit():
                value = int(_related_value__gte) / 100.0
                q &= get_q(_related_field, value, _related_player, 'gte')

        if _match_count and _match_count.isdigit():
            q &= Q(matches_total__gte=_match_count)

        if _gamingtime and _gamingtime.isdigit():
            q &= Q(gamingtime_total__gte=_gamingtime)

        if _fio:
            lang = request.LANGUAGE_CODE
            # exclude empty strings
            for name in filter(None, _fio.split(' ')):
                q &= (
                    Q(**{'{}_name__icontains'.format(lang): name}) |
                    Q(**{'{}_lastname__icontains'.format(lang): name}))

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
