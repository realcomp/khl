# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.hockey',
    url(r'^arenainstaphoto/$', 'admin.aip_list', name='aip_list'),
    url(r'^arenainstaphoto/(?P<pk>\d+)/$', 'admin.aip_detail', name='aip'),
    url(r'^processedarenainstaphoto/$', 'views.paip_list', name='paip_list'),
    url(r'^arena/$', 'admin.arena_list', name='arena_list'),
    url(r'^arena/(?P<pk>\d+)/$', 'admin.arena_detail', name='arena'),
    url(r'^admin/club/$', 'admin.club_list', name='club_list'),
    url(r'^admin/club/(?P<pk>\d+)/$', 'admin.club_detail', name='club_detail'),
    url(r'^clubinstaphoto/$', 'views.cip_list', name='cip_list'),
    url(r'^admin/match/$', 'admin.match_list', name='match_list'),
    url(r'^player/$', 'admin.player_list', name='player_list'),
    url(r'^playerinstaphoto/$', 'views.pip_list', name='pip_list'),


    url(r'^clubs/$', 'views.club_list', name='club-list-api'),
    url(r'^match/$', 'views.matches', name='matches'),
    url(r'^player/(?P<player_id>\d+)/partners/$', 'views.player_partners', name='player_partners'),
)