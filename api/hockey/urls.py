# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.hockey',
    url(r'^clubphotos/$', 'admin.cp_list', name='clubphotos'),
    url(r'^clubphotos/(?P<pk>\d+)/$', 'admin.cp_detail', name='clubphoto'),
)