# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .serializers import ProfileSerializer


class LoginReqMixin(object):
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(LoginReqMixin, self).dispatch(request, *args, **kwargs)


class ProfileMixin(object):
    def get_object(self):
        self.object = self.request.user
        return self.object

    def get_context_data(self, **kwargs):
        context = super(ProfileMixin, self).get_context_data(**kwargs)
        context.update(ProfileSerializer(self.get_object()).data)
        return context
