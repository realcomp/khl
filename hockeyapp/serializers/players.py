# -*- coding: utf-8 -*-
from operator import attrgetter

from rest_framework import serializers

from . import SeasonSerializer, BaseClubSerializer
from ..models import AdvancedPlayerStats, ClubPlayerMatch, Club, LeagueClub


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
    '''
    Serializer for QuerySet instances with aggregated values
    '''
    class AggregateSumField(serializers.ReadOnlyField):
        def get_attribute(self, instance):
            # defined in view
            return instance._aggregate

        def to_representation(self, value):
            return value.get('%s__sum' % self.field_name) or 0

    class AggregateAvgField(serializers.ReadOnlyField):
        def get_attribute(self, instance):
            # defined in view
            return instance._aggregate

        def to_representation(self, value):
            return value.get(self.field_name) or 0

    count = serializers.SerializerMethodField()
    date = serializers.DateTimeField()
    season = SeasonSerializer()
    goals = AggregateSumField()
    assists = AggregateSumField()
    points = AggregateSumField()
    plus_minus = AggregateSumField()
    penalty_time = AggregateSumField()
    ev_goals = AggregateSumField()
    pp_goals = AggregateSumField()
    es_goals = AggregateSumField()
    overtime_goals = AggregateSumField()
    win_goals = AggregateSumField()
    bullet_goals = AggregateSumField()
    shots = AggregateSumField()
    pis__avg = AggregateAvgField()
    faceoff = AggregateSumField()
    winfaceoff = AggregateSumField()
    winfaceoff_p__avg = AggregateAvgField()
    shots__avg = AggregateAvgField()
    gamingtime__avg = AggregateAvgField()
    change_count__avg = AggregateAvgField()

    def get_count(self, obj):
        return obj.count()

    class Meta(object):
        fields = (
            'count', 'date', 'season', 'goals', 'assists', 'points',
            'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals', 'es_goals',
            'overtime_goals', 'win_goals', 'bullet_goals', 'shots', 'pis__avg',
            'faceoff', 'winfaceoff', 'winfaceoff_p__avg',
            'shots__avg', 'gamingtime__avg', 'change_count__avg')
        model = ClubPlayerMatch


class PlayerCardClubsSerializer(BaseClubSerializer):
    seasons_title = serializers.SerializerMethodField()

    def get_seasons_title(self, obj):
        # clubleague = LeagueClub.objects.get(
        #     club=obj, season=obj.selected_seasons[0])
        league_title = ''
        if obj.league:
            league_title = '%s: ' % obj.league.get_locale_attr(
                'title', request=self.context.get('request'))
        return '%(league)s%(club)s (%(seasons)s)' % {
            # 'league': clubleague.league.short_title,
            'league': league_title,
            'club': obj.get_locale_attr(
                'title', request=self.context.get('request')),
            'seasons': ' '.join(
                map(attrgetter('short_title'), obj.selected_seasons)),
        }

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'url', 'seasons_title')
        model = Club
