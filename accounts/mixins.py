# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from rest_framework.renderers import JSONRenderer

from hockeyapp.serializers import CountrySerializer, BaseClubSerializer

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
        context['request'] = self.request
        user = self.get_object()
        context['user'] = ProfileSerializer(user, context=context).data
        counties = CountrySerializer(
            user.countries, many=True, context=context).data
        clubs = BaseClubSerializer(
            user.clubs, many=True, context=context).data
        context['countries'] = JSONRenderer().render(counties)
        context['clubs'] = JSONRenderer().render(clubs)
        return context
