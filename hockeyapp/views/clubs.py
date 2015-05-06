# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.views.generic import DetailView, TemplateView
from django.utils.translation import ugettext_lazy as _

from base.mixins import SeasonsMenuMixin
from base.models import Season

from .mixins import SeasonsMixin
from ..models import Club
from ..serializers import SeasonSerializer, ClubListSerializer
from ..serializers.clubs import ClubMainAboutSerializer


class ClubListTableView(TemplateView):
    template_name = 'hockeyapp/clubs/clubs-list-table.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListTableView, self).get_context_data(**kwargs)
        context['request'] = self.request
        seasons = Season.objects.order_by('-start_date')
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        return context


class ClubListView(TemplateView):
    template_name = 'hockeyapp/clubs/clubs-list.html'

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)
        context['request'] = self.request
        seasons = Season.objects.order_by('-start_date')
        context['seasons'] = SeasonSerializer(
            seasons, context=context, many=True).data
        return context


class ClubView(SeasonsMenuMixin, DetailView):
    model = Club
    template_name = 'hockeyapp/clubs/clubs-team.html'

    def get_context_data(self, **kwargs):
        context = super(ClubView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(ClubListSerializer(
            self.get_object(), context=context).data)
        return context


class ClubMainAboutView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-about.html'

    def get_context_data(self, **kwargs):
        context = super(ClubMainAboutView, self).get_context_data(**kwargs)
        context['request'] = self.request
        context.update(ClubMainAboutSerializer(
            self.get_object(), context=context).data)
        return context


class ClubMainGamesView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-games.html'


class ClubMainGeographyView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-geography.html'


class ClubMainNumbersView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-numbers.html'


class ClubMainRumorsView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-rumors.html'


class ClubMainSymbolView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-symbol.html'


class ClubMainCoachesView(ClubView):
    template_name = 'hockeyapp/clubs/main/main-coaches.html'


class ClubView2(TemplateView):
    template_name = 'hockeyapp/clubs/clubs-team2.html'

class ClubCalendarView(ClubView):
    template_name = 'hockeyapp/clubs/calendar/calendar-shedule.html'


class ClubCalendarWinLoseView(ClubView):
    template_name = 'hockeyapp/clubs/calendar/calendar-winlose.html'


class ClubCalendarGeographyView(ClubView):
    template_name = 'hockeyapp/clubs/calendar/calendar-geography.html'


class ClubCalendarTripsView(ClubView):
    template_name = 'hockeyapp/clubs/calendar/calendar-trips.html'


class ClubHomeView(ClubView):
    template_name = 'hockeyapp/clubs/home/home-about.html'


class ClubHomeSheduleView(ClubView):
    template_name = 'hockeyapp/clubs/home/home-shedule.html'


class ClubHomeMapView(ClubView):
    template_name = 'hockeyapp/clubs/home/home-map.html'


class ClubHomeAttendanceView(ClubView):
    template_name = 'hockeyapp/clubs/home/home-attendance.html'


class ClubHomePhotosView(ClubView):
    template_name = 'hockeyapp/clubs/home/home-photos.html'


class ClubFanZoneView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-fan.html'


class ClubPhotosView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-photos.html'


class ClubStatsView(ClubView):
    template_name = 'hockeyapp/clubs/stats/stats-table.html'

    def get_context_data(self, **kwargs):
        context = super(ClubStatsView, self).get_context_data(**kwargs)
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return context


class ClubStatsCompareView(ClubView):
    template_name = 'hockeyapp/clubs/stats/stats-compare.html'

    def get_context_data(self, **kwargs):
        context = super(ClubStatsCompareView, self).get_context_data(**kwargs)
        context['alphabet'] = _('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        return context


class ClubMainView(ClubView):
    template_name = 'hockeyapp/clubs/main/clubs-main.html'


class ClubNumbersView(ClubView):
    template_name = 'hockeyapp/clubs/clubs-numbers.html'
