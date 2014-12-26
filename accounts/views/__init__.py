# coding: utf-8
from django.views.generic import DetailView
from registration.backends.default.views import RegistrationView

from ..forms import RegForm
from ..mixins import LoginReqMixin, ProfileMixin


class Signup(RegistrationView):
    form_class = RegForm

    def register(self, request, **cleaned_data):
        cleaned_data['email'] = cleaned_data['username']
        return super(Signup, self).register(request, **cleaned_data)


class ProfileView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/user-card.html'


class ProfileOffersView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/user-card2.html'


class ProfileHistoryView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/user-card3.html'


class ProfilePrivateView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/user-card4.html'
