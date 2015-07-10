#coding: utf-8
from __future__ import unicode_literals
import itertools
import numpy

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

    @property
    def khl(self):
        ''' workaround for tests '''
        if not getattr(self, '_khl'):
            self._khl = League.objects.get(en_title='KHL')
        return self._khl

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404()
        return super(ClubPlayerMatchTemplate, self).dispatch(request, *args, **kwargs)

    def get_cps(self, players, league, up_league=None):
        _ul = up_league or self.khl
        for plr in players:
            cps = plr.clubplayer_set.filter(league=league)
            last_cp = cps.order_by('season__end_date').last()
            season = last_cp and last_cp.season
            if last_cp.clubplayermatch_set.count() > 29 and season:
                next_season = Season.objects.get_next_season(season)
                up_cps = plr.clubplayer_set.filter(league=_ul, season=next_season)
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
        aggr = itertools.chain(map(Avg,('goals', 'assists', 'points', 'sf',)))
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
        m2vhl_plrs = Player.objects.filter(id__in=mhl_plr_ids & vhl_plr_ids)
        for k,qs,league,ul in (
                            ('vhl2khl', vhl_plrs, vhl, self.khl),
                            ('mhl2khl', mhl_plrs, mhl, self.khl),
                            ('mhl2vhl', m2vhl_plrs, vhl, mhl),
        ):
            kwargs['leagues'][k] = self.get_players_data(qs, league, ul)
        return kwargs

    def get_players_data(self, qs, league, up_league=None):
        res=dict(   def_p=dict(up=list(), down=list()),
                    off_p=dict(up=list(), down=list()),
                    keeper_sf=dict(up=list(), down=list())
        )
        for cps, up_cps in self.get_cps(qs, league, up_league):
            player = cps.player
            _ul_val = self.aggregate_values(self.get_up_league_qs(up_cps))
            _dl_val = self.aggregate_values(cps.clubplayermatch_set.all())
            res[player.id] = dict(
                player=player,
                down_league=_dl_val,
                up_league=_ul_val,
            )
            if player.line == 1: #keeper
                if _dl_val['sf__avg']:
                    res['keeper_sf']['down'].append(_dl_val['sf__avg'])
                if _ul_val['sf__avg']:
                    res['keeper_sf']['up'].append(_ul_val['sf__avg'])
            if player.line == 2: #defender
                if _dl_val['points__avg']:
                    res['def_p']['down'].append(_dl_val['points__avg'])
                if _ul_val['points__avg']:
                    res['def_p']['up'].append(_ul_val['points__avg'])
            if player.line == 3: #offender
                if _dl_val['points__avg']:
                    res['off_p']['down'].append(_dl_val['points__avg'])
                if _ul_val['points__avg']:
                    res['off_p']['up'].append(_ul_val['points__avg'])
        for root_key in ('keeper_sf', 'def_p', 'off_p'):
            for key in ('up', 'down'):
                res[root_key][key] = self.get_average(res[root_key][key])
            res[root_key]['q'] = res[root_key]['up']/res[root_key]['down']
        return res

    def  get_average(self, lst=None):
        lst = lst or []
        if len(lst) > 2:
            _min = numpy.min(lst)
            _max = numpy.max(lst)
            lst.remove(_min)
            lst.remove(_max)
        _avg = numpy.average(lst)
        _median = numpy.median(lst)
        _mean = numpy.mean(lst)
        lst=(_avg+_median+_mean)/3.0
        return lst
cpmat = ClubPlayerMatchTemplate.as_view()
