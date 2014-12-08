#coding: utf-8
from __future__ import unicode_literals
from django.db import models

from base.models import TitleBaseModel, Region

#from .managers import MatchManager


class AbstractMan(models.Model):
    fio = models.CharField(b'ФИО', max_length=4096, blank=True)
    __unicode__ = lambda self: self.fio


class Player(AbstractMan):
    #player_type
    class Meta:
        verbose_name=b'Игрок'
        verbose_name_plural=b'Игроки'


class Coach(AbstractMan):
    class Meta:
        verbose_name=b'Тренер'
        verbose_name_plural=b'Тренеры'


class Judge(AbstractMan):
    class Meta:
        verbose_name=b'Судья'
        verbose_name_plural=b'Судьи'


class Team(TitleBaseModel):
    region = models.ForeignKey(Region, null=True, blank=True)
    coach = models.ForeignKey(Coach, null=True, blank=True)
    players = models.ManyToManyField(Player, null=True, blank=True)

    class Meta:
        verbose_name=b'Команда'
        verbose_name_plural=b'Команды'


class MatchManager(models.Manager):
    b''' Мененжер матчей по-умолчанию '''
    def get_or_create_match(self, **kwargs):
        b''' метод взять или создать запись о матче '''
        _hometeam = kwargs.pop('home_team', None)
        _guestteam = kwargs.pop('guest_team', None)
        _judges = kwargs.pop('judges', [])
        _linejudges = kwargs.pop('line_judges', [])
        match, _crt = self.get_or_create(khl_id = kwargs.get('khl_id'))
        match.home_team = self._get_team(**_hometeam)
        match.guest_team = self._get_team(**_guestteam)
        match.save()
        match.judges.add(*self._get_judges(_judges))
        match.line_judges.add(*self._get_judges(_linejudges))
        self.filter(pk=match.pk).update(**kwargs)
        return match

    def _get_team(self, **kwargs):
        _region = kwargs.pop('region', None)
        if _region:
            _region, _crt = Region.objects.get_or_create(title=_region)
        _coach = kwargs.pop('coach', None)
        if _coach:
            _coach, _crt = Coach.objects.get_or_create(fio=_coach)
        return Team.objects.get_or_create(  region=_region,
                                            coach=_coach,
                                            **kwargs)[0]

    def _get_judges(self, judges=None):
        judges = judges or []
        res = []
        for j in judges:
            _j, _crt = Judge.objects.get_or_create(fio=j)
            res.append(_j)
        return res


class Match(TitleBaseModel):
    objects = MatchManager()
    #service info
    khl_id = models.PositiveIntegerField(b'ID на стороннем ресурсе',
                                max_length=1024, blank=True)
    proccesed_time = models.DateTimeField(b'Обработан, время',auto_now_add=True)

    #main info
    spectators = models.CharField(b'Посещаемость', max_length=1024, blank=True)
    date = models.CharField(b'Дата матча', max_length=1024, blank=True)
    count = models.CharField(b'Счет матча', max_length=1024, blank=True)
    detail_count = models.CharField(b'Счет по периодам', 
                                    max_length=1024, blank=True)
    judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchjudges',
                            verbose_name=Judge._meta.verbose_name_plural)
    line_judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchllinejudges',
                            verbose_name=b'Линейные судьи')
    home_team = models.ForeignKey(Team, null=True, blank=True,
                                related_name='hometeam',
                                verbose_name=b'Домашняя команда')
    guest_team = models.ForeignKey(Team, null=True, blank=True,
                                related_name='guestteam',
                                verbose_name=b'Гостевая команда')

    class Meta:
        verbose_name=b'Матч'
        verbose_name_plural=b'Матчи'
        ordering = '-khl_id',