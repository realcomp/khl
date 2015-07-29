# -*- coding: utf-8 -*-
from django.conf.urls import include, url

from .. import views
from ..views import api
from ..views.api import (
    generic,
    clubs as api_clubs,
    players as api_players)
from ..views import admin, players as views_players


urlpatterns = [
    # TODO: move to separate namespace
    # REST API
    url(r'^api/countries/$', generic.CountryList.as_view(),
        name='country-list-api'),
    url(r'^api/countries/leagues/$', generic.CountryLeagueList.as_view(),
        name='country-league-list-api'),
    url(r'^api/leagues/$', generic.LeagueList.as_view(),
        name='league-list-api'),
    url(r'^api/players/$',
        api_players.PlayersSearch.as_view({'get': 'list'}),
        name='players-search-api'),
    url(r'^api/players/best/$',
        api_players.BestPlayer.as_view({'get': 'retrieve'}),
        name='best-player-api'),
    url(r'^api/players/numbers/$', api_players.PlayerNumbers.as_view(),
        name='player-numbers-api'),
    url(r'^api/players_by_name/$',
        api.PlayerNamesSearch.as_view(),
        name='player-names-search-api'),
    url(r'^api/clubs_by_title/$',
        api.ClubTitlesSearch.as_view(),
        name='club-titles-search-api'),
    url(r'^api/players/(?P<pk>\d+)/$',
        api_players.PlayerDetails.as_view(),
        name='player-card-api'),
    url(r'^api/players/(?P<player_id>\d+)/indicators/$',
        api.PlayerCardIndicators.as_view(),
        name='player-card-indicators-api'),
    url(r'^api/players/(?P<pk>\d+)/timeline/$',
        api.PlayerTimeline.as_view(),
        name='player-timeline-api'),
    url(r'^api/clubs/(?P<club_id>\d+)/players/$',
        api_clubs.ClubPlayers.as_view(),
        name='club-players-api'),
    url(r'^api/clubs/(?P<club_id>\d+)/coaches/$',
        api_clubs.ClubCoaches.as_view(),
        name='club-coaches-api'),
    url(r'^api/clubs/(?P<club_id>\d+)/numbers/$',
        api_clubs.PlayerNumbers.as_view(),
        name='club-player-numbers-api'),
    url(r'^api/clubs/(?P<pk>\d+)/$', api.ClubTeam.as_view(),
        name='club-team-api'),
    url(r'^api/clubs/(?P<pk>\d+)/compare/$', api.ClubTeamCompare.as_view(),
        name='club-team-compare-api'),
    url(r'^api/clubs/(?P<pk>\d+)/calendar/$', api.ClubCalendar.as_view(),
        name='club-calendar-api'),
    url(r'^api/clubs/(?P<club_id>\d+)/best/$',
        api.clubs.BestPlayers.as_view(), name='club-best-players-api'),
    url(r'^api/clubs/(?P<club_id>\d+)/origin_players/$',
        api_clubs.OriginPlayers.as_view(), name='club-origin-players-api'),
    url(r'^api/metrics/$', api.MetricsPlayers.as_view(),
        name='metrics-list-api'),
    url(r'^api/news/$', api.NewsList.as_view(), name='news-list-api'),
    url(r'^api/schedule/(?P<pk>\d+)/$',
        api.ScheduleView.as_view(), name='schedule-api'),
    # Django CBV's'
    url(r'^$', views.Index.as_view(),
        name='index'),
    url(r'^classic/$', views.IndexClassic.as_view(),
        name='index-classic'),
    url(r'^pro/$', views.IndexPro.as_view(),
        name='index-pro'),
    # metrics
    url(r'^metrics/players/$', views.MetricsPlayers.as_view(),
        name='metrics-players'),
    url(r'^metrics/players/(?P<pk>\d+)/$', views.MetricsPlayerCard.as_view(),
        name='metrics-player-card'),
    url(r'^metrics/players/compare/$', views.MetricsPlayersCompare.as_view(),
        name='metrics-compare'),
    url(r'^metrics/players/compare/graph/$',
        views.MetricsPlayersCompareGraph.as_view(),
        name='metrics-compare-graph'),
    # players
    url(r'^players/', include('hockeyapp.urls.players', namespace='players')),
    url(r'^v1/players/', include('hockeyapp.urls.v1.players', namespace='players_v1')),
    url(r'^players2/$', views_players.PlayersSearch2.as_view(),
        name='players-search2'),
    # clubs
    url(r'^clubs/', include('hockeyapp.urls.clubs', namespace='clubs')),
    url(r'^v1/clubs/', include('hockeyapp.urls.v1.clubs', namespace='clubs_v1')),

    # admin
    url(r'^sporto-admin/club-insta-photo/$',
        admin.cpat,
        name='club-insta-photo'),
]
