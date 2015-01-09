from django.conf.urls import url

from . import views
from .views import api


urlpatterns = [
    # TODO: move to separate namespace
    # REST API
    url(r'^api/profile/version/$', api.ProfileVersionView.as_view(),
        name='profile-version-api'),
    url(r'^api/profile/$', api.ProfileView.as_view(),
        name='profile-api'),
    # Django CBV's'
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^profile/$', views.ProfilePrivateView.as_view(),
        name='profile-private'),
    url(r'^profile/offers/$', views.ProfileOffersView.as_view(),
        name='profile-offers'),
    url(r'^profile/history/$', views.ProfileHistoryView.as_view(),
        name='profile-history'),
    url(r'^profile/options/$', views.ProfilePrivateView.as_view(),
        name='profile-options'),
]
