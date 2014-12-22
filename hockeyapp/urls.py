# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    # players summary
    url(r'^players/search/$', views.PlayersSearch.as_view(),
        name='players-search'),
    url(r'^players/compare/$', views.PlayersCompare.as_view(),
        name='players-compare'),
    # player's info
    url(r'^player/(?P<pk>\d+)/$', views.PlayerCard.as_view(),
        name='player-card'),
    url(r'^player/(?P<pk>\d+)/indicators/$',
        views.PlayerCardIndicators.as_view(),
        name='player-card-indicators'),
    url(r'^player/(?P<pk>\d+)/clubs/$', views.PlayerCardClubs.as_view(),
        name='player-card-clubs'),
    url(r'^player/(?P<pk>\d+)/coaches/$', views.PlayerCardCoaches.as_view(),
        name='player-card-coaches'),
    url(r'^player/(?P<pk>\d+)/partners/$', views.PlayerCardPartners.as_view(),
        name='player-card-partners'),
    url(r'^player/(?P<pk>\d+)/photos/$', views.PlayerCardPhotos.as_view(),
        name='player-card-photos'),
    url(r'^player/(?P<pk>\d+)/communication/$',
        views.PlayerCardCommunication.as_view(),
        name='player-card-communication'),
    url(r'^player/(?P<pk>\d+)/news/$', views.PlayerCardNews.as_view(),
        name='player-card-news'),
]
