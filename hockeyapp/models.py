#coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from addresses.models import Address, Country
from base.models import LocaleAttrMixin, TitleBaseModel, AdminLinkMixin, Season

from .choices import PLAYER_ROLE, PARITY_VALUES, CONTRACT_TYPE, FIVER_VALUES
from . import managers


class AbstractMan(LocaleAttrMixin, models.Model):
    ru_fio = models.CharField(_('Full name (rus)'), max_length=4096, blank=True)
    ru_name = models.CharField(_('Name (rus)'), max_length=4096, blank=True, null=True)
    ru_lastname = models.CharField(_('Last name (rus)'), max_length=4096, blank=True, null=True)
    en_fio = models.CharField(_('Full name (en)'), max_length=4096, blank=True)
    en_name = models.CharField(_('Name (en)'), max_length=4096, blank=True, null=True)
    en_lastname = models.CharField(_('Last name (en)'), max_length=4096, blank=True, null=True)
    birth_date = models.DateField(_('Birth date'), null=True, blank=True)
    death_date = models.DateField(_('Death date'), null=True, blank=True)
    wiki_page = models.URLField('Wiki page URL', blank=True, max_length=1024)
    khl_id = models.PositiveIntegerField(default=0, null=True)
    __unicode__ = lambda self: self.ru_fio

    def save(self, **kwargs):
        if self.ru_fio and (not self.ru_name or not self.ru_lastname):
            self.ru_name, sep, self.ru_lastname = self.ru_fio.partition(' ')
        if self.en_fio and (not self.en_name or not self.en_lastname):
            self.en_name, sep, self.en_lastname = self.en_fio.partition(' ')
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
    weight = models.CharField(_('Weight'), max_length=32, blank=True)
    height = models.CharField(_('Height'), max_length=32, blank=True)
    grip = models.CharField(_('Grip'), max_length=32, blank=True)
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)

    #serviceinfo
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    __unicode__ = lambda self: '{0} {1}'.format(self.khl_id, self.ru_fio)

    def save(self, **kwargs):
        if self.pk and not self.line:
            #смотрим амплуа игрока из истории 
            if self.clubplayer_set.exists():
                self.line = self.clubplayer_set.all().last().line
        super(Player, self).save(**kwargs)

    @property
    def club(self):
        return self.club_set.all().last()

    @property
    def last_clubs(self):
        last_club_ids = set(
            self.clubplayer_set
            .exclude(club=self.club)  # exclude current club
            .order_by('-end_date')
            .values_list('club_id', flat=True))
        clubs = list(Club.objects.filter(pk__in=last_club_ids))
        clubs.sort(key=lambda x: last_club_ids.index(x.pk))
        if self.club_set.exists():
            clubs.insert(0, self.club)
        return clubs

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


class Coach(AbstractMan):
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)
    class Meta:
        verbose_name=_('Coach')
        verbose_name_plural=_('Coaches')


class Judge(AbstractMan):
    citizenship = models.ForeignKey(Country, verbose_name=_('Citizenship'),
                                            on_delete=models.SET_NULL,
                                            null=True, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)
    class Meta:
        verbose_name=_('Judge')
        verbose_name_plural=_('Judges')


