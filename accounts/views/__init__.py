# coding: utf-8
from django.views.generic import DetailView, UpdateView
from registration.backends.default.views import RegistrationView

from ..forms import RegForm
from ..mixins import LoginReqMixin, ProfileMixin
from ..serializers import ProfileUpdateSerializer


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


class ProfilePrivateView(LoginReqMixin, ProfileMixin, UpdateView):
    template_name = 'accounts/user-card4.html'

    def post(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = ProfileUpdateSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.update(obj, serializer.validated_data)
        else:
            print('ERRORS')
            print(serializer.errors)
        return self.render_to_response(self.get_context_data())
