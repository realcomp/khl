#coding: utf-8
from __future__ import unicode_literals, print_function
import itertools

from django.core.management import BaseCommand
from django.db.models import Avg

from base.models import Season
from hockeyapp import models

class Command(BaseCommand):
    help = '''Use: ./manage.py check_players_stats'''
    khl = models.League.objects.get(en_title='KHL')


    def handle(self, *args, **options):
        vhl = models.League.objects.get(en_title='VHL')
        mhl = models.League.objects.get(en_title='MHL')
        cp = models.ClubPlayer.objects.filter(clubplayermatch__gte=30)
        mhl_plr_ids = set(cp.filter(league=mhl).values_list('player', flat=True))
        vhl_plr_ids = set(cp.filter(league=vhl).values_list('player', flat=True))
        khl_plr_ids = set(cp.filter(league=self.khl).values_list('player', flat=True))
        res = dict(mhl2khl={}, vhl2khl={}, mhl2vhl={})
        vhl_plrs = models.Player.objects.filter(id__in=vhl_plr_ids & khl_plr_ids)
        for cps, up_cps in self.get_cps(vhl_plrs, vhl):
            player = cps.player
            _up_cpms = self.get_up_league_qs(up_cps)
            _down_cpms = cps.clubplayermatch_set.all()
            res['vhl2khl'][player.id] = dict(
                player=player,
                down_league=self.aggregate_values(_down_cpms),
                up_league=self.aggregate_values(_up_cpms),
            )
            print(res['vhl2khl'][player.id])
        mhl_plrs = models.Player.objects.filter(id__in=mhl_plr_ids & khl_plr_ids)
        return 'done'

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
            return models.ClubPlayerMatch.objects.filter(
                                            pk__in=set(itertools.chain(*ids)))
        else:
            return up_cps.last().clubplayermatch_set.all()

    def aggregate_values(self, qs):
        aggr = itertools.chain(map(Avg,('goals', 'assists', 'points',
                                        'plus_minus', 'saves','loose_goals')))
        return qs.aggregate(*aggr)  