class Arena(TitleBaseModel):
    objects = managers.arena.ArenaManager()
    capacity = models.PositiveIntegerField(_('Capacity'), null=True)
    capacity_str = models.CharField(_('Capacity'), max_length=1024, blank=True)
    coords = models.CharField(_('Latitude and Longitude'),
                                max_length=1024, blank=True)
    site = models.URLField(_('Site'), blank=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    tickets_url = models.URLField(_('Tickets'), blank=True)
    photo = FilerImageField(verbose_name=_('Main photo'), null=True, blank=True)
    country = models.ForeignKey(Country, null=True, blank=True,
                                verbose_name=Country._meta.verbose_name,)
    league = models.ForeignKey('League', null=True, blank=True)

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


class League(TitleBaseModel):
    country = models.ForeignKey(Country, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    class Meta:
        verbose_name=_('League')
        verbose_name_plural=_('Leagues')


class Club(TitleBaseModel):
    objects = managers.club.ClubQuerySet.as_manager()
    opening_dt = models.DateField(_('Founding date'), null=True, blank=True)
    closing_dt = models.DateField(_('Closing date'), null=True, blank=True)
    logo = FilerImageField(verbose_name=_('Logo'), null=True, blank=True,
                            on_delete=models.SET_NULL)
    site = models.URLField(_('Site'), blank=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    style = models.TextField(_('Styles (CSS)'), blank=True, null=True)

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

    class Meta:
        verbose_name = _('Club')
        verbose_name_plural = _('Clubs')


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
    photo = FilerImageField(verbose_name=_('Photo'))
    addressclub = models.ForeignKey(AddressClub, 
                                    verbose_name=AddressClub._meta.verbose_name)


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
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    number = models.PositiveIntegerField(_('Number'), default=0)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)
    season = models.ForeignKey( Season, null=True, blank=True,
                                on_delete=models.SET_NULL,)

    __unicode__ = lambda self: '{0} ({1})'.format(self.player, self.club)

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



# class ClubPlayerMatchQuerySet(models.QuerySet):
#     def plus_minus(self):
#         return self.aggregate(models.Sum('plus_minus')).get('plus_minus__sum', 0)


class ClubPlayerMatch(models.Model):
    b'''
        связка игрок в клубе в сезоне с матчем в сезоне
        По сути статистика игрока в каждом матче
    '''
    # objects = ClubPlayerMatchQuerySet.as_manager()
    clubplayer = models.ForeignKey(ClubPlayer)
    match = models.ForeignKey('hockeyapp.Match')
    adv_stats = models.OneToOneField(AdvancedPlayerStats, null=True, blank=True)
    goals = models.SmallIntegerField(_('Goals'), null=True)
    assists = models.SmallIntegerField(_('Assists'), null=True)
    points = models.SmallIntegerField(_('Points'), null=True)
    plus_minus = models.SmallIntegerField('+/-', null=True)
    plus_minus_str = models.CharField('+/-', max_length=8, blank=True)
    penalty_time = models.PositiveIntegerField(_('Penalty Time'), null=True)
    penalty_time_str = models.CharField(_('Penalty Time'), max_length=8, blank=True)
    ev_goals = models.PositiveSmallIntegerField(_('EV Goals'), null=True)
    ev_goals_str = models.CharField(_('EV Goals'), max_length=8, blank=True)
    pp_goals = models.PositiveSmallIntegerField(_('Power Play Goals'), null=True)
    pp_goals_str = models.CharField(_('Power Play Goals'), max_length=8, blank=True)
    es_goals = models.PositiveSmallIntegerField(_('Even Strength Goals'), null=True)
    es_goals_str = models.CharField(_('Even Strength Goals'),
                                max_length=8, blank=True)
    overtime_goals = models.PositiveSmallIntegerField(_('Overtime Goals'), null=True)
    overtime_goals_str = models.CharField(_('Overtime Goals'),
                                max_length=8, blank=True)
    win_goals = models.PositiveSmallIntegerField(_('Win Goals'), null=True)
    win_goals_str = models.CharField(_('Win Goals'), max_length=8,  blank=True)
    bullet_goals = models.PositiveSmallIntegerField(_('Win Bullet Goals'), null=True)
    bullet_goals_str = models.CharField(_('Win Bullet Goals'), 
                                max_length=8, blank=True)
    shots = models.PositiveSmallIntegerField(_('Shots count'), null=True)
    shots_str = models.CharField(_('Shots count'), max_length=8, blank=True)
    pis = models.FloatField(_('Implemented Shots, %'), null=True)
    pis_str = models.CharField(_('Implemented Shots, %'),
                                max_length=8, blank=True)
    faceoff = models.PositiveSmallIntegerField(_('Face-off'), null=True)
    faceoff_str = models.CharField(_('Face-off'), max_length=8, blank=True)
    winfaceoff = models.PositiveSmallIntegerField(_('Face-off Wins'), null=True)
    winfaceoff_str = models.CharField(_('Face-off Wins'), max_length=8, blank=True)
    winfaceoff_p = models.FloatField(_('Face-off Wins, %'), null=True)
    winfaceoff_p_str = models.CharField(_('Face-off Wins, %'),
                                max_length=8, blank=True)
    #khl adv stats
    change_count = models.PositiveIntegerField(_('Change count'),null=True)
    hits = models.PositiveIntegerField(_('Hits'),null=True)
    blocks = models.PositiveIntegerField(_('Blocks'),null=True)
    fouls = models.PositiveIntegerField(_('Fouls'),null=True)
    #keeper stats
    loose_goals = models.PositiveSmallIntegerField(_('Loose Goals'), null=True)
    loose_goals_str = models.CharField(_('Loose Goals'), max_length=8,  blank=True)
    saves = models.PositiveSmallIntegerField(_('Saves Goals'), null=True)
    saves_str = models.CharField(_('Saves Goals'), max_length=8, blank=True)
    saves_p = models.FloatField(_('Saves Goals , %'), null=True)
    saves_p_str = models.CharField(_('Saves Goals , %'),
                                max_length=8, blank=True)
    sf = models.FloatField(_('Safety Factor'), null=True)
    sf_str = models.CharField(_('Safety Factor'), max_length=8, blank=True)
    gamingtime = models.PositiveIntegerField(_('Gaming time'), null=True)
    gamingtime_str = models.CharField(_('Gaming time'), max_length=8, blank=True)

    __unicode__ = lambda self: '{}'.format(self.match or self.pk,)

    @property
    def match_date(self):
        return self.match.date

    class Meta:
        verbose_name=_('Club Player History Match')
        verbose_name_plural=_('Club Player Histories in Matches')


class MatchGoalHistory(models.Model):
    b'''Хранит историю матча. Заброшенные шайбы'''
    objects = managers.match.MatchGoalHistoryManager()
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
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
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


class Schedule(TitleBaseModel):
    objects = managers.ScheduleManager()
    khl_id = models.PositiveIntegerField(_('Other site ID'), null=True,)
    date = models.DateTimeField(_('Match date'), null=True, blank=True)
    is_championship = models.BooleanField(_('Is championship'), default=True)
    is_playoff = models.BooleanField(_('Is playoff'), default=False)
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
    proccesed_time = models.DateTimeField(_('Processed time'),
                                            null=True, blank=True)
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
        verbose_name=_('Name')
        verbose_name_plural=_('Names')
