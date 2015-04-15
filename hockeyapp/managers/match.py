#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models
from django.db.models import F, Q, Max, Min
from django.db.models.loading import get_model

from base.models import Season

from ..utils import month_range


CURRENT_APP = __package__.split('.')[0]

class ManagerMixin(object):
    def _get_players(self, khl_ids):
        b''' получить список игроков '''
        return [self._get_player(khl_id) for khl_id in khl_ids if khl_id]

    def _get_player(self, khl_id, fio='', update=False):
        b''' получить игрока '''
        model = get_model(CURRENT_APP, 'Player')
        return model.objects.get_or_create_player(  khl_id=khl_id, 
                                                    fio=fio,
                                                    update=update)

    def _get_clubplayers(self, lst, club, match=None):
        b''' получить список клубных игроков '''
        return [self._get_clubplayer(data, club, match) for data in lst]

    def _get_clubplayer(self, data, club, match=None):
        b''' получить клубного игрока '''
        _player = self._get_player( data.pop('khl_id', None),
                                    fio=data.pop('fio', ''),
                                    #update=True,
        )
        model = get_model(CURRENT_APP, 'ClubPlayer')
        data.update(self._season)
        stats = data.pop('stats', None)
        adv_stats = data.pop('adv_stats', None)
        _clubplayers = model.objects.filter(club=club, player=_player, **data)
        _clubplayer = _clubplayers.order_by('pk').first()
        if not _clubplayer:
            _clubplayer = model.objects.create(club=club, player=_player,**data)
        if match and _clubplayer and stats:
            cpm = self._create_clubplayer_stats(match=match, data=stats,
                                                clubplayer=_clubplayer)
            if cpm and adv_stats:
                _update = cpm.adv_stats
                self._create_clubplayer_adv_stats(cpm, adv_stats, _update)
        return _clubplayer

    def _create_clubplayer_stats(self, match=None, clubplayer=None, data=None):
        b''' Создание общей статистики игрока в матче '''
        model = get_model(CURRENT_APP, 'ClubPlayerMatch')
        obj = model.objects.filter(match=match, clubplayer=clubplayer).last()
        if obj:
            model.objects.filter(pk=obj.pk).update(**data)
            return obj
        else:
            data['match'] = match
            data['clubplayer'] = clubplayer
            return model.objects.create(**data)

    def _create_clubplayer_adv_stats(self, clubplayermatch=None, data=None,
                                    update=False):
        b''' Создание  дополнительной статистики игрока в матче '''
        model = get_model(CURRENT_APP, 'AdvancedPlayerStats')
        if update:
            model.objects.filter(pk=clubplayermatch.adv_stats.pk).update(**data)
        else:
            obj = model.objects.create(**data)
            clubplayermatch.adv_stats = obj
            clubplayermatch.save(update_fields=['adv_stats'])


class MatchFKQuerySetMixin(object):
    def by_club(self, club, player):
        q_home = Q(
            match__home_team=club,
            match__home_players__player=player)
        q_guest = Q(
            match__guest_team=club,
            match__guest_players__player=player)
        return self.is_active().filter(q_home | q_guest)

    def is_active(self):
        b'''Запись, которую необходимо учитывать при подсчете статистики'''
        return self.filter( match__isnull=False,
                            match__challenge_type__isnull=False,
                            match__challenge_type__gt=0)


class MatchGoalHistoryQuerySet(
        MatchFKQuerySetMixin, ManagerMixin, models.QuerySet):
    b''' Мененжер истории голов матча '''
    def create_goal(self, match, **goal_data):
        b''' Создаем запись в БД о голе '''
        _assist = self._get_players(goal_data.pop('assist',[]))
        _scorer = self._get_player(goal_data.pop('scorer'))
        goal_data['match'] = match
        goal_data['scorer'] = _scorer
        entry = self.filter(**goal_data).last()
        if not entry:
            entry = self.create(**goal_data)
        entry.assist.add(*_assist)
        #entry.home_five.add(*_home_five)
        #entry.guest_five.add(*_guest_five)


class MatchPenaltyHistoryManager(ManagerMixin, models.Manager):
    b''' Мененжер истории нарушений матча '''
    def create_penalty(self, match, **penalty_data):
        b''' Создаем запись в БД о нарушении '''
        _player = penalty_data.pop('player', None)
        if _player:
            _player = self._get_player(_player)
            penalty_data['match'] = match
            penalty_data['player'] = _player
            if not self.filter(**penalty_data):
                self.create(**penalty_data)


