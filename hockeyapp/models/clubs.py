# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import re

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from base.models import AdminLinkMixin, TitleBaseModel

from .. import choices, managers
from ..validators import hex_validator


class Club(AdminLinkMixin, TitleBaseModel):
    objects = managers.club.ClubQuerySet.as_manager()

    opening_dt = models.DateField(_('Founding date'), null=True, blank=True)
    closing_dt = models.DateField(_('Closing date'), null=True, blank=True)
    logo = FilerImageField(verbose_name=_('Logo'), null=True, blank=True,
                           on_delete=models.SET_NULL)
    site = models.URLField(_('Site'), blank=True)
    email = models.CharField(_('E-mail'), max_length=255, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=255, blank=True, null=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    style = models.TextField(_('Styles (CSS)'), blank=True, null=True)
    rgb = models.CharField(_('RGB'), blank=True, null=True, max_length=255,
                            help_text=_('Color hex. Example: #00ffaa'),
                            validators=[hex_validator])
    main_color = models.TextField(_('Main color'), blank=True,
                            help_text=_('Color hex. Example: #00ffaa'),
                            validators=[hex_validator])
    secondary_color = models.TextField(_('2th color'), blank=True,
                            help_text=_('Color hex. Example: #00ffaa'),
                            validators=[hex_validator])
    third_color = models.TextField(_('Third color'), blank=True,
                            help_text=_('Color hex. Example: #00ffaa'),
                            validators=[hex_validator])
    #socials
    vk = models.URLField('VK account URL', blank=True, max_length=1024)
    ok = models.URLField('OK account URL', blank=True, max_length=1024)
    fb = models.URLField('Facebook account URL', blank=True, max_length=1024)
    gl = models.URLField('Google+ account URL', blank=True, max_length=1024)
    tw = models.URLField('Twitter account URL', blank=True, max_length=1024)
    im = models.URLField('Instagram account URL', blank=True, max_length=1024)
    pp = models.URLField('Personal page URL', blank=True, max_length=1024)
    ut = models.URLField('Youtube account URL', blank=True, max_length=1024)
    #relation
    address = models.ForeignKey(
        'addresses.Address', null=True, blank=True,
        on_delete=models.SET_NULL)
    coach = models.ForeignKey(
        'hockeyapp.Coach', null=True, blank=True,
        related_name='headcoachclubs', verbose_name=_('Head Coach'),
        on_delete=models.SET_NULL)
    coaches = models.ManyToManyField(
        'hockeyapp.Coach', null=True, blank=True,
        related_name='helpcoachclubs', verbose_name=_('Help coaches'))
    arena = models.ForeignKey(
        'hockeyapp.Arena', null=True, blank=True, on_delete=models.SET_NULL)
    players = models.ManyToManyField('hockeyapp.Player', null=True, blank=True)
    league = models.ForeignKey('hockeyapp.League', null=True, blank=True)
    farm_club = models.OneToOneField('self', null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='farmclubparent')
    junior_club = models.OneToOneField('self', null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='juniorclubparent')
    #serviceinfo
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    # counters
    matches_total = models.IntegerField(_('Matches Total'), null=True)
    last_match_date = models.DateTimeField(
        _('Last match history parsed'), null=True)

    __unicode__ = lambda self: '{} ({})'.format(self.ru_title, self.address)

    def get_title_verbose(self, request=None):
        title = self.get_locale_attr('title', request=request)
        if self.address:
            title += ' (%s)' % self.address.get_locale_attr(
                'title', request=request)
        return title

    def get_players(self, season):
        from . import Player
        if season.is_current:
            return self.players.all()
        else:
            clubplayers = self.clubplayer_set.by_season(season)
            pks = clubplayers.values_list('player_id', flat=True)
            return Player.objects.filter(pk__in=pks)

    def get_not_playing_players(self):
        from . import Player, Season
        current_season = Season.objects.get_current_season()
        if current_season:
            ids =  Player.objects.exclude(clubplayer__season=current_season
                                ).filter(clubplayer__club=self
                                ).values_list('pk', flat=True)
            return Player.objects.filter(pk__in=ids)
        return Player.objects.none()

    @property
    def all_players(self):
        return self.players.order_by('line', 'number')

    @property
    def current_offender_players(self):
        return self.players.filter(line=3).order_by('number')

    @property
    def current_defender_players(self):
        return self.players.filter(line=2).order_by('number')

    @property
    def current_goalkeeper_players(self):
        return self.players.filter(line=1).order_by('number')

    def get_absolute_url(self):
        if self.pk:
            return reverse('hockeyapp:clubs:details', kwargs={'pk': self.pk})

    @property
    def seasons(self):
        from . import Season
        return (
            Season.objects
            .filter(pk__in=self.clubplayer_set.values_list('season_id'))
            .order_by('-start_date'))

    def get_prev_season(self, season):
        seasons = list(reversed(self.seasons))
        i = seasons.index(season)
        if i > 0:
            return seasons[i - 1]

    def get_next_season(self, season):
        seasons = list(reversed(self.seasons))
        i = seasons.index(season)
        if i < len(seasons) - 1:
            return seasons[i + 1]

    def get_instagam_photo(self):
        return self.pk and self.arenainstaphoto_set.club_photo(self)

    class Meta:
        verbose_name = _('Club')
        verbose_name_plural = _('Clubs')
