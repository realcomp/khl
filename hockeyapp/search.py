# -*- coding: utf-8 -*-
from __future__ import unicode_literals
'''
Результаты поиска
'''
from django.db.models import Q


class SearchResult(object):
    obj = None

    def __init__(self, obj):
        self.obj = obj


class ClubSearchResult(SearchResult):
    pass


class PlayerSearchResult(SearchResult):
    pass


class SearchResultFactory(object):
    def __init__(self, sources):
        self.sources = sources

    def _get_source(self, key):
        source = self.sources.get(key)
        if source:
            return source

    def get_results(self, s):
        # TODO: обрабатывать Ё
        results = []
        results += self._search_players(s)
        return results

    def _search_clubs(self, s):
        clubs = self._get_source('club')
        if clubs:
            for club in clubs.filter(
                    Q(en_title__icontains=s) |
                    Q(ru_title__icontains=s))[:10]:
                yield ClubSearchResult(club)

    def _search_players(self, s):
        players = self._get_source('player')
        if players:
            for player in players.filter(
                    Q(en_name__icontains=s) |
                    Q(ru_name__icontains=s) |
                    Q(en_lastname__icontains=s) |
                    Q(ru_lastname__icontains=s))[:10]:
                yield PlayerSearchResult(player)
