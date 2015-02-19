# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
События на главной странице
'''

import datetime

from django.core.urlresolvers import reverse
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
    def image(self):
        pass

    @property
    def logo(self):
        pass

    @property
    def type(self):
        pass


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

    @property
    def type(self):
        return _('Birth day')


class MatchEvent(Event):
    """
    Clubs's matches
    """
    def __init__(self, date, obj):
        super(MatchEvent, self).__init__(obj.date.date(), obj)

    @property
    def type(self):
        return _('Match')


class HomeMatchEvent(MatchEvent):
    """
    Clubs's home matches
    """
    @property
    def url(self):
        return reverse(
            'hockeyapp:club-news', kwargs={'pk': self.obj.home_team_id})

    @property
    def logo(self):
        return self.obj.home_team.logo and self.obj.home_team.logo.url


class GuestMatchEvent(MatchEvent):
    """
    Clubs's guest matches
    """
    @property
    def url(self):
        return reverse(
            'hockeyapp:club-news', kwargs={'pk': self.obj.guest_team_id})

    @property
    def logo(self):
        return self.obj.guest_team.logo and self.obj.guest_team.logo.url


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
        events += self.get_home_match_events(date)
        events += self.get_guest_match_events(date)
        return events

    def get_birthday_events(self, date):
        events = []
        x_birthdate = {
            'where': [
                'extract(day from birth_date)=%d and '
                'extract(month from birth_date)=%d' % (date.day, date.month)],
        }
        players = self.sources.get('player')
        if players:
            for player in players.extra(**x_birthdate):
                events.append(BirthdayEvent(date, player))
        return events

    def get_home_match_events(self, date):
        events = []
        schedules = self.sources.get('schedule')
        if schedules:
            for schedule in schedules.filter(
                    date__gte=date,
                    date__lte=date + datetime.timedelta(days=7)):
                events.append(HomeMatchEvent(date, schedule))
        return events

    def get_guest_match_events(self, date):
        events = []
        schedules = self.sources.get('schedule')
        if schedules:
            for schedule in schedules.filter(
                    date__gte=date,
                    date__lte=date + datetime.timedelta(days=7)):
                events.append(GuestMatchEvent(date, schedule))
        return events
