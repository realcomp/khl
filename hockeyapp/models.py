#coding: utf-8
from __future__ import unicode_literals
import datetime
import itertools
import re
import urllib

from dateutil import relativedelta

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import F, Q, Avg, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from addresses.models import Address, Country
from base.models import LocaleAttrMixin, TitleBaseModel, AdminLinkMixin, Season
from base.models import TitleAlias, SocialAbstract, InstagramImageFile

from .choices import PLAYER_ROLE, PARITY_VALUES, CONTRACT_TYPE, FIVER_VALUES
from .choices import CHALLENGE_TYPE, PARSERS
from . import managers, parsers


def rgb_validator(value):
    if not re.match(r"(\d+),\s*(\d+),\s*(\d+)", value):
        raise ValidationError('Incorrect format. Expected `#,#,#`.')


def hex_validator(value):
    if not re.match(r'#[0-9a-fA-F]{6}', value):
        raise ValidationError('Incorrect format. Expected hex.')


class AbstractMan(LocaleAttrMixin, models.Model):
    ru_fio = models.CharField(_('Full name (rus)'), max_length=4096, blank=True)
    ru_name = models.CharField(_('Name (rus)'), max_length=4096, blank=True, null=True)
    ru_lastname = models.CharField(_('Last name (rus)'), max_length=4096, blank=True, null=True)
    en_fio = models.CharField(_('Full name (en)'), max_length=4096, blank=True)
    en_name = models.CharField(_('Name (en)'), max_length=4096, blank=True, null=True)
    en_lastname = models.CharField(_('Last name (en)'), max_length=4096, blank=True, null=True)
    birth_date = models.DateField(_('Birth date'), null=True, blank=True)
    death_date = models.DateField(_('Death date'), null=True, blank=True)
    khl_id = models.PositiveIntegerField(default=0, null=True)
    #socials
    vk = models.URLField('VK account URL', blank=True, max_length=1024)
    ok = models.URLField('OK account URL', blank=True, max_length=1024)
    fb = models.URLField('Facebook account URL', blank=True, max_length=1024)
    gl = models.URLField('Google+ account URL', blank=True, max_length=1024)
    tw = models.URLField('Twitter account URL', blank=True, max_length=1024)
    im = models.URLField('Instagram account URL', blank=True, max_length=1024)
    pp = models.URLField('Personal page URL', blank=True, max_length=1024)
    ut = models.URLField('Youtube account URL', blank=True, max_length=1024)
    wiki_page = models.URLField('Wiki page URL', blank=True, max_length=1024)
    #parser service
    fio = models.CharField(_('FIO from parser'),max_length=4096, blank=True,
                            editable=False)

    __unicode__ = lambda self: self.ru_fio

    @property
    def age(self):
        ''' returns age as (years, months) '''
        if self.birth_date:
            delta = relativedelta.relativedelta(
                timezone.now().date(), self.birth_date)
            return delta.years, delta.months
        return None, None

    def save(self, **kwargs):
        if self.ru_fio and (not self.ru_name or not self.ru_lastname):
            self.ru_name, sep, self.ru_lastname = self.ru_fio.partition(' ')
        if self.en_fio and (not self.en_name or not self.en_lastname):
            self.en_name, sep, self.en_lastname = self.en_fio.partition(' ')
        if not self.ru_fio and self.fio:
            self.ru_fio = self.fio
        super(AbstractMan, self).save(**kwargs)

    class Meta:
        abstract=True


class Player(AbstractMan):
    objects = managers.player.PlayerQuerySet.as_manager()
    contract_type = models.CharField(_('Contract type'),
                                        choices=CONTRACT_TYPE,
                                            max_length=32, blank=True)
    contract_to = models.DateField(_('Contract to'), null=True, blank=True)
    number = models.CharField(_('Number'), max_length=32, blank=True)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    pos = models.CharField(_('Offender position'), blank=True, max_length=255)
    weight = models.CharField(_('Weight'), max_length=32, blank=True)
    height = models.CharField(_('Height'), max_length=32, blank=True)
    grip = models.CharField(_('Grip'), max_length=32, blank=True)
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
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

    def get_absolute_url(self):
        if self.pk:
            return reverse('hockeyapp:player-card', kwargs={'pk': self.pk})

    class Meta:
        verbose_name=_('Player')
        verbose_name_plural=_('Players')