class MatchManager(ManagerMixin, models.Manager):
    b''' Мененжер матчей по-умолчанию '''
    def active(self):
        b'''Запись, которую необходимо учитывать при подсчете статистики'''
        return self.filter( challenge_type__isnull=False,
                            challenge_type__gt=0)

    def get_or_create_match(self, **kwargs):
        b''' метод взять или создать запись о матче '''
        self._season = kwargs.pop('season', {})
        sm = get_model('base', 'Season')
        sm = sm.objects.get_or_create_season
        self._season['season'], _crt = sm(**self._season)
        _scheduler = self._get_scheduled_match(kwargs.get('khl_id'))
        _match = {
                'home_team': self._get_team(**kwargs.pop('home_team', {})),
                'home_coach': self._get_coach(kwargs.pop('home_coach', {})),
                'home_players': kwargs.pop('home_players', None),
                'guest_team': self._get_team(**kwargs.pop('guest_team', {})),
                'guest_coach': self._get_coach(kwargs.pop('guest_coach', {})),
                'guest_players': kwargs.pop('guest_players', None),
                'judges': self._get_judges(kwargs.pop('judges', None)),
                'line_judges': self._get_judges(kwargs.pop('line_judges', None)),
                'goals_history': kwargs.pop('goals_history', {}),
                'penalties_history': kwargs.pop('penalties_history', {}),
                'schedule': _scheduler,
        }
        kwargs['home_team']=_match.get('home_team')
        kwargs['home_coach']=_match.get('home_coach')
        kwargs['guest_team']=_match.get('guest_team')
        kwargs['guest_coach']=_match.get('guest_coach')
        kwargs['challenge_type']=_scheduler and _scheduler.challenge_type
        match = self.filter(khl_id = kwargs.get('khl_id')).last()
        if match:
            self.filter(pk=match.pk).update(**kwargs)
        else:
            match = self.create(**kwargs)
        if _scheduler:
            _scheduler.processed=True
            _scheduler.match = match
            match.schedule.save(update_fields=['processed', 'match'])
        #relations
        match.judges.add(*(j[0].pk for j in _match.get('judges')))
        match.line_judges.add(*(j[0].pk for j in _match.get('line_judges')))
        match.home_players.add(*self._get_clubplayers(
                                                    _match.get('home_players'),
                                                    _match.get('home_team'),
                                                    match = match,
        ))
        match.guest_players.add(*self._get_clubplayers(
                                                    _match.get('guest_players'),
                                                    _match.get('guest_team'),
                                                    match = match,
        ))
        self._create_match_history(match, match_data=_match)
        return match

    def _get_scheduled_match(self, khl_id):
        if khl_id:
            schedule_m = get_model(CURRENT_APP, 'Schedule')
            return schedule_m.objects.filter(khl_id=khl_id).last()

    def _create_match_history(self, match, match_data=None):
        b''' создаем историю матча '''
        match_data = match_data or {}
        self._create_goalmatchhistory(match, match_data.get('goals_history'))
        self._create_penaltymatchhistory(match, match_data.get('penalties_history'))

    def _create_goalmatchhistory(self, match, goals_history=None):
        b''' Создаем по списку записи о голе в матче '''
        goals_history = goals_history or ()
        model = get_model(CURRENT_APP, 'MatchGoalHistory')
        for goal in goals_history:
            model.objects.create_goal(match=match,**goal)

    def _create_penaltymatchhistory(self, match, penalties_history=None):
        b''' Создаем по списку записи о нарушении в матче '''
        penalties_history = penalties_history or ()
        model = get_model(CURRENT_APP, 'MatchPenaltyHistory')
        for penalty in penalties_history:
            model.objects.create_penalty(match=match,**penalty)

    def _get_coach(self, fio=''):
        b''' получить тренера '''
        model = get_model(CURRENT_APP, 'Coach')
        _qs = model.objects.filter(fio=fio)
        return _qs.first() or model.objects.create(fio=fio)

    def _get_team(self, **kwargs):
        b''' получить команду '''
        _region = kwargs.pop('region', None)
        _coach = kwargs.pop('coach', None)
        _players = kwargs.pop('players', None)
        club_model = get_model(CURRENT_APP, 'club')
        _title = kwargs.pop('title', None)
        _club = club_model.objects.by_title_alias(_title).first()
        if not _club:
            kwargs['title'] = _title
            _club, _crt = club_model.objects.get_or_create(**kwargs)
            if _players and _crt:
                _players = [self._get_player(p.get('khl_id'), p.get('fio'),)
                            for p in _players]
                _club.players = set(_players)
        if _region:
            model = get_model('addresses', 'Address')
            _region, _crt = model.objects.get_or_create(title=_region)
            kwargs['address'] =_region
            model = get_model(CURRENT_APP, 'AddressClub')
            model.objects.get_or_create(club=_club, 
                                        address=_region, 
                                        **self._season
            )
        if _coach:
            kwargs['coach'] = self._get_coach(_coach)
            model = get_model(CURRENT_APP, 'CoachClub')
            model.objects.get_or_create(club=_club, 
                                        coach=kwargs['coach'],
                                        **self._season
            )
        club_model.objects.filter(pk=_club.pk).update(**kwargs)
        return _club

    def _get_judges(self, judges=None):
        b''' получить судей '''
        judges = judges or []
        model = get_model(CURRENT_APP, 'Judge')
        return (model.objects.get_or_create(fio=j) for j in judges)


