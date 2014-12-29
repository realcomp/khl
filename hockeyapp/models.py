#coding: utf-8
from __future__ import unicode_literals
import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from addresses.models import Address, Country
from base.models import TitleBaseModel

from .choices import PLAYER_ROLE, PARITY_VALUES
from .defaults import MD
from . import managers


class AbstractMan(models.Model):
    ru_fio = models.CharField(_('Full name (rus)'), max_length=4096, blank=True)
    en_fio = models.CharField(_('Full name (en)'), max_length=4096, blank=True)
    __unicode__ = lambda self: self.ru_fio
    class Meta:
        abstract=True

class Player(AbstractMan):
    objects = managers.player.PlayerManager()
    khl_id = models.PositiveIntegerField(default=0)
    line = models.PositiveSmallIntegerField(_('Line'), default=0,
                                            choices=PLAYER_ROLE)
    birth_date = models.DateField(_('Birth date'), null=True, blank=True)
    weight = models.CharField(_('Weight'), max_length=32, blank=True)
    height = models.CharField(_('Height'), max_length=32, blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)

    #serviceinfo
    proccesed_time = models.DateTimeField(_('Processed time'),auto_now_add=True)
    url = models.URLField('URL', blank=True)
    html_body = models.TextField('Parse HTML', blank=True)

    __unicode__ = lambda self: '{0} {1}'.format(self.khl_id, self.ru_fio)

    @property
    def club(self):
        return self.club_set.latest('pk')

    @property
    def previous_clubs(self):
        previous_club_ids = self.clubplayer_set.values_list(
            'club_id', flat=True)
        current_club_ids = self.club_set.values_list('id', flat=True)
        return (
            Club.objects
            .exclude(pk__in=current_club_ids)
            .filter(pk__in=previous_club_ids)[:8])

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


