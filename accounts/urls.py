from django.conf.urls import url

from . import views
from .views import api


urlpatterns = [
    url(r'^api/user/version/$', api.UserVersionView.as_view(),
        name='user-version'),
    url(r'^signup/$', views.Signup.as_view(), name='signup'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/offers/$', views.ProfileOffersView.as_view(),
        name='profile-offers'),
    url(r'^profile/history/$', views.ProfileHistoryView.as_view(),
        name='profile-history'),
    url(r'^profile/private/$', views.ProfilePrivateView.as_view(),
        name='profile-private'),
]
