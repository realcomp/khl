# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _

from base.models import Season

from .mixins import SeasonsMixin
from ..models import Club
from ..serializers import SeasonSerializer, ClubListSerializer


class ClubListView(TemplateView):
    template_name = 'hockeyapp/clubs/clubs.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        seasons = Season.objects.order_by('-start_date')
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        return context


class ClubView(SeasonsMixin, DetailView):
    model = Club
    template_name = 'hockeyapp/clubs/clubs-team.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(ClubListSerializer(
            self.get_object(), context=context).data)
        return context


class ClubView2(TemplateView):
    template_name = 'hockeyapp/clubs/clubs-team2.html'


class ClubCalendarView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-calendar.html'


class ClubHomeView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-home.html'


class ClubFanZoneView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-fan.html'


class ClubPhotosView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-photos.html'


class ClubStatsView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-stats.html'

    def get_context_data(self, **kwargs):
        context = super(ClubStatsView, self).get_context_data(**kwargs)
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return context


class ClubNewsView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-news.html'


class ClubNumbersView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-numbers.html'
