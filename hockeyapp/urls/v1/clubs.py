# -*- coding: utf-8 -*-
from django.conf.urls import url

from ...views.v1 import clubs


urlpatterns = [
    url(r'^$', clubs.ClubListView.as_view(), name='list'),
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
    url(r'^(?P<pk>\d+)/calendar/$', clubs.ClubCalendarView.as_view(),
        name='calendar-shedule'),
    url(r'^(?P<pk>\d+)/stats/$', clubs.ClubStatsView.as_view(),
        name='stats'),
    url(r'^(?P<pk>\d+)/numbers/$', clubs.ClubNumbersView.as_view(),
        name='numbers'),
    # testing purposes
    url(r'^indicators/$', clubs.ClubView2.as_view(), name='club2'),
]
