# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from . import AbstractMan
from .. import choices, managers


class Player(AbstractMan):
    objects = managers.player.PlayerQuerySet.as_manager()
    contract_type = models.CharField(
        _('Contract type'),
        choices=choices.CONTRACT_TYPE, max_length=32, blank=True)
    contract_to = models.DateField(_('Contract to'), null=True, blank=True)
    number = models.CharField(_('Number'), max_length=32, blank=True)
    line = models.PositiveSmallIntegerField(
        _('Line'), default=0, choices=choices.PLAYER_ROLE)
    pos = models.CharField(_('Offender position'), blank=True, max_length=255)
    weight_str = models.CharField(_('Weight'), max_length=32, blank=True)
    height_str = models.CharField(_('Height'), max_length=32, blank=True)
    weight = models.PositiveSmallIntegerField(_('Weight'), null=True)
    height = models.PositiveSmallIntegerField(_('Height'), null=True)
    grip = models.CharField(_('Grip'), max_length=32, blank=True)
    citizenship = models.ForeignKey(
        'addresses.Country', verbose_name=_('Citizenship'),
        on_delete=models.SET_NULL, null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)
    last_club = models.ForeignKey(
        'hockeyapp.Club', verbose_name=_('Club'),
        related_name='last_players', null=True)
    birth_place = models.CharField(_('Birth place'), blank=True,
                                    max_length=255)
    first_school = models.CharField(_('First school'), blank=True,
                                    max_length=255)
    #serviceinfo
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    # clubplayermatch data (do recalc_counters to update)
    seasons_total = models.IntegerField(_('Seasons Total'), null=True)
    matches_total = models.IntegerField(_('Matches Total'), null=True)
    goals_total = models.IntegerField(_('Goals Total'), null=True)
    assists_total = models.IntegerField(_('Assists Total'), null=True)
    points_total = models.IntegerField(_('Points Total'), null=True)
    plus_minus_total = models.IntegerField(_('Plus/minus Total'), null=True)
    penalty_time_total = models.IntegerField(
        _('Penalty Time Total'), null=True)
    gamingtime_total = models.IntegerField(_('Gaming Time Total'), null=True)
    goals_average = models.FloatField(_('Goals Average'), null=True)
    assists_average = models.FloatField(_('Assists Average'), null=True)
    points_average = models.FloatField(_('Points Average'), null=True)
    plus_minus_average = models.FloatField(_('Plus/minus Average'), null=True)
    penalty_time_average = models.FloatField(
        _('Penalty Time Average'), null=True)
    # goalkeeper specific
    bullet_matches_total = models.IntegerField(
        _('Total Matches with Bullet'), null=True)
    zero_goals_matches_total = models.IntegerField(
        _('0 Goals Matches'), null=True)
    shots_received_total = models.IntegerField(
        _('Shots Received Total'), null=True)
    saves_total = models.IntegerField(
        _('Saves Goals Total'), null=True)
    loose_goals_total = models.IntegerField(
        _('Loose Goals'), null=True)
    saves_p_average = models.FloatField(
        _('Saves Goals, Average %'), null=True)
    sf_average = models.FloatField(
        _('Safety Factor Average'), null=True)
    matches_win_total = models.IntegerField(_('Matches Win Total'), null=True)
    matches_lose_total = models.IntegerField(
        _('Matches Lose Total'), null=True)

    # players rating (do recalc_rating to update)
    seasons_total_index = models.IntegerField(
        _('Seasons Total Index'), null=True)
    matches_total_index = models.IntegerField(
        _('Matches Total Index'), null=True)
    goals_total_index = models.IntegerField(
        _('Goals Total Index'), null=True)
    assists_total_index = models.IntegerField(
        _('Assists Total Index'), null=True)
    points_total_index = models.IntegerField(
        _('Points Total Index'), null=True)
    plus_minus_total_index = models.IntegerField(
        _('Plus/minus Total Index'), null=True)
    penalty_time_total_index = models.IntegerField(
        _('Penalty Time Total Index'), null=True)
    goals_average_index = models.IntegerField(
        _('Goals Average Index'), null=True)
    assists_average_index = models.IntegerField(
        _('Assists Average Index'), null=True)
    points_average_index = models.IntegerField(
        _('Points Average Index'), null=True)
    plus_minus_average_index = models.IntegerField(
        _('Plus/minus Average Index'), null=True)
    penalty_time_average_index = models.IntegerField(
        _('Penalty Time Average Index'), null=True)
    gamingtime_total_index = models.IntegerField(
        _('Gaming Time Total Index'), null=True)
    # goalkeeper specific
    bullet_matches_total_index = models.IntegerField(
        _('Total Matches with Bullet Index'), null=True)
    zero_goals_matches_total_index = models.IntegerField(
        _('0 Goals Matches Index'), null=True)
    shots_received_total_index = models.IntegerField(
        _('Shots Received TOtal Index'), null=True)
    saves_total_index = models.IntegerField(
        _('Saves Goals Total Index'), null=True)
    saves_p_average_index = models.IntegerField(
        _('Saves Goals, Average % Index'), null=True)
    sf_average_index = models.IntegerField(
        _('Safety Factor Average Index'), null=True)
    loose_goals_total_index = models.IntegerField(
        _('Loose Goals Index'), null=True)
    matches_win_total_index = models.IntegerField(
        _('Matches Win Total Index'), null=True)
    matches_lose_total_index = models.IntegerField(
        _('Matches Lose Total Index'), null=True)

    last_match_date = models.DateTimeField(
        _('Last match history parsed'), null=True)

    __unicode__ = lambda self: '{0} {1}'.format(self.khl_id, self.ru_fio)

    def save(self, **kwargs):
        if self.pk and not self.line:
            #смотрим амплуа игрока из истории 
            if self.clubplayer_set.exists():
                self.line = self.clubplayer_set.all().last().line
        # update last club
        if self.pk and self.clubplayer_set.exists():
            self.last_club = self.clubplayer_set.order_by(
                '-end_date', '-pk')[0].club
        super(Player, self).save(**kwargs)

    @property
    def club(self):
        return self.last_club

    @property
    def is_legionnaire(self):
        return self.citizenship and (self.citizenship.en_title != 'Russia')

    @property
    def last_match(self):
        from . import ClubPlayerMatch
        return (
            ClubPlayerMatch.objects
            .filter(clubplayer__player=self).order_by('match__date').last())

    def get_absolute_url(self):
        if self.pk:
            return reverse('hockeyapp:players:card', kwargs={'pk': self.pk})

    class Meta(object):
        verbose_name = _('Player')
        verbose_name_plural = _('Players')
