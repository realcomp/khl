# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.hockey',
    url(r'^arenaphoto/$', 'admin.arenaphoto_list', name='arenaphoto_list'),
    url(r'^clubphotos/$', 'admin.cp_list', name='clubphotos'),
    url(r'^clubphotos/(?P<pk>\d+)/$', 'admin.cp_detail', name='clubphoto'),
    url(r'^club/$', 'admin.club_list', name='club_list'),
    url(r'^club/(?P<pk>\d+)/$', 'admin.club_detail', name='club'),
    url(r'^match/$', 'admin.match_list', name='match_list'),
)