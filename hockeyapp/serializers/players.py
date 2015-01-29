# -*- coding: utf-8 -*-
from functools import partial
from operator import itemgetter

from django.db.models import Sum

from rest_framework import serializers

from ..models import AdvancedPlayerStats, ClubPlayerMatch


class AdvancedPlayerStatsSerializer(serializers.ModelSerializer):
    class Meta(object):
        fields = (
            'pk', 'fiver', 'shots_1th', 'shots_2nd', 'shots_3th', 'shots_all',
            'faceoff_1th', 'faceoff_2nd', 'faceoff_3th', 'faceoff_all',
            'change_count_1th', 'change_count_2nd', 'change_count_3th',
            'gamingtime_1th', 'gamingtime_2nd', 'gamingtime_3th',
            'change_count_all', 'gamingtime_all', 'block_1th', 'hit_1th',
            'foul_1th', 'block_2nd', 'hit_2nd', 'foul_2nd', 'block_3th',
            'hit_3th', 'foul_3th', 'block_all', 'hit_all', 'foul_all')
        model = AdvancedPlayerStats


class ClubPlayerMatchSerilizer(serializers.ModelSerializer):
    count = serializers.SerializerMethodField()
    date = serializers.DateTimeField()
    plus_minus = serializers.SerializerMethodField()
    penalty_time = serializers.SerializerMethodField()
    ev_goals = serializers.SerializerMethodField()
    pp_goals = serializers.SerializerMethodField()
    es_goals = serializers.SerializerMethodField()
    overtime_goals = serializers.SerializerMethodField()
    win_goals = serializers.SerializerMethodField()
    bullet_goals = serializers.SerializerMethodField()
    shots = serializers.SerializerMethodField()
    pis = serializers.SerializerMethodField()
    faceoff = serializers.SerializerMethodField()
    winfaceoff = serializers.SerializerMethodField()
    winfaceoff_p = serializers.SerializerMethodField()
    goals = serializers.SerializerMethodField()
    score = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.count()

    def get_plus_minus(self, obj):
        return obj._aggregate.get('plus_minus__sum') or 0

    def get_penalty_time(self, obj):
        return obj._aggregate.get('penalty_time__sum') or 0

    def get_ev_goals(self, obj):
        return obj._aggregate.get('ev_goals__sum') or 0

    def get_pp_goals(self, obj):
        return obj._aggregate.get('pp_goals__sum') or 0

    def get_es_goals(self, obj):
        return obj._aggregate.get('es_goals__sum') or 0

    def get_overtime_goals(self, obj):
        return obj._aggregate.get('overtime_goals__sum') or 0

    def get_win_goals(self, obj):
        return obj._aggregate.get('win_goals__sum') or 0

    def get_bullet_goals(self, obj):
        return obj._aggregate.get('bullet_goals__sum') or 0

    def get_shots(self, obj):
        return obj._aggregate.get('shots__sum') or 0

    def get_pis(self, obj):
        return obj._aggregate.get('pis__sum') or 0

    def get_faceoff(self, obj):
        return obj._aggregate.get('faceoff__sum') or 0

    def get_winfaceoff(self, obj):
        return obj._aggregate.get('winfaceoff__sum') or 0

    def get_winfaceoff_p(self, obj):
        return obj._aggregate.get('winfaceoff_p__sum') or 0

    def get_goals(self, obj):
        return sum(map(lambda x: obj._aggregate.get(x) or 0, (
            'ev_goals', 'pp_goals', 'es_goals', 'overtime_goals')))

    def get_score(self, obj):
        # TODO: добавить передачи к сумме
        return sum(map(lambda x: obj._aggregate.get(x) or 0, (
            'ev_goals', 'pp_goals', 'es_goals', 'overtime_goals')))

    class Meta(object):
        fields = (
            'count', 'date',
            'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals', 'es_goals',
            'overtime_goals', 'win_goals', 'bullet_goals', 'shots', 'pis',
            'faceoff', 'winfaceoff', 'winfaceoff_p',
            'goals', 'score')
        model = ClubPlayerMatch
