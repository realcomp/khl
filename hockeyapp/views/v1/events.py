# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
События на главной странице
'''

import datetime
import random

from django.core.urlresolvers import reverse
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _


class Event(object):
    '''
    Abstract event
    '''
    date = None
    obj = None

    def __init__(self, date, obj):
        self.date = date
        self.obj = obj

    @property
    def url(self):
        pass

    @property
    def type(self):
        pass

    @property
    def image(self):
        pass

    @property
    def logos(self):
        pass

    @property
    def logos_urls(self):
        pass

    @property
    def rgb(self):
        return '#3078a2'


class BirthdayEvent(Event):
    """
    Player's birthday
    """
    @property
    def url(self):
        return self.obj.get_absolute_url()

    @property
    def image(self):
        return self.obj.photo and self.obj.photo.url


class MatchEvent(Event):
    """
    Clubs's matches
    """
    def __init__(self, date, obj):
        super(MatchEvent, self).__init__(obj.date.date(), obj)


class HomeMatchEvent(MatchEvent):
    """
    Clubs's home matches
    """
    @property
    def logos(self):
        result = []
        if self.obj.home_team.logo:
            result.append(self.obj.home_team.logo.url)
        if self.obj.guest_team.logo:
            result.append(self.obj.guest_team.logo.url)
        return result

    @property
    def logos_urls(self):
        return map(lambda pk: reverse(
            'hockeyapp:clubs:news', kwargs={'pk': pk}),
            (self.obj.home_team_id, self.obj.guest_team_id))

    @property
    def rgb(self):
        return self.obj.home_team.rgb or super(HomeMatchEvent, self).rgb


class GuestMatchEvent(HomeMatchEvent):
    """
    Clubs's guest matches
    """
    @property
    def logos(self):
        return reversed(super(GuestMatchEvent, self).logos)

    @property
    def logos_urls(self):
        return reversed(super(GuestMatchEvent, self).logos_urls)

    @property
    def rgb(self):
        return self.obj.guest_team.rgb or super(GuestMatchEvent, self).rgb


class TimelineEvent(Event):
    @property
    def url(self):
        return self.obj.player.get_absolute_url()

    @property
    def image(self):
        return self.obj.player.photo and self.obj.player.photo.url

    @property
    def rgb(self):
        return (
            (self.obj.club and self.obj.club.rgb) or
            super(TimelineEvent, self).rgb)


class EventFactory(object):
    '''
    Event aggregation factory
    '''
    sources = {}

    def __init__(self, sources):
        self.sources = sources

    def _get_source(self, key):
        source = self.sources.get(key)
        if source:
            return source

    def get_events(self, date):
        events = []
        events += self.get_birthday_events(date)
        events += self.get_home_match_events(date)
        events += self.get_guest_match_events(date)
        events += self.get_timeline_events(date)
        random.shuffle(events)
        return events

    def get_birthday_events(self, date):
        events = []
        x_birthdate = {
            'where': [
                'extract(day from birth_date)=%d and '
                'extract(month from birth_date)=%d' % (date.day, date.month)],
        }
        players = self._get_source('player')
        if players:
            for player in players.extra(**x_birthdate):
                events.append(BirthdayEvent(date, player))
        return events

    def get_home_match_events(self, date):
        schedules = self._get_source('schedule')
        if schedules:
            for schedule in schedules.filter(
                    date__gte=date,
                    date__lte=date + datetime.timedelta(days=7)):
                yield HomeMatchEvent(date, schedule)

    def get_guest_match_events(self, date):
        schedules = self._get_source('schedule')
        if schedules:
            for schedule in schedules.filter(
                    date__gte=date,
                    date__lte=date + datetime.timedelta(days=7)):
                yield GuestMatchEvent(date, schedule)

    def get_timeline_events(self, date):
        timelines = self._get_source('timeline')
        days = 7
        q_completed_event = Q(
            start_date__gte=date - datetime.timedelta(days=days),
            end_date__isnull=True)
        q_recent_running_event = Q(
            start_date__gte=date - datetime.timedelta(days=days),
            end_date__isnull=False)
        # q_running_event = Q(
        #     start_date__lte=date,
        #     end_date__gte=date)
        if timelines:
            for timeline in timelines.filter(
                    q_completed_event | q_recent_running_event):
                yield TimelineEvent(date, timeline)
