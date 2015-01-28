from functools import partial

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
    # adv_stats = AdvancedPlayerStatsSerializer()
    match_date = serializers.SerializerMethodField()
    goals = serializers.SerializerMethodField()

    def get_match_date(self, obj):
        return obj.match_date.strftime('%d.%m.%Y %H:%M')

    def get_goals(self, obj):
        return sum(map(
            partial(getattr, obj),
            ('ev_goals', 'pp_goals', 'es_goals', 'overtime_goals')))

    class Meta(object):
        fields = (
            'pk', 'match_date', #'adv_stats',
            'plus_minus',
            'penalty_time', 'ev_goals', 'pp_goals', 'es_goals',
            'overtime_goals', 'win_goals', 'bullet_goals', 'shots', 'pis',
            'faceoff', 'winfaceoff', 'winfaceoff_p', 'loose_goals',
            'saves', 'saves_p', 'sf', 'gamingtime', 'goals')
        model = ClubPlayerMatch
