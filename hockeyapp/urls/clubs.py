# -*- coding: utf-8 -*-
from django.conf.urls import url

from ..views import clubs


urlpatterns = [
    url(r'^$', clubs.ClubListView.as_view(), name='list'),
    url(r'^table/$', clubs.ClubListTableView.as_view(), name='list-table'),
    url(r'^(?P<pk>\d+)/$', clubs.ClubView.as_view(), name='details'),
    url(r'^(?P<pk>\d+)/calendar/$', clubs.ClubCalendarView.as_view(),
        name='calendar'),
    url(r'^(?P<pk>\d+)/stats/$', clubs.ClubStatsView.as_view(),
        name='stats'),
    url(r'^(?P<pk>\d+)/home/$', clubs.ClubHomeView.as_view(),
        name='home'),
    url(r'^(?P<pk>\d+)/photos/$', clubs.ClubPhotosView.as_view(),
        name='photos'),
    url(r'^(?P<pk>\d+)/fanzone/$', clubs.ClubFanZoneView.as_view(),
        name='fanzone'),

    url(r'^(?P<pk>\d+)/main/$', clubs.ClubMainAboutView.as_view(),
        name='main-about'),
    url(r'^(?P<pk>\d+)/main/games/$', clubs.ClubMainGamesView.as_view(),
        name='main-games'),
    url(r'^(?P<pk>\d+)/main/coaches/$', clubs.ClubMainCoachesView.as_view(),
        name='main-coaches'),
    url(r'^(?P<pk>\d+)/main/rumors/$', clubs.ClubMainRumorsView.as_view(),
        name='main-rumors'),
    url(r'^(?P<pk>\d+)/main/geography/$', clubs.ClubMainGeographyView.as_view(),
        name='main-geography'),
    url(r'^(?P<pk>\d+)/main/numbers/$', clubs.ClubMainNumbersView.as_view(),
        name='main-numbers'),
    url(r'^(?P<pk>\d+)/main/symbol/$', clubs.ClubMainSymbolView.as_view(),
        name='main-symbol'),

    url(r'^(?P<pk>\d+)/calendar/$', clubs.ClubCalendarView.as_view(),
        name='calendar-shedule'),
    url(r'^(?P<pk>\d+)/calendar/winlose/$', clubs.ClubCalendarWinLoseView.as_view(),
        name='calendar-winlose'),
    url(r'^(?P<pk>\d+)/calendar/geography/$', clubs.ClubCalendarGeographyView.as_view(),
        name='calendar-geography'),
    url(r'^(?P<pk>\d+)/calendar/trips/$', clubs.ClubCalendarTripsView.as_view(),
        name='calendar-trips'),

    url(r'^(?P<pk>\d+)/numbers/$', clubs.ClubNumbersView.as_view(),
        name='numbers'),
    # testing purposes
    url(r'^indicators/$', clubs.ClubView2.as_view(), name='club2'),
]
