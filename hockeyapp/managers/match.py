#coding: utf-8
from __future__ import unicode_literals, print_function

__author__='smirnov.ev'

from django.db import models
from django.db.models.loading import get_model


CURRENT_APP = __package__.split('.')[0]

class ManagerMixin(object):
    def _get_players(self, khl_ids):
        b''' получить список игроков '''
        return [self._get_player(khl_id) for khl_id in khl_ids if khl_id]

    def _get_player(self, khl_id, ru_fio='', update=False):
        b''' получить игрока '''
        model = get_model(CURRENT_APP, 'Player')
        return model.objects.get_or_create_player(  khl_id=khl_id, 
                                                    ru_fio=ru_fio,
                                                    update=update)

    def _get_clubplayers(self, lst, club, match=None):
        b''' получить список клубных игроков '''
        return [self._get_clubplayer(data, club, match) for data in lst]

    def _get_clubplayer(self, data, club, match=None):
        b''' получить клубного игрока '''
        _player = self._get_player( data.pop('khl_id', None),
                                    ru_fio=data.pop('ru_fio', ''),
                                    #update=True,
        )
        model = get_model(CURRENT_APP, 'ClubPlayer')
        data.update(self._season)
        stats = data.pop('stats', None)
        adv_stats = data.pop('adv_stats', None)
        _clubplayer, _crt = model.objects.get_or_create(club=club,
                                                        player=_player,
                                                        **data)
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

class MatchGoalHistoryManager(ManagerMixin, models.Manager):
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
    def get_or_create_match(self, **kwargs):
        b''' метод взять или создать запись о матче '''
        self._season = kwargs.pop('season', {})
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
        kwargs['home_team']=_match.get('home_team')
        kwargs['home_coach']=_match.get('home_coach')
        kwargs['guest_team']=_match.get('guest_team')
        kwargs['guest_coach']=_match.get('guest_coach')

        match = self.filter(khl_id = kwargs.get('khl_id')).last()
        if match:
            self.filter(pk=match.pk).update(**kwargs)
        else:
            match = self.create(**kwargs)
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

    def _get_coach(self, coach_ru_fio=''):
        b''' получить тренера '''
        model = get_model(CURRENT_APP, 'Coach')
        return model.objects.get_or_create(ru_fio=coach_ru_fio)[0]

    def _get_team(self, **kwargs):
        b''' получить команду '''
        _region = kwargs.pop('region', None)
        _coach = kwargs.pop('coach', None)
        _players = kwargs.pop('players', None)
        club_model = get_model(CURRENT_APP, 'club')
        _club, _crt = club_model.objects.get_or_create(**kwargs)
        if _players:
            _players = [self._get_player(   p.get('khl_id'),
                                            p.get('ru_fio'),
                                        ) for p in _players
            ]
            _club.players.clear()
            _club.players.add(*_players)
        if _region:
            model = get_model('addresses', 'Address')
            _region, _crt = model.objects.get_or_create(ru_title=_region)
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
        return (model.objects.get_or_create(ru_fio=j) for j in judges)