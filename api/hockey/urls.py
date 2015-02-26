# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.hockey',
    url(r'^arenainstaphoto/$', 'admin.aip_list', name='aip_list'),
    url(r'^arenainstaphoto/(?P<pk>\d+)/$', 'admin.aip_detail', name='aip'),
    url(r'^club/$', 'admin.club_list', name='club_list'),
    url(r'^club/(?P<pk>\d+)/$', 'admin.club_detail', name='club'),
    url(r'^match/$', 'admin.match_list', name='match_list'),
)