class ClubPlayerMatchQuerySet(MatchFKQuerySetMixin, models.QuerySet):
    X_HOME_WIN = {
        'where': [
            "hockeyapp_match.count ~ '^[0-9]:[0-9]' and "
            "cast(split_part(left(hockeyapp_match.count, 3), ':', 1) as integer) > "
            "cast(split_part(left(hockeyapp_match.count, 3), ':', 2) as integer)"
        ],
    }
    X_GUEST_WIN = {
        'where': [
            "hockeyapp_match.count ~ '^[0-9]:[0-9]' and "
            "cast(split_part(left(hockeyapp_match.count, 3), ':', 1) as integer) < "
            "cast(split_part(left(hockeyapp_match.count, 3), ':', 2) as integer)"
        ],
    }

    # Вообще кверисет должен возвращать кверисет. А там, где нужно убрать дубли,
    # лучше заюзать set(queryset) и циклы, как ниже описаны. Но Queryset должен
    # быть queryset
    def group_by_month(self):
        """
        returns list of QuerySet's
        """
        min_max = self.aggregate(Min('match__date'), Max('match__date'))
        start_date = min_max.get('match__date__min')
        end_date = min_max.get('match__date__max')
        if start_date and end_date:
            self._dates = list(month_range(start_date, end_date))
            return map(self._month_qs, range(len(self._dates) - 1))
        return []

    def _month_qs(self, i):
        month_qs = self.is_active().filter(
            match__date__gt=self._dates[i],
            match__date__lte=self._dates[i + 1])
        month_qs.date = self._dates[i]
        if month_qs.exists():
            month_qs.season = month_qs.first().clubplayer.season
        else:
            month_qs.season = None
        return month_qs

    def group_by_season(self):
        """
        returns list of QuerySet's
        """
        _s_ids = self.values_list('clubplayer__season_id')
        seasons = Season.objects.filter(pk__in=_s_ids).order_by('start_date')
        return map(self._season_qs, seasons)

    def _season_qs(self, season):
        season_qs = self.is_active().filter(clubplayer__season=season)
        min_max = season_qs.aggregate(Min('match__date'),Max('match__date'))
        season_qs.start_date = min_max.get('match__date__min')
        season_qs.end_date = min_max.get('match__date__max')
        season_qs.date = None
        season_qs.season = season
        return season_qs

    def home_matches(self):
        return self.is_active().filter(match__home_team=F('clubplayer__club'))

    def guest_matches(self):
        return self.is_active().filter(match__guest_team=F('clubplayer__club'))

    def home_matches_win(self):
        return self.home_matches().extra(**self.X_HOME_WIN)

    def home_matches_lose(self):
        return self.home_matches().extra(**self.X_GUEST_WIN)

    def guest_matches_win(self):
        return self.guest_matches().extra(**self.X_GUEST_WIN)

    def guest_matches_lose(self):
        return self.guest_matches().extra(**self.X_HOME_WIN)
