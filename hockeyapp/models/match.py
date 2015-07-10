# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from base.models import TitleBaseModel, AdminLinkMixin

from .. import choices, managers
from . import Judge


class Match(AdminLinkMixin, TitleBaseModel):
    objects = managers.match.MatchManager()

    # service info
    khl_id = models.PositiveIntegerField(_('Other site ID'), null=True)
    challenge_type = models.PositiveSmallIntegerField(
        _('Challenge Type'), null=True, choices=choices.CHALLENGE_TYPE)
    proccesed_time = models.DateTimeField(_('Processed time'), auto_now=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    # main info
    spectators = models.PositiveIntegerField(_('Spectators count'), null=True)
    spectators_str = models.CharField(
        _('Spectators count'), max_length=1024, blank=True)
    date_str = models.CharField(_('Match date'), max_length=1024, blank=True)
    date = models.DateTimeField(_('Match date'), null=True, blank=True)
    count = models.CharField(_('Match count'), max_length=1024, blank=True)
    detail_count = models.CharField(
        _('Match detail count'), max_length=1024, blank=True)
    home_score = models.PositiveSmallIntegerField(_('Home score'), null=True)
    guest_score = models.PositiveSmallIntegerField(_('Guest score'), null=True)
    overtime_win = models.BooleanField(_('Overtime'), default=False)
    bullet_win = models.BooleanField(_('Bullets'), default=False)
    judges = models.ManyToManyField(
        'hockeyapp.Judge', null=True, blank=True,
        related_name='matchjudges',
        verbose_name=Judge._meta.verbose_name_plural)
    line_judges = models.ManyToManyField(
        'hockeyapp.Judge', null=True, blank=True,
        related_name='matchlinejudges', verbose_name=_('Line judges'))
    home_team = models.ForeignKey(
        'hockeyapp.Club', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='homematches',
        verbose_name=_('Home team'))
    home_coach = models.ForeignKey(
        'hockeyapp.Coach', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='homematches')
    home_players = models.ManyToManyField(
        'hockeyapp.ClubPlayer', null=True, blank=True,
        related_name='homematches')
    guest_team = models.ForeignKey(
        'hockeyapp.Club', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='guestmatches',
        verbose_name=_('Guest team'))
    guest_coach = models.ForeignKey(
        'hockeyapp.Coach', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='guestmatches')
    guest_players = models.ManyToManyField(
        'hockeyapp.ClubPlayer', null=True, blank=True,
        related_name='guestmatches')

    league = models.ForeignKey(
        'hockeyapp.League', null=True, blank=True, on_delete=models.SET_NULL)
    home_count = models.IntegerField(_('Home team count'), default=0)
    guest_count = models.IntegerField(_('Guest team count'), default=0)

    class Meta(object):
        verbose_name = _('Match')
        verbose_name_plural = _('Matches')
        ordering = '-khl_id',

    def __unicode__(self):
        if self.count and self.date and self.home_team and self.guest_team:
            return '{} {} {} ({})'.format(
                self.home_team, self.count, self.guest_team, self.date)
        return self.ru_title

    @property
    def winner(self):
        if self.home_count > self.guest_count:
            return self.home_team
        if self.home_count < self.guest_count:
            return self.guest_team

    @property
    def loser(self):
        if self.home_count < self.guest_count:
            return self.home_team
        if self.home_count > self.guest_count:
            return self.guest_team

    def save(self, **kwargs):
        if self.count:
            home_count, _, guest_count = self.count.partition(':')
            self.home_count = int(filter(
                lambda x: x.isdigit(), home_count) or 0)
            self.guest_count = int(filter(
                lambda x: x.isdigit(), guest_count) or 0)
        super(Match, self).save(**kwargs)


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
