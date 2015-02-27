# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.hockey',
    url(r'^arenainstaphoto/$', 'admin.aip_list', name='aip_list'),
    url(r'^arenainstaphoto/(?P<pk>\d+)/$', 'admin.aip_detail', name='aip'),
    url(r'^arena/$', 'admin.arena_list', name='arena_list'),
    url(r'^arena/(?P<pk>\d+)/$', 'admin.arena_detail', name='arena'),
    url(r'^club/$', 'admin.club_list', name='club_list'),
    url(r'^club/(?P<pk>\d+)/$', 'admin.club_detail', name='club_detail'),
    url(r'^match/$', 'admin.match_list', name='match_list'),
    url(r'^player/$', 'admin.player_list', name='player_list'),
)