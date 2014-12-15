#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.db.models.loading import get_model

from .utils import GetPlayerInfo


CUR_APP = 'hockeyapp' #TODO: remove this


class PlayerManager(models.Manager):
    b''' Менджер игрока '''
    def get_or_create_player(self, khl_id, ru_fio=''):
        b''' получаем игрока по id со стороннего ресурса '''
        _player, _crt = self.get_or_create(khl_id=khl_id)
        data=dict()
        if _crt:
            data = GetPlayerInfo().get_page(khl_id)
            data.pop('khl_id', None)
            for k,v in data.items():
                if not v:
                    data.pop(k, None)
        if not data.get('ru_fio') and ru_fio:
            data['ru_fio'] = ru_fio 
        if data:
            self.filter(pk=_player.pk).update(**data)
        return _player


class ManagerMixin(object):
    def _get_players(self, khl_ids):
        b''' получить список игроков '''
        return [self._get_player(khl_id) for khl_id in khl_ids]

    def _get_player(self, khl_id, ru_fio=''):
        b''' получить игрока '''
        model = get_model(CUR_APP, 'Player')
        return model.objects.get_or_create_player(khl_id=khl_id, ru_fio=ru_fio)

    def _get_clubplayers(self, lst, club):
        b''' получить список клубных игроков '''
        return [self._get_clubplayer(data, club) for data in lst]

    def _get_clubplayer(self, data, club):
        b''' получить клубного игрока '''
        _player = self._get_player( data.pop('khl_id', None),
                                    ru_fio=data.pop('ru_fio', '')
        )
        model = get_model(CUR_APP, 'ClubPlayer')
        return model.objects.get_or_create( club=club,
                                            player=_player,
                                            **data)[0]


class MatchGoalHistoryManager(ManagerMixin, models.Manager):
    b''' Мененжер истории голов матча '''
    def create_goal(self, match, **goal_data):
        _assist = self._get_players(goal_data.pop('assist',[]))
        _scorer = self._get_player(goal_data.pop('scorer'))
        entry = self.create(match=match,
                            scorer=_scorer,
                            **goal_data)
        entry.assist.add(*_assist)
        #entry.home_five.add(*_home_five)
        #entry.guest_five.add(*_guest_five)

class MatchPenaltyHistoryManager(ManagerMixin, models.Manager):
    b''' Мененжер истории нарушений матча '''
    def create_penalty(self, match, **penalty_data):
        _player = self._get_player(penalty_data.pop('player'))
        self.create(match=match, player=_player, **penalty_data)


class MatchManager(ManagerMixin, models.Manager):
    b''' Мененжер матчей по-умолчанию '''
    def get_or_create_match(self, **kwargs):
        b''' метод взять или создать запись о матче '''
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
        }
        match, _crt = self.get_or_create(khl_id = kwargs.get('khl_id'))
        match.judges.add(*(j[0].pk for j in _match.get('judges')))
        match.line_judges.add(*(j[0].pk for j in _match.get('line_judges')))
        match.home_players.add(*self._get_clubplayers(
                                                    _match.get('home_players'),
                                                    _match.get('home_team')
        ))
        match.guest_players.add(*self._get_clubplayers(
                                                    _match.get('guest_players'),
                                                    _match.get('guest_team')
        ))
        kwargs['home_team']=_match.get('home_team')
        kwargs['home_coach']=_match.get('home_coach')
        kwargs['guest_team']=_match.get('guest_team')
        kwargs['guest_coach']=_match.get('guest_coach')
        self.filter(pk=match.pk).update(**kwargs)
        self._create_match_history(match, match_data=_match)
        return match

    def _create_match_history(self, match, match_data=None):
        b''' создаем историю матча '''
        match_data = match_data or {}
        self._create_goalmatchhistory(match, match_data.get('goals_history'))
        self._create_penaltymatchhistory(match, match_data.get('penalties_history'))

    def _create_goalmatchhistory(self, match, goals_history=None):
        goals_history = goals_history or ()
        model = get_model(CUR_APP, 'MatchGoalHistory')
        for goal in goals_history:
            model.objects.create_goal(match=match,**goal)

    def _create_penaltymatchhistory(self, match, penalties_history=None):
        penalties_history = penalties_history or ()
        model = get_model(CUR_APP, 'MatchPenaltyHistory')
        for penalty in penalties_history:
            model.objects.create_penalty(match=match,**penalty)

    def _get_coach(self, coach_ru_fio=''):
        b''' получить тренера '''
        model = get_model(CUR_APP, 'Coach')
        return model.objects.get_or_create(ru_fio=coach_ru_fio)[0]

    def _get_team(self, **kwargs):
        b''' получить команду '''
        _region = kwargs.pop('region', None)
        _coach = kwargs.pop('coach', None)
        _players = kwargs.pop('players', None)
        if _region:
            model = get_model('addresses', 'Address')
            _region, _crt = model.objects.get_or_create(ru_title=_region)
            kwargs['address'] =_region
        if _coach:
            kwargs['coach'] = self._get_coach(_coach)
        model = get_model(CUR_APP, 'club')
        _club, _crt = model.objects.get_or_create(**kwargs)
        if _players:
            _khlids = [p.get('khl_id') for p in _players]
            _club.players.add(*self._get_players(_khlids))
        return _club

    def _get_judges(self, judges=None):
        b''' получить судей '''
        judges = judges or []
        model = get_model(CUR_APP, 'Judge')
        return (model.objects.get_or_create(ru_fio=j) for j in judges)