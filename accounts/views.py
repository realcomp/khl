#coding: utf-8
from registration.backends.default.views import RegistrationView

from .forms import RegForm


class Signup(RegistrationView):
    form_class = RegForm

    def register(self, request, **cleaned_data):
        cleaned_data['email'] = cleaned_data['username']
        return super(Signup, self).register(request,**cleaned_data)
signup = Signup.as_view()