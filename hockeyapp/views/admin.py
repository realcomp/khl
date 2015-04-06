#coding: utf-8
from __future__ import unicode_literals
import itertools

from django.db.models import Avg
from django.http import Http404
from django.views.generic import FormView, TemplateView

from base.models import Season
from ..forms import ClubleaguesAddForm, MatchParserForm
from ..models import LeagueClub, Match, League, ClubPlayer, Player
from ..models import ClubPlayerMatch


class ClubleaguesAddView(FormView):
    b''' Форма создания связок клуб - лига в сезоне '''
    form_class = ClubleaguesAddForm
    template_name = 'admin/clubleagues_form.html'

    def get_success_url(self):
        return LeagueClub.admin_list_link()

    def form_valid(self, form):
        clubs = form.cleaned_data.pop('clubs', list())
        seasons = form.cleaned_data.pop('seasons', list())
        for season in seasons:
            for club in clubs:
                LeagueClub.objects.get_or_create(club=club,
                                                 start_date=season.start_date,
                                                 end_date=season.end_date,
                                                 season=season,
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
        #from_id = form.cleaned_data['from_id']
        #to_id = form.cleaned_data.get('to_id')
        #count = form.cleaned_data.get('count')
        #parser_id = form.cleaned_data.get('parser_id')
        #update = form.cleaned_data.get('update')
        #if not count:
            #count = to_id-from_id+1 if to_id else 1
        return super(MatchParserFormView, self).form_valid(form)
matchparser_form = MatchParserFormView.as_view()


class ClubPhotoAngularTemplate(TemplateView):
    template_name = 'hockeyapp/admin/clubs-insta-photo.html'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404()
        return super(ClubPhotoAngularTemplate, self).dispatch(request, *args, **kwargs)
cpat = ClubPhotoAngularTemplate.as_view()


class ClubPlayerMatchTemplate(TemplateView):
    b''' fix 257 '''
    template_name = 'admin/fix257.html'
    khl = League.objects.get(en_title='KHL')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404()
        return super(ClubPlayerMatchTemplate, self).dispatch(request, *args, **kwargs)

    def get_cps(self, players, league):
        for plr in players:
            cps = plr.clubplayer_set.filter(league=league)
            last_cp = cps.order_by('season__end_date').last()
            season = last_cp and last_cp.season
            if last_cp.clubplayermatch_set.count() > 29 and season:
                next_season = Season.objects.get_next_season(season)
                up_cps = plr.clubplayer_set.filter(league=self.khl, season=next_season)
                if cps.exists() and up_cps.exists():
                    yield last_cp, up_cps

    def get_up_league_qs(self, up_cps):
        if up_cps.count() > 1:
            ids = []
            for cp in up_cps:
                ids.append(cp.clubplayermatch_set.values_list('id', flat=True))
            return ClubPlayerMatch.objects.filter(
                                            pk__in=set(itertools.chain(*ids)))
        else:
            return up_cps.last().clubplayermatch_set.all()

    def aggregate_values(self, qs):
        aggr = itertools.chain(map(Avg,('goals', 'assists', 'points',
                                        'plus_minus', 'saves','loose_goals')))
        return qs.aggregate(*aggr)

    def get_context_data(self, **kwargs):
        if 'view' not in kwargs:
            kwargs['view'] = self
        if 'leagues' not in kwargs:
            kwargs['leagues'] = dict()
        vhl = League.objects.get(en_title='VHL')
        mhl = League.objects.get(en_title='MHL')
        cp = ClubPlayer.objects.filter(clubplayermatch__gte=30)
        mhl_plr_ids = set(cp.filter(league=mhl).values_list('player', flat=True))
        vhl_plr_ids = set(cp.filter(league=vhl).values_list('player', flat=True))
        khl_plr_ids = set(cp.filter(league=self.khl).values_list('player', flat=True))
        vhl_plrs = Player.objects.filter(id__in=vhl_plr_ids & khl_plr_ids)
        mhl_plrs = Player.objects.filter(id__in=mhl_plr_ids & khl_plr_ids)
        #m2vhl_plrs = models.Player.objects.filter(id__in=mhl_plr_ids & vhl_plr_ids)
        for k,qs,league in (
                            ('vhl2khl', vhl_plrs, vhl),
                            ('mhl2khl', mhl_plrs, mhl),
                            #('mhl2vhl', m2vhl_plrs, vhl),
        ):
            kwargs['leagues'][k]=self.get_players_data(qs, league)
        return kwargs

    def get_players_data(self, qs, league):
        res=dict()
        for cps, up_cps in self.get_cps(qs, league):
            player = cps.player
            _up_cpms = self.get_up_league_qs(up_cps)
            _down_cpms = cps.clubplayermatch_set.all()
            res[player.id] = dict(
                player=player,
                down_league=self.aggregate_values(_down_cpms),
                up_league=self.aggregate_values(_up_cpms),
            )
        return res    
cpmat = ClubPlayerMatchTemplate.as_view()