class PlayerCitizenship(models.Model):
    b''' связка игрок - гражданство '''
    player = models.ForeignKey(Player)
    citizenship = models.ForeignKey(Country)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)

    __unicode__ = lambda self: '{0} ({1})'.format(self.player, self.citizenship)

    class Meta:
        verbose_name=_('Player citizenship')
        verbose_name_plural=_('Players citizenships')


class PlayerSocial(SocialAbstract):
    player = models.ForeignKey(Player)
    class Meta:
        verbose_name=_('Player social account')
        verbose_name_plural=_('Players social accounts')


class Coach(AbstractMan):
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)
    class Meta:
        verbose_name=_('Coach')
        verbose_name_plural=_('Coaches')


class CoachSocial(SocialAbstract):
    coach = models.ForeignKey(Coach)
    class Meta:
        verbose_name=_('Coach social account')
        verbose_name_plural=_('Coaches social accounts')


class Judge(AbstractMan):
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)
    class Meta:
        verbose_name=_('Judge')
        verbose_name_plural=_('Judges')


class JudgeSocial(SocialAbstract):
    judge = models.ForeignKey(Judge)
    class Meta:
        verbose_name=_('Judge social account')
        verbose_name_plural=_('Judges social accounts')


class PlayerCoachJudge(models.Model):
    player = models.OneToOneField(Player,verbose_name=Player._meta.verbose_name,
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    coach = models.OneToOneField(Coach,verbose_name=Coach._meta.verbose_name,
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    judge = models.OneToOneField(Judge,verbose_name=Judge._meta.verbose_name,
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    __unicode__ = lambda self: '{} {} {} {}'.format(self.id, self.player,
                                                    self.coach, self.judge)
    class Meta:
        verbose_name=_('Player - Coach - Judge')
        verbose_name_plural=verbose_name


class Arena(AdminLinkMixin, TitleBaseModel):
    objects = managers.arena.ArenaQuerySet.as_manager()
    capacity = models.PositiveIntegerField(_('Capacity'), null=True)
    coords = models.CharField(_('Latitude and Longitude'),
                                max_length=1024, blank=True)
    site = models.URLField(_('Site'), blank=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    tickets_url = models.URLField(_('Tickets'), blank=True)
    photo = FilerImageField(verbose_name=_('Main photo'), null=True, blank=True)
    address = models.ForeignKey(Address, null=True, blank=True,
                                verbose_name=Address._meta.verbose_name,)
    country = models.ForeignKey(Country, null=True, blank=True,
                                verbose_name=Country._meta.verbose_name,)
    league = models.ForeignKey('League', null=True, blank=True)
    image_folder_name = property(lambda self: 'ArenaInstaPhoto:{}(id{})'.format(
                                                                self.title,
                                                                self.pk,)
    )

    def get_absolute_url(self):
        if self.pk:
            club = self.club_set.latest('pk')
            return reverse('hockeyapp:club-home', kwargs={'pk': club.pk})

    class Meta:
        verbose_name=_('Arena')
        verbose_name_plural=_('Arenas')


class ArenaPhotos(models.Model):
    photo = FilerImageField(verbose_name=_('Photo'))
    arena = models.ForeignKey(Arena, verbose_name=Arena._meta.verbose_name)


class ArenaInstaPhoto(models.Model):
    objects = managers.arena.ArenaInstaPhotoQuerySet.as_manager()
    arena = models.ForeignKey(Arena, verbose_name=Arena._meta.verbose_name)
    photo = models.ForeignKey(InstagramImageFile)
    match = models.ForeignKey('hockeyapp.Match', null=True, blank=True,
                                on_delete=models.SET_NULL,)
    club = models.ForeignKey('hockeyapp.Club', null=True, blank=True,
                                on_delete=models.SET_NULL,)
    players = models.ManyToManyField(Player, null=True, blank=True,)
    comment = models.CharField(_('Comment'), max_length=1024, blank=True)
    processed = models.BooleanField(default=False)
    proccesed_time = models.DateTimeField(_('Processed time'), auto_now=True,)    
    class Meta:
        verbose_name=_('Club instagram photo')
        verbose_name_plural=_('Club instagram photos')
        ordering = 'photo__created',

    def save(self, **kwargs):
        if self.photo.comment and not self.comment:
            self.comment = self.photo.comment
        super(ArenaInstaPhoto, self).save(**kwargs)


class League(TitleBaseModel):
    country = models.ForeignKey(Country, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    class Meta:
        verbose_name=_('League')
        verbose_name_plural=_('Leagues')


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
    address = models.ForeignKey(Address, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    coach = models.ForeignKey(Coach, null=True, blank=True,
                    related_name='headcoachclubs', verbose_name=_('Head Coach'),
                                    on_delete=models.SET_NULL)
    coaches = models.ManyToManyField(Coach, null=True, blank=True,
                    related_name='helpcoachclubs', verbose_name=_('Help coaches')
    )
    arena = models.ForeignKey(Arena, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    players = models.ManyToManyField(Player, null=True, blank=True)
    league = models.ForeignKey(League, null=True, blank=True)
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

    __unicode__ = lambda self: '{} ({})'.format(self.ru_title, self.address)

    def get_title_verbose(self, request=None):
        title = self.get_locale_attr('title', request=request)
        if self.address:
            title += ' (%s)' % self.address.get_locale_attr(
                'title', request=request)
        return title

    def get_players(self, season):
        if season.is_last:
            return self.players.all()
        else:
            clubplayers = self.clubplayer_set.by_season(season)
            pks = clubplayers.values_list('player_id', flat=True)
            return Player.objects.filter(pk__in=pks)

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
            return reverse('hockeyapp:club', kwargs={'pk': self.pk})

    @property
    def seasons(self):
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


class ClubTitleAlias(models.Model):
    b''' Имя(алиас) клуба '''
    club = models.ForeignKey(Club)
    alias = models.OneToOneField(TitleAlias)

    class Meta:
        verbose_name = _('Club title alias')
        verbose_name_plural = _('Club title aliases ')


class AddressClub(models.Model):
    b''' связка адрес - клуб в сезоне '''
    address = models.ForeignKey(Address)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)

    postaddress = models.TextField(_('Post address'), blank=True)
    office_phone = models.CharField(_('Office phone'),
                                    max_length=255, blank=True)
    contact_name = models.CharField(_('Contact name'),
                                    max_length=255, blank=True)
    contact_phone = models.CharField(_('Contact phone'),
                                    max_length=255, blank=True)
    contact_post = models.CharField(_('Contact post'),
                                    max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(_('Phone'), max_length=255, blank=True)
    coords = models.CharField(_('Latitude and Longitude'),
                                max_length=1024, blank=True)
    photo = FilerImageField(verbose_name=_('Main photo'), null=True, blank=True)

    __unicode__ = lambda self: '{0} ({1})'.format(self.address, self.club)

    class Meta:
        verbose_name=_('Club address')
        verbose_name_plural=_('Club addresses')


class AddressClubPhotos(models.Model):
    addressclub = models.ForeignKey(AddressClub, 
                                    verbose_name=AddressClub._meta.verbose_name)
    photo = FilerImageField(verbose_name=_('Photo'))


class LeagueClub(AdminLinkMixin, models.Model):
    b''' связка лига - клуб в сезоне '''
    league = models.ForeignKey(League)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)
    
    __unicode__ = lambda self: '{0} ({1})'.format(self.league, self.club)
    
    class Meta:
        verbose_name=_('Club league')
        verbose_name_plural=_('Club leagues')


class ClubPlayer(models.Model):
    b''' связка игрок - клуб в сезоне '''
    objects = managers.player.ClubPlayerQuerySet.as_manager()
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    number = models.PositiveIntegerField(_('Number'), default=0)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    league = models.ForeignKey(League, null=True, blank=True,
                                on_delete=models.SET_NULL,)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)

    __unicode__ = lambda self: '{0} ({1})'.format(self.player, self.club)

    def save(self, **kwargs):
        if not self.league:
            #добавляем лигу клуба
            self.league = self._get_club_league()
        super(ClubPlayer, self).save(**kwargs)

    def _get_club_league(self):
        if self.club:
            if self.club.league:
                return self.club.league
            qs = self.club.leagueclub_set.all()
            if qs.last():
                return qs.last().league

    @property
    def player_url(self):
        if self.pk and self.player:
            url = reverse(
                'hockeyapp:player-card', kwargs={'pk': self.player.pk})
            return '%s' % url

    @property
    def club_url(self):
        if self.pk and self.club:
            url = reverse('hockeyapp:club', kwargs={'pk': self.club.pk})
            if self.season:
                url += '?%s' % urllib.urlencode({
                    'season': self.season.pk,
                })
            return url

    class Meta:
        verbose_name=_('Club player')
        verbose_name_plural=_('Club players')


class CoachClub(models.Model):
    b''' связка тренер клуб в сезоне '''
    coach = models.ForeignKey(Coach)
    club = models.ForeignKey(Club)
    head = models.BooleanField(_('Head coach'), default=True)
    start_date = models.DateField(_('Start date'), null=True)
    end_date = models.DateField(_('End date'), null=True)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)

    __unicode__ = lambda self: '{0} ({1})'.format(self.coach, self.club)

    class Meta:
        verbose_name=_('Club coach')
        verbose_name_plural=_('Club coaches')


class LogoClubHistory(models.Model):
    b''' связка лого клуб в сезоне '''
    club = models.ForeignKey(Club)
    logo = FilerImageField(verbose_name=_('Logo'))
    start_date = models.DateField(_('Start date'), null=True)
    end_date = models.DateField(_('End date'), null=True)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)
    class Meta:
        verbose_name=_('Logo Club History')
        verbose_name_plural=_('Logo Club Histories')


class ClubSocial(SocialAbstract):
    club = models.ForeignKey(Club)
    class Meta:
        verbose_name=_('Club social account')
        verbose_name_plural=_('Clubs social accounts')


class AdvancedPlayerStats(models.Model):
    b''' Дополнительная статистика по игроку в матче '''
    fiver = models.PositiveSmallIntegerField(_('Fiver'), null=True,
                                            choices=FIVER_VALUES)
    shots_1th = models.CharField(_('1th period Shots'),
                                    max_length=16, blank=True)
    shots_2nd = models.CharField(_('2nd period Shots'),
                                    max_length=16, blank=True)
    shots_3th = models.CharField(_('3th period Shots'),
                                    max_length=16, blank=True)
    shots_all = models.CharField(_('All periods Shots'),
                                    max_length=16, blank=True)
    faceoff_1th = models.CharField(_('1th period Faceoffs'),
                                    max_length=16, blank=True)
    faceoff_2nd = models.CharField(_('2nd period Faceoffs'),
                                    max_length=16, blank=True)
    faceoff_3th = models.CharField(_('3th period Faceoffs'),
                                    max_length=16, blank=True)
    faceoff_all = models.CharField(_('All periods Faceoffs'),
                                    max_length=16, blank=True)
    change_count_1th = models.PositiveSmallIntegerField(
                                    _('1th period change count'), null=True)
    gamingtime_1th = models.PositiveIntegerField(
                                    _('1th period time in game, sec'),null=True)
    change_count_2nd = models.PositiveSmallIntegerField(
                                    _('2nd period change count'), null=True)
    gamingtime_2nd = models.PositiveIntegerField(
                                    _('2nd period time in game, sec'),null=True)
    change_count_3th = models.PositiveIntegerField(
                                    _('3th period change count'),null=True)
    gamingtime_3th = models.PositiveIntegerField(
                                    _('3th period time in game, sec'),null=True)
    change_count_all = models.PositiveIntegerField(
                                    _('All periods change count'),null=True)
    gamingtime_all = models.PositiveIntegerField(
                                    _('All periods time in game, sec'),null=True)
    block_1th = models.PositiveIntegerField(
                                    _('1th period blocks'),null=True)
    hit_1th = models.PositiveIntegerField(
                                    _('1th period hits'),null=True)
    foul_1th = models.PositiveIntegerField(
                                    _('1th period fouls'),null=True)
    block_2nd = models.PositiveIntegerField(
                                    _('2nd period blocks'),null=True)
    hit_2nd = models.PositiveIntegerField(
                                    _('2nd period hits'),null=True)
    foul_2nd = models.PositiveIntegerField(
                                    _('2nd period fouls'),null=True)
    block_3th = models.PositiveIntegerField(
                                    _('3th period blocks'),null=True)
    hit_3th = models.PositiveIntegerField(
                                    _('3th period hits'),null=True)
    foul_3th = models.PositiveIntegerField(
                                    _('3th period fouls'),null=True)
    block_all = models.PositiveIntegerField(
                                    _('All periods blocks'),null=True)
    hit_all = models.PositiveIntegerField(
                                    _('All periods hits'),null=True)
    foul_all = models.PositiveIntegerField(
                                    _('All periods fouls'),null=True)

    def __unicode__ (self):
        if self.clubplayermatch:
            return '{} {}'.format(
                                    self.clubplayermatch.clubplayer or '',
                                    self.clubplayermatch or self.pk,
                                )
        return self.pk

    class Meta:
        verbose_name=_('Player Stats')
        verbose_name_plural=_('Players Stats')


class ClubPlayerMatch(models.Model):
    b'''
        связка игрок в клубе в сезоне с матчем в сезоне
        По сути статистика игрока в каждом матче
    '''
    objects = managers.match.ClubPlayerMatchQuerySet.as_manager()
    clubplayer = models.ForeignKey(ClubPlayer)
    match = models.ForeignKey('hockeyapp.Match')
    adv_stats = models.OneToOneField(AdvancedPlayerStats, null=True, blank=True)
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
    sf = models.FloatField(_('Safety Factor'), null=True)
    gamingtime = models.PositiveIntegerField(_('Gaming time'), null=True)

    __unicode__ = lambda self: '{}'.format(self.match or self.pk,)

    @property
    def match_date(self):
        return self.match.date

    class Meta:
        verbose_name=_('Club Player History Match')
        verbose_name_plural=_('Club Player Histories in Matches')


class MatchGoalHistory(models.Model):
    b'''Хранит историю матча. Заброшенные шайбы'''
    objects = managers.match.MatchGoalHistoryQuerySet.as_manager()
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
    guest_five_numbers = models.CharField(max_length=1024, blank=True)

    __unicode__ = lambda self: '{}'.format(self.pk,)

    @property
    def gamingtime(self):
        ''' returns gamingtime in seconds '''
        time = datetime.datetime.strptime(self.time, '%H:%M').time()
        return (time.hour * 60 + time.minute) * 60

    class Meta:
        verbose_name=_('Match goal entry')
        verbose_name_plural=_('Match goal entries')


class MatchPenaltyHistory(models.Model):
    b'''Хранит историю матча. Заброшенные шайбы'''
    objects = managers.match.MatchPenaltyHistoryManager()
    match = models.ForeignKey('hockeyapp.Match')
    player = models.ForeignKey(Player, related_name='penaltymatch')
    ptype = models.CharField(max_length=1024, blank=True)
    time = models.CharField(max_length=32, blank=True)
    duration = models.CharField(max_length=32, blank=True)

    __unicode__ = lambda self: '{}'.format(self.pk,)

    class Meta:
        verbose_name=_('Match penalty entry')
        verbose_name_plural=_('Match penalty entries')


class Match(AdminLinkMixin, TitleBaseModel):
    objects = managers.match.MatchManager()
    #service info
    khl_id = models.PositiveIntegerField(_('Other site ID'), null=True)
    challenge_type = models.PositiveSmallIntegerField(_('Challenge Type'),
                                null=True, choices=CHALLENGE_TYPE)
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    #main info
    spectators = models.PositiveIntegerField(_('Spectators count'), null=True)
    spectators_str = models.CharField(_('Spectators count'), max_length=1024,
                                    blank=True)
    date_str = models.CharField(_('Match date'), max_length=1024, blank=True)
    date = models.DateTimeField(_('Match date'), null=True, blank=True)
    count = models.CharField(_('Match count'), max_length=1024, blank=True)
    detail_count = models.CharField(_('Match detail count'), 
                                    max_length=1024, blank=True)
    judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchjudges',
                            verbose_name=Judge._meta.verbose_name_plural)
    line_judges = models.ManyToManyField(Judge, null=True, blank=True,
                            related_name='matchlinejudges',
                            verbose_name=_('Line judges'))
    home_team = models.ForeignKey(Club, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='homematches',
                                verbose_name=_('Home team'))
    home_coach = models.ForeignKey(Coach, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='homematches')
    home_players = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    related_name='homematches')
    guest_team = models.ForeignKey(Club, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='guestmatches',
                                verbose_name=_('Guest team'))
    guest_coach = models.ForeignKey(Coach, null=True, blank=True,
                                    on_delete=models.SET_NULL,
                                    related_name='guestmatches')
    guest_players = models.ManyToManyField(ClubPlayer, null=True, blank=True,
                                    related_name='guestmatches')

    league = models.ForeignKey(League, null=True, blank=True,
                                on_delete=models.SET_NULL,)

    class Meta:
        verbose_name=_('Match')
        verbose_name_plural=_('Matches')
        ordering = '-khl_id',

    def __unicode__(self):
        if self.count and self.date and self.home_team and self.guest_team:
            return '{} {} {} ({})'.format(self.home_team,
                                        self.count,
                                        self.guest_team,
                                        self.date)
        return self.ru_title


class Challenge(TitleBaseModel):
    khl_id = models.PositiveIntegerField(_('Other site calendar ID'))
    url = models.URLField('Challenge calendar for parsing', blank=True)
    parser_type = models.CharField('Parser', blank=True, max_length=255,
                                    choices=PARSERS)
    challenge_type = models.PositiveSmallIntegerField(_('Challenge Type'),
                                null=True, choices=CHALLENGE_TYPE)
    season = models.ForeignKey(Season, null=True, blank=True)
    league = models.ForeignKey(League)
    processed = models.BooleanField(default=False)
    proccesed_time = models.DateTimeField(_('Processed time'), auto_now=True,
                                            null=True)

    @property
    def match_parser(self):
        return {
                'KHLScheduleParser': parsers.match.HockeyKHLMatchParser,
                'VHLScheduleParser': parsers.match.HockeyVHLMatchParser,
                'MHLScheduleParser': parsers.match.HockeyMHLMatchParser,
                'MHL2ScheduleParser': parsers.match.HockeyMHL2MatchParser,
            }.get(self.parser_type)

    def match_url(self, match_id):
        return {
                'KHLScheduleParser': 'http://www.khl.ru/game/{}/{}/protocol/',
                'VHLScheduleParser': 'http://www.vhlru.ru/report/{}/?idgame={}',
                'MHLScheduleParser': 'http://mhl.khl.ru/report/{}/?idgame={}',
                'MHL2ScheduleParser': 'http://mhl2.khl.ru/report/{}/?idgame={}',
            }.get(self.parser_type).format(self.khl_id, match_id)

    class Meta:
        verbose_name=_('Challenge')
        verbose_name_plural=_('Challenges')


class Schedule(TitleBaseModel):
    objects = managers.ScheduleManager()
    khl_id = models.PositiveIntegerField(_('Other site ID'), null=True,)
    match_url = models.URLField('Match Other site url', blank=True)
    date = models.DateTimeField(_('Match date'), null=True, blank=True)
    challenge = models.ForeignKey(Challenge, null=True,
                                verbose_name=Challenge._meta.verbose_name,
                                on_delete=models.SET_NULL,)
    challenge_type = models.PositiveSmallIntegerField(_('Challenge Type'),
                                null=True, choices=CHALLENGE_TYPE)
    #relations
    season = models.ForeignKey(Season, null=True, blank=True)
    league = models.ForeignKey(League, null=True, blank=True)
    match = models.OneToOneField(Match, null=True, blank=True,
                                on_delete=models.SET_NULL,)
    home_team = models.ForeignKey(Club, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='schedule_homematches',
                                verbose_name=_('Home team'))
    guest_team = models.ForeignKey(Club, null=True, blank=True,
                                on_delete=models.SET_NULL,
                                related_name='schedule_guestmatches',
                                verbose_name=_('Guest team'))
    processed = models.BooleanField(default=False)
    proccesed_time = models.DateTimeField(_('Processed time'), auto_now=True,
                                            null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.match_url and self.challenge and self.khl_id:
            self.match_url = self.challenge.match_url(self.khl_id)
        super(Schedule, self).save(*args, **kwargs)

    class Meta:
        verbose_name=_('League Schedule')
        verbose_name_plural=_('League Schedules')
        ordering = 'date',


class Name(models.Model):
    b'''Словарь имен/фамилий'''
    type = models.SmallIntegerField(choices=(
        (0, (_('First Name'))),
        (1, (_('Last Name'))),
    ))
    ru_name = models.CharField(
        _('Name (rus)'), max_length=4096, blank=True)
    en_name = models.CharField(
        _('Name (en)'), max_length=4096, blank=True)

    def __unicode__(self):
        return '%s: %s / %s' % (self.type, self.ru_name, self.en_name)

    class Meta(object):
        verbose_name = _('Name')
        verbose_name_plural = _('Names')


class Timeline(LocaleAttrMixin, models.Model):
    start_date = models.DateTimeField(_('Start date'), blank=True, null=True)
    end_date = models.DateTimeField(_('End date'), blank=True, null=True)
    ru_headline = models.CharField(
        _('Headline (RU)'), max_length=255, blank=True, null=True)
    en_headline = models.CharField(
        _('Headline (EN)'), max_length=255, blank=True, null=True)
    ru_text = models.TextField(_('Text (RU)'), blank=True, null=True)
    en_text = models.TextField(_('Text (EN)'), blank=True, null=True)
    media = FilerImageField(verbose_name=_('Media'), null=True, blank=True)
    ru_media_credit = models.CharField(
        _('Media credit (RU)'), max_length=255, blank=True, null=True)
    en_media_credit = models.CharField(
        _('Media credit (EN)'), max_length=255, blank=True, null=True)
    ru_media_caption = models.CharField(
        _('Media caption (RU)'), max_length=255, blank=True, null=True)
    en_media_caption = models.CharField(
        _('Media caption (EN)'), max_length=255, blank=True, null=True)
    type = models.CharField(
        _('Type'), max_length=255, blank=True, null=True)
    tag = models.CharField(
        _('Tag'), max_length=255, blank=True, null=True)

    # related objects
    player = models.ForeignKey(
        Player, verbose_name=_('Player'), on_delete=models.SET_NULL,
        blank=True, null=True)
    club = models.ForeignKey(
        Club, verbose_name=_('Club'), on_delete=models.SET_NULL,
        blank=True, null=True)

    class Meta(object):
        ordering = 'start_date',
        verbose_name = _('Timeline event')
        verbose_name_plural = _('Timeline events')
