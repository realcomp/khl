# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
События на главной странице
'''

import datetime


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
        raise NotImplementedError()

    @property
    def image(self):
        raise NotImplementedError()


class BirthdayEvent(Event):
    """
    Player's birthday
    """
    @property
    def url(self):
        return self.obj.get_absolute_url()

    @property
    def image(self):
        return self.obj.photo.url


class MatchEvent(Event):
    """
    Clubs's matches
    """
    def __init__(self, date, obj):
        super(MatchEvent, self).__init__(obj.date.date(), obj)

    @property
    def url(self):
        return self.obj.home_team.get_absolute_url()

    @property
    def image(self):
        return self.obj.home_team.logo and self.obj.home_team.logo.url


class EventFactory(object):
    '''
    Event aggregation factory
    '''
    sources = {}

    def __init__(self, sources):
        self.sources = sources

    def get_events(self, date):
        events = []
        events += self.get_birthday_events(date)
        events += self.get_match_events(date)
        return events

    def get_birthday_events(self, date):
        events = []
        birth_dates = map(
            lambda x: datetime.date(year=x, month=date.month, day=date.day),
            range(date.year-200, date.year))
        players = self.sources.get('player')
        if players:
            for player in players.filter(birth_date__in=birth_dates):
                events.append(BirthdayEvent(date, player))
        return events

    def get_match_events(self, date):
        events = []
        schedules = self.sources.get('schedule')
        if schedules:
            for schedule in schedules.filter(
                    date__gte=date,
                    date__lte=date + datetime.timedelta(days=1)):
                events.append(MatchEvent(date, schedule))
        return events
