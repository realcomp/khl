# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from .. import managers


class ClubPlayerMatch(models.Model):
    b'''
        связка игрок в клубе в сезоне с матчем в сезоне
        По сути статистика игрока в каждом матче
    '''
    objects = managers.match.ClubPlayerMatchQuerySet.as_manager()

    clubplayer = models.ForeignKey('hockeyapp.ClubPlayer')
    match = models.ForeignKey('hockeyapp.Match')
    adv_stats = models.OneToOneField('hockeyapp.AdvancedPlayerStats', null=True, blank=True)
    goals = models.SmallIntegerField(_('Goals'), null=True)
    assists = models.SmallIntegerField(_('Assists'), null=True)
    points = models.SmallIntegerField(_('Points'), null=True)
    plus_minus = models.SmallIntegerField('+/-', null=True)
    penalty_time = models.PositiveIntegerField(_('Penalty Time'), null=True)
    ev_goals = models.PositiveSmallIntegerField(_('EV Goals'), null=True)
    pp_goals = models.PositiveSmallIntegerField(_('Power Play Goals'), null=True)
    es_goals = models.PositiveSmallIntegerField(_('Even Strength Goals'), null=True)
    overtime_goals = models.PositiveSmallIntegerField(_('Overtime Goals'), null=True)
    win_goals = models.PositiveSmallIntegerField(_('Win Goals'), null=True)
    bullet_goals = models.PositiveSmallIntegerField(_('Win Bullet Goals'), null=True)
    shots = models.PositiveSmallIntegerField(_('Shots count'), null=True)
    pis = models.FloatField(_('Implemented Shots, %'), null=True)
    faceoff = models.PositiveSmallIntegerField(_('Face-off'), null=True)
    winfaceoff = models.PositiveSmallIntegerField(_('Face-off Wins'), null=True)
    winfaceoff_p = models.FloatField(_('Face-off Wins, %'), null=True)
    #khl adv stats
    change_count = models.PositiveIntegerField(_('Change count'),null=True)
    hits = models.PositiveIntegerField(_('Hits'),null=True)
    blocks = models.PositiveIntegerField(_('Blocks'),null=True)
    fouls = models.PositiveIntegerField(_('Fouls'),null=True)
    #keeper stats
    loose_goals = models.PositiveSmallIntegerField(_('Loose Goals'), null=True)
    saves = models.PositiveSmallIntegerField(_('Saves Goals'), null=True)
    saves_p = models.FloatField(_('Saves Goals , %'), null=True)
    sf = models.FloatField(_('Safety Factor'), null=True) # KH
    gamingtime = models.PositiveIntegerField(_('Gaming time'), null=True)

    created = models.DateTimeField(_('Created date'), auto_now_add=True)

    __unicode__ = lambda self: '{}'.format(self.match or self.pk,)

    @property
    def match_date(self):
        return self.match.date

    class Meta(object):
        verbose_name = _('Club Player History Match')
        verbose_name_plural = _('Club Player Histories in Matches')
