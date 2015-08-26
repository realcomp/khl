# -*- coding: utf-8 -*-
from django.conf.urls import url

from ..views import players


urlpatterns = [
    url(r'^$', players.PlayersSearch.as_view(), name='search'),
    url(r'^(?P<pk>\d+)/$', players.PlayerMainCard.as_view(), name='main-card'),
    url(r'^(?P<pk>\d+)/indicators/$', players.PlayerIndicators.as_view(),
        name='indicators'),
    url(r'^(?P<pk>\d+)/coaches/$', players.PlayerCoaches.as_view(),
        name='coaches'),
    url(r'^(?P<pk>\d+)/partners/$', players.PlayerPartners.as_view(),
        name='partners'),
    url(r'^(?P<pk>\d+)/photos/$', players.PlayerPhotos.as_view(),
        name='photos'),
    url(r'^(?P<pk>\d+)/achievements/$', players.PlayerAchievements.as_view(),
        name='achievements'),
    url(r'^(?P<pk>\d+)/clubs/$', players.PlayerClubs.as_view(),
        name='clubs'),
    url(r'^(?P<pk>\d+)/communication/$',
        players.PlayerCardCommunication.as_view(),
        name='communication'),
    url(r'^(?P<pk>\d+)/news/$', players.PlayerCardNews.as_view(),
        name='news'),
    url(r'^(?P<pk>\d+)/numbers/$', players.PlayerCardNumbers.as_view(),
        name='numbers'),
]
