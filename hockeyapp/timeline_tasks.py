#coding: utf-8
from __future__ import unicode_literals, print_function

import datetime
import itertools
import operator

from celery import Task
from celery.utils.log import get_task_logger
logger = get_task_logger(__name__)

from django.db.models import Q
from django.utils import timezone
tz = timezone.get_current_timezone()

from . import models


class PlayerTimelineGenerator(Task):
    ignore_result=True
    track_started=True

    def run(self, ids, *args, **kwargs):
        self.players = models.Player.objects.filter(pk__in=ids)
        self.birthday_events()
        self.first_goal_event()
        self.first_hat_trick_event()
        self.first_poker_event()
        self.first_0_loose_goals_event()
        self.first_loose_goal_event()
        self.first_match_event()
        self.goals_events()
        self.points_events()
        self.matches_events()
        self.club_matches_events()
        self.club_change_events()
        self.first_club_goal_event()
        self.series_0_loose_goals_event()
        
    def date2datetime(self, date):
        dt = datetime.datetime(date.year, date.month, date.day, 12, 0, 0)
        return timezone.make_aware(dt, tz)

    def birthday_events(self):
        players = self.players.filter(birth_date__isnull=False)
        players_pks = models.Timeline.objects.filter(type='birthday'
                                    ).values_list('player_id', flat=True)
        for player in players.exclude(pk__in=players_pks):
            models.Timeline.objects.create(
                start_date=self.date2datetime(player.birth_date),
                ru_headline='День рождения',
                en_headline='Birth day',
                ru_text='День рождения',
                en_text='Birth day',
                media=player.photo,
                type='birthday',
                player=player)

    def first_event(self, **kwargs):
        ''' abstract 1st event factory '''
        players_pks = models.Timeline.objects.filter(type=kwargs['type']
                            ).values_list('player_id', flat=True)
        for player in self.players.exclude(pk__in=players_pks):
            date = kwargs['date_query'](player)
            if date:
                models.Timeline.objects.create(
                    start_date=date,
                    ru_headline=kwargs['ru_headline'],
                    en_headline=kwargs['en_headline'],
                    ru_text=kwargs['ru_text'],
                    en_text=kwargs['en_text'],
                    media=player.photo,
                    type=kwargs['type'],
                    player=player)

    def first_goal_event(self):
        def date_query(player):
            obj = models.MatchGoalHistory.objects.is_active(
                                         ).filter(scorer=player
                                         ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_goal',
            date_query=date_query,
            date_model=models.MatchGoalHistory,
            ru_headline='Первая шайба в карьере',
            en_headline='First goal in career',
            ru_text='Первая шайба в карьере',
            en_text='First goal in career')

    def first_hat_trick_event(self):
        def date_query(player):
            obj = models.ClubPlayerMatch.objects.is_active(
                                    ).filter(clubplayer__player=player, goals=3
                                    ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_hat_trick',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "хет-трик" в карьере',
            en_headline='First hat trick in career',
            ru_text='Первый "хет-трик" в карьере',
            en_text='First hat trick in career')

    def first_poker_event(self):
        def date_query(player):
            obj = models.ClubPlayerMatch.objects.is_active(
                                    ).filter(clubplayer__player=player, goals=4
                                    ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_poker',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "покер" в карьере',
            en_headline='First poker in career',
            ru_text='Первый "покер" в карьере',
            en_text='First poker in career')

    def first_0_loose_goals_event(self):
        def date_query(player):
            # line=1 goalkeeper
            obj = models.ClubPlayerMatch.objects.is_active(
                                    ).filter(   clubplayer__player=player,
                                                clubplayer__line=1,
                                                loose_goals=0,
                                                gamingtime__gte=58*60
                                    ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_0_loose_goals',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый "сухарь" в карьере',
            en_headline='First 0 loose goals in career',
            ru_text='Первый "сухарь" в карьере',
            en_text='First 0 loose goals in career')


    def first_loose_goal_event(self):
        def date_query(player):
            # line=1 goalkeeper
            obj = models.ClubPlayerMatch.objects.is_active(
                                    ).filter(   clubplayer__player=player,
                                                clubplayer__line=1,
                                                loose_goals__gte=1
                                    ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_loose_goal',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый гол в карьере',
            en_headline='First loose goal in career',
            ru_text='Первый гол в карьере',
            en_text='First loose goal in career')

    def first_match_event(self):
        def date_query(player):
            obj = models.ClubPlayerMatch.objects.is_active(
                                    ).filter(clubplayer__player=player
                                    ).order_by('match__date').first()
            return obj and obj.match and obj.match.date

        self.first_event(
            type='first_match',
            date_query=date_query,
            date_model=models.ClubPlayerMatch,
            ru_headline='Первый матч в карьере',
            en_headline='First match in career',
            ru_text='Первый матч в карьере',
            en_text='First match in career')

    def goals_events(self):
        for player in self.players:
            count = models.Timeline.objects.filter(type='goals', player=player
                                    ).count()
            goals = models.MatchGoalHistory.objects.filter(scorer=player
                                    ).order_by('match__date')
            if goals.count() > 0 and goals.count() / 50 > count:
                for i, goal in enumerate(goals):
                    if i + 1 > count * 50 and not (i + 1) % 50:
                        models.Timeline.objects.create(
                            start_date=goal.match.date,
                            ru_headline='%d-я шайба в карьере' % (i + 1),
                            en_headline='%dth goal in career' % (i + 1),
                            ru_text='%d-я шайба в карьере' % (i + 1),
                            en_text='%dth goal in career' % (i + 1),
                            media=player.photo,
                            type='goals',
                            player=player)

    def points_events(self):
        for player in self.players:
            matches = models.ClubPlayerMatch.objects.is_active(
                            ).filter(clubplayer__player=player
                            ).exclude(points=0
                            ).order_by('match__date')
            i = 0
            target = 50
            for match in matches:
                i += match.points or 0
                if i >= target:
                    target += 50
                    if not models.Timeline.objects.filter(
                            start_date=match.match.date,
                            type='points',
                            player=player).exists():
                        models.Timeline.objects.create(
                            start_date=match.match.date,
                            ru_headline='%d-е очко в карьере' % i,
                            en_headline='%dth point in career' % i,
                            ru_text='%d-е очко в карьере' % i,
                            en_text='%dth point in career' % i,
                            media=player.photo,
                            type='points',
                            player=player)

    def matches_events(self):
        for player in self.players:
            count = models.Timeline.objects.filter(type='matches', player=player
                        ).count()
            matches = models.ClubPlayerMatch.objects.is_active(
                            ).filter(clubplayer__player=player
                            ).order_by('match__date')
            if matches.count() > 0 and matches.count() / 50 > count:
                for i, match in enumerate(matches):
                    if i + 1 > count * 50 and not (i + 1) % 50:
                        models.Timeline.objects.create(
                            start_date=match.match.date,
                            ru_headline='%d-й матч в карьере' % (i + 1),
                            en_headline='%dth match in career' % (i + 1),
                            ru_text='%d-й матч в карьере' % (i + 1),
                            en_text='%dth match in career' % (i + 1),
                            media=player.photo,
                            type='matches',
                            player=player)

    def club_matches_events(self):
        for player in self.players:
            matches = models.ClubPlayerMatch.objects.is_active(
                        ).filter(clubplayer__player=player
                        ).order_by('match__date')
            clubs = models.Club.objects.filter(
                        Q(pk__in=matches.values_list('match__home_team_id')) |
                        Q(pk__in=matches.values_list('match__guest_team_id'))
                    )
            for club in set(clubs):
                count = models.Timeline.objects.filter(
                                type='club_matches', player=player, club=club
                            ).count()
                matches = models.ClubPlayerMatch.objects.is_active(
                                ).filter(clubplayer__player=player
                                ).by_club(club, player
                                ).order_by('match__date'
                                ).distinct()
                if matches.count() > 0 and matches.count() / 100 > count:
                    for i, match in enumerate(matches):
                        if i + 1 > count * 100 and not (i + 1) % 100:
                            ru_club = club.ru_title
                            en_club = club.en_title
                            models.Timeline.objects.create(
                                start_date=match.match.date,
                                ru_headline='%d-й матч в клубе "%s"' % ((i + 1), ru_club),
                                en_headline='%dth match in a club "%s"' % ((i + 1), en_club),
                                ru_text='%d-й матч в клубе "%s"' % ((i + 1), ru_club),
                                en_text='%dth match in a club "%s"' % ((i + 1), ru_club),
                                media=club.logo,
                                type='club_matches',
                                player=player,
                                club=club)

    def club_change_events(self):
        for player in self.players:
            clubplayers = player.clubplayer_set.all().order_by('start_date')
            timelines = models.Timeline.objects.filter(
                type='club_change', player=player)
            if timelines.exists():
                # ~Q & ~Q & ~Q
                q_existing = reduce(operator.and_, map(
                    lambda x: ~Q(   start_date__gte=x.start_date.date(),
                                    end_date__lte=x.end_date.date()),
                    timelines))
                clubplayers = clubplayers.filter(q_existing)
            # group by club
            timelines = {}
            for clubplayer in clubplayers:
                ru_club = clubplayer.club.ru_title
                en_club = clubplayer.club.en_title
                url = clubplayer.club_url
                timeline = models.Timeline(
                    start_date=self.date2datetime(clubplayer.start_date),
                    end_date=self.date2datetime(clubplayer.end_date),
                    ru_headline='В составе клуба "%s"' % ru_club,
                    en_headline='Membership in a club "%s"' % en_club,
                    ru_text='В составе клуба "%s"' % ru_club,
                    en_text='Membership in a club "%s"' % en_club,
                    media=clubplayer.club.logo,
                    ru_media_caption='<a href="%s">%s</a>' % (url, ru_club),
                    en_media_caption='<a href="%s">%s</a>' % (url, en_club),
                    type='club_change',
                    player=player,
                    club=clubplayer.club)

                if clubplayer.club.pk not in timelines:
                    timelines[clubplayer.club.pk] = [timeline]
                else:
                    date_a = timelines[clubplayer.club.pk][-1].end_date
                    date_b = self.date2datetime(clubplayer.start_date)
                    # extra day between the same events is ignored
                    if date_a + datetime.timedelta(days=1) >= date_b:
                        # combine events by shifting end date
                        dt = self.date2datetime(clubplayer.end_date)
                        timelines[clubplayer.club.pk][-1].end_date = dt
                    else:
                        timelines[clubplayer.club.pk].append(timeline)
            models.Timeline.objects.bulk_create(
                itertools.chain(*timelines.values()))

    def first_club_goal_event(self):
        for player in self.players:
            clubplayers = player.clubplayer_set.all()
            timelines = models.Timeline.objects.filter(
                player=player, type='first_club_goal')
            clubs = models.Club.objects.filter(
                            pk__in=clubplayers.values_list('club', flat=True)
                        ).exclude(
                            pk__in=timelines.values_list('club', flat=True)
                        )
            for club in clubs:
                history = models.MatchGoalHistory.objects.filter(scorer=player
                                    ).by_club(club, player
                                    ).order_by('match__date').first()
                if history:
                    ru_club = club.ru_title
                    en_club = club.en_title
                    models.Timeline.objects.get_or_create(
                        start_date=history.match.date,
                        ru_headline='Первая шайба в клубе "%s"' % ru_club,
                        en_headline='First goal in a club "%s"' % en_club,
                        ru_text='Первая шайба в клубе "%s"' % ru_club,
                        en_text='First goal in a club "%s"' % en_club,
                        media=club.logo,
                        type='first_club_goal',
                        player=player,
                        club=club)

    def series_0_loose_goals_event(self):
        for player in self.players:
            matches = models.ClubPlayerMatch.objects.is_active().filter(    
                    clubplayer__player=player,
                    clubplayer__line=1,
                    gamingtime__gt=0
                ).order_by('match__date')
            i = 0
            for match in matches:
                if match.loose_goals == 0:
                    i += 1
                else:
                    i = 0
                if i >= 3 and not models.Timeline.objects.filter(
                        start_date=match.match.date,
                        type='series_0_loose_goals',
                        player=player).exists():
                    models.Timeline.objects.create(
                        start_date=match.match.date,
                        ru_headline='%d-й "сухарь" подряд' % i,
                        en_headline='%dth in series of 0 loose goals' % i,
                        ru_text='%d-й "сухарь" подряд' % i,
                        en_text='%dth in series of 0 loose goals' % i,
                        media=player.photo,
                        type='series_0_loose_goals',
                        player=player)
