from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^base/', include('api.base.urls', namespace='base')),
    url(r'^hockey/', include('api.hockey.urls', namespace='hockey')),
)