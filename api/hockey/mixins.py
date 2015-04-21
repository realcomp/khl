# -*- coding: utf-8 -*-
from base.models import Season
from hockeyapp.models import League, LeagueClub


class ClubListMixin(object):
    def _get_season(self):
        default = Season.objects.latest('start_date')
        return self.request.GET.get('season', default)

    def _get_leagues(self):
        leagueclubs = LeagueClub.objects.filter(season=self._get_season())
        return League.objects.filter(pk__in=leagueclubs.values_list('league'))

    def _get_league(self):
        if 'league' in self.request.GET:
            league = self.request.GET['league']
            if league:  # selected
                return League.objects.get(pk=league)
            else:  # default
                leagues = self._get_leagues()
                khl = leagues.filter(ru_title='КХЛ')
                if khl.exists():
                    return khl.last()
                superleague = leagues.filter(ru_title='Суперлига')
                if superleague.exists():
                    return superleague.last()
                return leagues.last()
