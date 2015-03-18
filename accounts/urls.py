# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views
from .views import api


urlpatterns = [
    # TODO: move to separate namespace
    # REST API
    url(r'^api/signup/$', api.RegistrationView.as_view(),
        name='registration-api'),
    url(r'^api/password_reset/$', api.PasswordResetView.as_view(),
        name='password-reset-api'),
    url(r'^api/password_reset_confirm/$',
        api.PasswordResetConfirmView.as_view(),
        name='password-reset-confirm-api'),
    url(r'^api/profile/version/$', api.ProfileVersionView.as_view(),
        name='profile-version-api'),
    url(r'^api/profile/$', api.ProfileView.as_view(),
        name='profile-api'),
    # Django CBV's'
    url(r'^signup/',
        TemplateView.as_view(
            template_name='registration/registration_form.html'),
        name='signup'),
    url(r'^profile/$', views.ProfilePrivateView.as_view(),
        name='profile-private'),
    url(r'^profile/offers/$', views.ProfileOffersView.as_view(),
        name='profile-offers'),
    url(r'^profile/history/$', views.ProfileHistoryView.as_view(),
        name='profile-history'),
    url(r'^profile/options/$', views.ProfileOptionsView.as_view(),
        name='profile-options'),
]
