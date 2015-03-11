# coding: utf-8
from django.contrib.auth import views
from django.views.generic import DetailView
from registration.backends.default.views import RegistrationView

from ..forms import RegForm
from ..mixins import LoginReqMixin, ProfileMixin

password_reset_confirm = views.password_reset_confirm
password_reset_complete = views.password_reset_complete


class Signup(RegistrationView):
    form_class = RegForm

    def register(self, request, **cleaned_data):
        cleaned_data['email'] = cleaned_data['username']
        return super(Signup, self).register(request, **cleaned_data)


class ProfileOptionsView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card.html'


class ProfileOffersView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card2.html'


class ProfileHistoryView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card3.html'


class ProfilePrivateView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card4.html'
