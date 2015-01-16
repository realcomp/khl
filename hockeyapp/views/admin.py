#coding: utf-8
from __future__ import unicode_literals

from django.views.generic import FormView

from ..forms import ClubleaguesAddForm
from ..models import LeagueClub


class ClubleaguesAddView(FormView):
    b''' Форма создания связок клуб - лига в сезоне '''
    form_class = ClubleaguesAddForm
    template_name = 'admin/clubleagues_form.html'

    def get_success_url(self):
        return LeagueClub.admin_list_link()

    def form_valid(self, form):
        clubs = form.cleaned_data.pop('clubs', list())
        season = form.cleaned_data['season']
        for club in clubs:
            LeagueClub.objects.get_or_create(club=club,
                                             start_date=season.start_date,
                                             end_date=season.end_date,
                                             **form.cleaned_data)
        return super(ClubleaguesAddView, self).form_valid(form)
clubleagues_add = ClubleaguesAddView.as_view()