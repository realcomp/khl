#coding: utf-8
from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from addresses.models import Address
from base.models import TitleBaseModel

from .choices import PLAYER_ROLE, PARITY_VALUES
from . import managers


class AbstractMan(models.Model):
    ru_fio = models.CharField(_('Full name (rus)'), max_length=4096, blank=True)
    en_fio = models.CharField(_('Full name (en)'), max_length=4096, blank=True)
    __unicode__ = lambda self: self.ru_fio
    class Meta:
        abstract=True

class Player(AbstractMan):
    objects = managers.PlayerManager()
    khl_id = models.PositiveIntegerField(default=0)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    __unicode__ = lambda self: '{0} {1}'.format(self.khl_id, self.ru_fio)
    class Meta:
        verbose_name=_('Player')
        verbose_name_plural=_('Players')


class Coach(AbstractMan):
    class Meta:
        verbose_name=_('Coach')
        verbose_name_plural=_('Coaches')


class Judge(AbstractMan):
    class Meta:
        verbose_name=_('Judge')
        verbose_name_plural=_('Judges')


class Club(TitleBaseModel):
    address = models.ForeignKey(Address, null=True, blank=True)
    coach = models.ForeignKey(Coach, null=True, blank=True)
    players = models.ManyToManyField(Player, null=True, blank=True)
    opening_dt = models.DateField(_('Founding date'), null=True, blank=True)
    closing_dt = models.DateField(_('Closing date'), null=True, blank=True)
    logo = FilerImageField(verbose_name=_('Logo'), null=True, blank=True)
    site = models.URLField(_('Site'), blank=True)

    class Meta:
        verbose_name=_('Club')
        verbose_name_plural=_('Clubs')


class AddressClub(models.Model):
    b''' связка адрес - клуб в сезоне '''
    address = models.ForeignKey(Address)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    class Meta:
        verbose_name=_('Club address')
        verbose_name_plural=_('Club addresses')


class ClubPlayer(models.Model):
    b''' связка игрок - клуб в сезоне '''
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    number = models.PositiveIntegerField(_('Number'), default=0)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    __unicode__ = lambda self: '{0} ({1})'.format(self.player, self.club)
    class Meta:
        verbose_name=_('Club player')
        verbose_name_plural=_('Club players')


class CoachClub(models.Model):
    b''' связка тренер клуб в сезоне '''
    coach = models.ForeignKey(Coach)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True)
    end_date = models.DateField(_('End date'), null=True)
    class Meta:
        verbose_name=_('Club coach')
        verbose_name_plural=_('Club coaches')


class ClubPlayerMatch(models.Model):
    b''' связка игрок в клубе в сезоне с матчем в сезоне '''
    clubplayers = models.ManyToManyField(ClubPlayer)
    match = models.ForeignKey('hockeyapp.Match')


class MatchGoalHistory(models.Model):
    b'''Хранит историю матча. Заброшенные шайбы'''
    objects = managers.MatchGoalHistoryManager()
    match = models.ForeignKey('hockeyapp.Match')
    parity = models.PositiveSmallIntegerField(choices=PARITY_VALUES, default=0)
    time = models.CharField(max_length=16, blank=True)
    description = models.CharField(max_length=1024, blank=True)
    period = models.CharField(max_length=32, blank=True)
    scorer = models.ForeignKey(Player, related_name='goalscorermatch')
    assist = models.ManyToManyField(Player, null=True, blank=True,
                                    related_name='goalassistmatch')
    #home_five = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    #related_name='homematchegoalhistory')
    #guest_five = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    #related_name='guestmatchegoalhistory')
    home_five_numbers = models.CharField(max_length=1024, blank=True)
    home_five_numbers = models.CharField(max_length=1024, blank=True)
    class Meta:
        verbose_name=_('Match goal entry')
        verbose_name_plural=_('Match goal entries')


class MatchPenaltyHistory(models.Model):
    b'''Хранит историю матча. Заброшенные шайбы'''
    objects = managers.MatchPenaltyHistoryManager()
    match = models.ForeignKey('hockeyapp.Match')
    player = models.ForeignKey(Player, related_name='penaltymatch')
    ptype = models.CharField(max_length=1024, blank=True)
    time = models.CharField(max_length=32, blank=True)
    duration = models.CharField(max_length=32, blank=True)
    class Meta:
        verbose_name=_('Match penalty entry')
        verbose_name_plural=_('Match penalty entries')


class Match(TitleBaseModel):
    objects = managers.MatchManager()
    #service info
    khl_id = models.PositiveIntegerField(_('Other site ID'),
                                max_length=1024, blank=True)
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    #main info
    spectators = models.CharField(_('Spectators count'), max_length=1024,
                                    blank=True)
    date = models.CharField(_('Match date'), max_length=1024, blank=True)
    count = models.CharField(_('Match count'), max_length=1024, blank=True)
    detail_count = models.CharField(_('Match detail count'), 
                                    max_length=1024, blank=True)
    judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchjudges',
                            verbose_name=Judge._meta.verbose_name_plural)
    line_judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchllinejudges',
                            verbose_name=_('Line judges'))
    home_team = models.ForeignKey(Club, null=True, blank=True,
                                related_name='homematches',
                                verbose_name=_('Home team'))
    home_coach = models.ForeignKey(Coach, null=True, blank=True,
                                    related_name='homematches')
    home_players = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    related_name='homematches')
    guest_team = models.ForeignKey(Club, null=True, blank=True,
                                related_name='guestmatches',
                                verbose_name=_('Guest team'))
    guest_coach = models.ForeignKey(Coach, null=True, blank=True,
                                    related_name='guestmatches')
    guest_players = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    related_name='guestmatches')

    class Meta:
        verbose_name=_('Match')
        verbose_name_plural=_('Matches')
        ordering = '-khl_id',