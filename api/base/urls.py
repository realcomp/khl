# -*- coding: utf-8 -*-
from django.conf.urls import url, patterns


urlpatterns = patterns('api.base',
    url(r'^instagram_user/$', 'views.iu_list', name='iu_list'),
    url(r'^instagram_user/(?P<pk>\d+)/$', 'views.iu_detail', name='iu_detail'),
)