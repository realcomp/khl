# -*- coding: utf-8 -*-
from django.conf.urls import url

from . import views


urlpatterns = [
    # metrics
    url(r'^metrics/players/$', views.MetricsPlayers.as_view(),
        name='metrics-players'),
    url(r'^metrics/players/(?P<pk>\d+)/$', views.MetricsPlayerCard.as_view(),
        name='metrics-player-card'),
    url(r'^metrics/players/compare/$', views.MetricsPlayersCompare.as_view(),
        name='metrics-compare'),
    url(r'^metrics/players/compare2/$', views.MetricsPlayersCompare2.as_view(),
        name='metrics-compare2'),
    url(r'^metrics/players/compare3/$', views.MetricsPlayersCompare3.as_view(),
        name='metrics-compare3'),
    # players
    url(r'^players/$', views.PlayersSearch.as_view(),
        name='players-search'),
    url(r'^players/(?P<pk>\d+)/$', views.PlayerCard.as_view(),
        name='player-card'),
    url(r'^players/(?P<pk>\d+)/indicators/$',
        views.PlayerCardIndicators.as_view(),
        name='player-card-indicators'),
    url(r'^players/(?P<pk>\d+)/clubs/$', views.PlayerCardClubs.as_view(),
        name='player-card-clubs'),
    url(r'^players/(?P<pk>\d+)/coaches/$', views.PlayerCardCoaches.as_view(),
        name='player-card-coaches'),
    url(r'^players/(?P<pk>\d+)/partners/$', views.PlayerCardPartners.as_view(),
        name='player-card-partners'),
    url(r'^players/(?P<pk>\d+)/photos/$', views.PlayerCardPhotos.as_view(),
        name='player-card-photos'),
    url(r'^players/(?P<pk>\d+)/communication/$',
        views.PlayerCardCommunication.as_view(),
        name='player-card-communication'),
    url(r'^players/(?P<pk>\d+)/news/$', views.PlayerCardNews.as_view(),
        name='player-card-news'),
    # clubs
    url(r'^clubs/$', views.ClubListView.as_view(), name='club-list'),
    url(r'^clubs/(?P<pk>\d+)/$', views.ClubView.as_view(), name='club'),
    url(r'^clubs/(?P<pk>\d+)/stats/$', views.ClubStatsView.as_view(),
        name='club-stats'),
    url(r'^clubs/(?P<pk>\d+)/home/$', views.ClubHomeView.as_view(),
        name='club-home'),
    url(r'^clubs/(?P<pk>\d+)/photos/$', views.ClubPhotosView.as_view(),
        name='club-photos'),
    url(r'^clubs/(?P<pk>\d+)/fanzone/$', views.ClubFanZoneView.as_view(),
        name='club-fanzone'),
]
