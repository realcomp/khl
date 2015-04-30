# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import bisect
import numpy

from operator import itemgetter, methodcaller

from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Avg
from django.utils import timezone
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
    last_relatedplayer_modified = models.DateTimeField(
        _('Last related player modified date'), null=True)

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

    def get_age_related_players(self):
        '''
        age-related players
        returns players from the same age group
        '''
        age_groups = (
            # до 19 лет (юноши и дети)
            (19, {'years__lt': 20}),
            # 20-23 (молодежь)
            (23, {'years__lt': 24, 'years__gte': 20}),
            # 24-30 (зрелые игроки)
            (30, {'years__lt': 31, 'years__gte': 24}),
            # 31-35 (опытные игроки)
            (35, {'years__lt': 36, 'years__gte': 31}),
            # 36+ (ветераны)
            (999, {'years__gte': 36}),
        )

        group = bisect.bisect_left(zip(*age_groups)[0], self.age[0])
        age_params = age_groups[group][1]
        return Player.objects.by_age(**age_params)

    def get_league_coef(self, player):
        my_cp = self.clubplayer_set.last()
        other_cp = player.clubplayer_set.last()
        if (not my_cp or not my_cp.league or
                not other_cp or not other_cp.league):
            return 1.
        my_league = my_cp.league.en_title.lower()
        other_league = other_cp.league.en_title.lower()
        if my_league == other_league:
            return 1.
        COEFFS = {
            'mhl': {
                'vhl': .8,  # MHL * 0.8 = VHL
            },
            'vhl': {
                'khl': .8,  # VHL * 0.8 = KHL
            },
            'khl': {
            },
        }
        # MHL2KHL = MHL2VHL * VHL2KHL
        COEFFS['mhl']['khl'] = COEFFS['mhl']['vhl'] * COEFFS['vhl']['khl']
        # reversed
        COEFFS['vhl']['mhl'] = 1. / COEFFS['mhl']['vhl']
        COEFFS['khl']['vhl'] = 1. / COEFFS['vhl']['khl']
        COEFFS['khl']['mhl'] = 1. / COEFFS['mhl']['khl']
        return COEFFS.get(my_league, {}).get(other_league, 1.)

    def get_absolute_url(self):
        if self.pk:
            return reverse('hockeyapp:players:card', kwargs={'pk': self.pk})

    class Meta(object):
        verbose_name = _('Player')
        verbose_name_plural = _('Players')


class RelatedPlayer(models.Model):
    objects = managers.player.RelatedPlayer.as_manager()

    player1 = models.ForeignKey(
        Player, verbose_name=_('Player 1'), related_name='relatedplayers1',
        on_delete=models.SET_NULL, null=True, blank=True)
    player2 = models.ForeignKey(
        Player, verbose_name=_('Player 2'), related_name='relatedplayers2',
        on_delete=models.SET_NULL, null=True, blank=True)
    goals_value = models.FloatField(
        _('Similarity by Goals'), blank=True, null=True)
    assists_value = models.FloatField(
        _('Similarity by Assists'), blank=True, null=True)
    points_value = models.FloatField(
        _('Similarity by Points'), blank=True, null=True)
    penalty_time_value = models.FloatField(
        _('Similarity by Penalty time'), blank=True, null=True)
    plus_minus_value = models.FloatField(
        _('Similarity by +/-'), blank=True, null=True)
    modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%d: [%s] - [%s]' % (self.pk, self.player1, self.player2)

    @classmethod
    def calc(cls, players1, players2=None):
        '''
        RelatedPlayer factory
        Calculates similarity values between each pair of players
        '''
        from . import ClubPlayerMatch

        fields = (
            'goals',  # Среднее количество голов за игру
            'assists',  # Среднее количество передач за игру
            'points',  # Среднее количество очков за игру
            'penalty_time',  # Среднее штрафное время за игру
            'plus_minus',  # Средний показатель "плюс/минус" за игру
        )

        def _calc_rel(player, max_length=None):
            '''
            Calculate relative values for list [A1...An] limited by max_length
            Ai / SUM(A1...An)
            '''
            params = {field: Avg(field) for field in fields}
            # list of qs
            qss = (
                ClubPlayerMatch.objects
                .filter(clubplayer__player=player)
                .group_by_month())
            if max_length:
                qss = qss[:max_length]
            aggregated = map(methodcaller('aggregate', **params), qss)

            total = {
                # sum of values excluding None
                field: sum(filter(None, map(itemgetter(field), aggregated)))
                for field in fields
            }

            def _calc_fields_rel(qs, field):
                '''
                Calculate relative value for each field
                '''
                t = float(total.get(field) or 0)
                if t:
                    return float(qs.get(field) or 0) / t
                return .0

            for qs in aggregated:
                yield {field: _calc_fields_rel(qs, field) for field in fields}

        def _calc_mean_diff(rel1, rel2, coef=1):
            '''
            Calculate mean value
            Di = |Ai * COEF - Bi|
            MEAN(D1...Dn)
            '''
            def _calc_fields_mean(field):
                values = [
                    abs(a.get(field) * coef - b.get(field))
                    for a, b in zip(rel1, rel2) if a and b]
                if values:
                    return numpy.mean(values)
                return 0

            return {field: _calc_fields_mean(field) for field in fields}

        for player1 in players1:
            rel1 = list(_calc_rel(player1))
            if rel1 and player1.age:
                if players2:
                    filtered_players2 = players2
                else:
                    # select players from the same age group
                    filtered_players2 = player1.get_age_related_players()
                # don't compare with myself
                filtered_players2 = filtered_players2.exclude(pk=player1.pk)

                for player2 in filtered_players2:
                    rel2 = list(_calc_rel(player2, max_length=len(rel1)))
                    if rel2:
                        # limit array length by minimal
                        length = min(len(rel1), len(rel2))
                        mean = _calc_mean_diff(
                            rel1[:length], rel2[:length],
                            coef=player1.get_league_coef(player2))
                        # get model object to save values
                        rel_players = cls.objects.by_players(player1, player2)
                        if rel_players.exists():
                            rel_player = rel_players.last()
                        else:
                            rel_player = cls.objects.create(
                                player1=player1, player2=player2)
                        for k, v in mean.items():
                            setattr(rel_player, '%s_value' % k, v)
                        rel_player.save()
                player1.last_relatedplayer_modified = timezone.now()
                player1.save(update_fields=('last_relatedplayer_modified',))

    class Meta(object):
        ordering = 'modified',
        verbose_name = _('Related Player')
        verbose_name_plural = _('Related Players')