class Arena(TitleBaseModel):
    objects = managers.arena.ArenaManager()
    capacity = models.CharField(_('Capacity'), max_length=1024, blank=True)
    site = models.URLField(_('Site'), blank=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    tickets_url = models.URLField(_('Tickets'), blank=True)
    photo = FilerImageField(verbose_name=_('Photo'), null=True, blank=True)

    class Meta:
        verbose_name=_('Arena')
        verbose_name_plural=_('Arenas')


class League(TitleBaseModel):
    country = models.ForeignKey(Country, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    class Meta:
        verbose_name=_('League')
        verbose_name_plural=_('Leagues')


class Club(TitleBaseModel):
    objects = managers.club.ClubManager()
    opening_dt = models.DateField(_('Founding date'), null=True, blank=True)
    closing_dt = models.DateField(_('Closing date'), null=True, blank=True)
    logo = FilerImageField(verbose_name=_('Logo'), null=True, blank=True,
                            on_delete=models.SET_NULL)
    site = models.URLField(_('Site'), blank=True)
    contacts = models.TextField(_('Contacts'), blank=True)
    #relation
    address = models.ForeignKey(Address, null=True, blank=True,
                                    on_delete=models.SET_NULL)
    coach = models.ForeignKey(Coach, null=True, blank=True,
                                    on_delete=models.SET_NULL)
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

    @property
    def all_players(self):
        player_ids = self.clubplayer_set.values_list('player_id', flat=True)
        return Player.objects.filter(pk__in=player_ids)

    @property
    def current_offender_players(self):
        return self.players.filter(line=3)

    @property
    def current_defender_players(self):
        return self.players.filter(line=2)

    @property
    def current_goalkeeper_players(self):
        return self.players.filter(line=1)

    class Meta:
        verbose_name = _('Club')
        verbose_name_plural = _('Clubs')


class AddressClub(models.Model):
    b''' связка адрес - клуб в сезоне '''
    address = models.ForeignKey(Address)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)

    class Meta:
        verbose_name=_('Club address')
        verbose_name_plural=_('Club addresses')


class LeagueClub(models.Model):
    b''' связка лига - клуб в сезоне '''
    league = models.ForeignKey(League)
    club = models.ForeignKey(Club)
    start_date = models.DateField(_('Start date'), null=True, blank=True)
    end_date = models.DateField(_('End date'), null=True, blank=True)

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


class LogoClubHistory(models.Model):
    b''' связка тренер клуб в сезоне '''
    club = models.ForeignKey(Club)
    logo = FilerImageField(verbose_name=_('Logo'))
    start_date = models.DateField(_('Start date'), null=True)
    end_date = models.DateField(_('End date'), null=True)
    class Meta:
        verbose_name=_('Logo Club History')
        verbose_name_plural=_('Logo Club Histories')


class AdvancedPlayerStats(models.Model):
    b''' Дополнительная статистика по игроку в матче '''
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
    change_count_1th = models.CharField(_('1th period change count'),
                                    max_length=16, blank=True)
    gamingtime_1th = models.CharField(_('1th period time in game'),
                                    max_length=16, blank=True)
    change_count_2nd = models.CharField(_('2nd period change count'),
                                    max_length=16, blank=True)
    gamingtime_2nd = models.CharField(_('2nd period change count'),
                                    max_length=16, blank=True)
    change_count_3th = models.CharField(_('3th period change count'),
                                    max_length=16, blank=True)
    gamingtime_3th = models.CharField(_('3th period time in game'),
                                    max_length=16, blank=True)
    change_count_all = models.CharField(_('All periods change count'),
                                    max_length=16, blank=True)
    gamingtime_all = models.CharField(_('All periods time in game'),
                                    max_length=16, blank=True)
    block_1th = models.CharField(_('1th period blocks'),
                                    max_length=16, blank=True)
    hit_1th = models.CharField(_('1th period hits'),
                                    max_length=16, blank=True)
    foul_1th = models.CharField(_('1th period fouls'),
                                    max_length=16, blank=True)
    block_2nd = models.CharField(_('2nd period blocks'),
                                    max_length=16, blank=True)
    hit_2nd = models.CharField(_('2nd period hits'),
                                    max_length=16, blank=True)
    foul_2nd = models.CharField(_('2nd period fouls'),
                                    max_length=16, blank=True)
    block_3th = models.CharField(_('3th period blocks'),
                                    max_length=16, blank=True)
    hit_3th = models.CharField(_('3th period hits'),
                                    max_length=16, blank=True)
    foul_3th = models.CharField(_('3th period fouls'),
                                    max_length=16, blank=True)
    block_all = models.CharField(_('All periods blocks'),
                                    max_length=16, blank=True)
    hit_all = models.CharField(_('All periods hits'),
                                    max_length=16, blank=True)
    foul_all = models.CharField(_('All periods fouls'),
                                    max_length=16, blank=True)

    class Meta:
        verbose_name=_('Player Stats')
        verbose_name_plural=_('Players Stats')


class ClubPlayerMatch(models.Model):
    b'''
        связка игрок в клубе в сезоне с матчем в сезоне
        По сути статистика игрока в каждом матче
    '''
    clubplayer = models.ForeignKey(ClubPlayer)
    match = models.ForeignKey('hockeyapp.Match')
    adv_stats = models.OneToOneField(AdvancedPlayerStats, null=True, blank=True)
    plus_minus = models.CharField('+/-', max_length=8, blank=True)
    penalty_time = models.CharField(_('Penalty Time'), max_length=8, blank=True)
    ev_goals = models.CharField(_('EV Goals'), max_length=8, blank=True)
    pp_goals = models.CharField(_('Power Play Goals'), max_length=8, blank=True)
    es_goals = models.CharField(_('Even Strength Goals'),
                                max_length=8, blank=True)
    overtime_goals = models.CharField(_('Overtime Goals'),
                                max_length=8, blank=True)
    win_goals = models.CharField(_('Win Goals'), max_length=8,  blank=True)
    bullet_goals = models.CharField(_('Win Bullet Goals'), 
                                max_length=8, blank=True)
    shots = models.CharField(_('Shots count'), max_length=8, blank=True)
    pis = models.CharField(_('Percentage of Implemented Shots'),
                                max_length=8, blank=True)
    faceoff = models.CharField(_('Face-off'), max_length=8, blank=True)
    winfaceoff = models.CharField(_('Face-off Wins'), max_length=8, blank=True)
    winfaceoff_p = models.CharField(_('Face-off Wins Percentage'),
                                max_length=8, blank=True)
    #keeper stats
    loose_goals = models.CharField(_('Loose Goals'), max_length=8,  blank=True)
    saves = models.CharField(_('Saves Goals'), max_length=8, blank=True)
    saves_p = models.CharField(_('Saves Goals Percentage'),
                                max_length=8, blank=True)
    sf = models.CharField(_('Safety Factor'), max_length=8, blank=True)
    gamingtime = models.CharField(_('Gaming time'), max_length=8, blank=True)

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
    class Meta:
        verbose_name=_('Match penalty entry')
        verbose_name_plural=_('Match penalty entries')


class Match(TitleBaseModel):
    objects = managers.match.MatchManager()
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

    class Meta:
        verbose_name=_('Match')
        verbose_name_plural=_('Matches')
        ordering = '-khl_id',

    @property
    def python_date(self):
        if self.date:
            _date_dict = self.date.strip().lower().split(',')
            _dt = _date_dict[:2]
            _dt.append(_date_dict[3])
            _date_dict = _dt
            _m = _date_dict[0].split()[1].encode('utf-8')
            _date_dict[0] = _date_dict[0].replace(_m.decode('utf-8'), MD.get(_m))
            if _date_dict[-1] != '':
                mask = '%d %m %Y %H:%M'
            else:
                mask = '%d %m %Y'
            _dt = ''.join(_date_dict).encode('utf-8')
            return datetime.datetime.strptime(_dt, mask)
