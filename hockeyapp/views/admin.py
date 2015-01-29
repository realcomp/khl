#coding: utf-8
from __future__ import unicode_literals

from django.views.generic import FormView

from ..forms import ClubleaguesAddForm, MatchParserForm
from ..models import LeagueClub, Match
from hockeyapp.tasks import async_hockey_matches_parser


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


class MatchParserFormView(FormView):
    b''' Форма асинхронной обработки протоколов матча с сайта mhl.ru'''
    form_class = MatchParserForm
    template_name = 'admin/matchparser_form.html'

    def get_success_url(self):
        return Match.admin_list_link()

    def form_valid(self, form):
        from_id = form.cleaned_data['from_id']
        to_id = form.cleaned_data.get('to_id')
        count = form.cleaned_data.get('count')
        parser_id = form.cleaned_data.get('parser_id')
        update = form.cleaned_data.get('update')
        if not count:
            count = to_id-from_id+1 if to_id else 1
        async_hockey_matches_parser.delay(parser_id, from_id, count or 1,update)
        return super(MatchParserFormView, self).form_valid(form)
matchparser_form = MatchParserFormView.as_view()