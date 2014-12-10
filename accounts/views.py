#coding: utf-8
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from .forms import UsrCrtForm


class Signup(FormView):
    template_name = 'accounts/signup.html'
    form_class = UsrCrtForm
    success_url = reverse('index')

    def form_valid(self, form):
        _usr = form.save(commit=False)
        _usr.is_active = False
        _usr.save()
        return HttpResponseRedirect(self.get_success_url())
signup = Signup.as_view()