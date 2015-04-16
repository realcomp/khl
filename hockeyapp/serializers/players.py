# -*- coding: utf-8 -*-
import itertools

from django.db.models import Avg, Sum

from rest_framework import pagination, serializers

from . import (
    AbstractManSerializer, TitleBaseSerializer, BasePlayerCardSerializer,
    SeasonSerializer, BaseClubSerializer,
    CoachSerializer, CountrySerializer, ClubLightListSerializer,
    ClubListSerializer)
from ..models import (
    AdvancedPlayerStats, ClubPlayerMatch, Club, Coach, Player)


class PlayersSearchSerializer(BasePlayerCardSerializer):
    url = serializers.ReadOnlyField(source='get_absolute_url')
    photo = serializers.ReadOnlyField(source='photo.url')
    line_display = serializers.ReadOnlyField(source='get_line_display')
    citizenship = CountrySerializer()
    #clubplayers = serializers.SerializerMethodField()
    club = ClubLightListSerializer()
    age = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    rating_index = serializers.SerializerMethodField()
    contract_to = serializers.SerializerMethodField()
    contract_type = serializers.ReadOnlyField(source='get_contract_type_display')

    #def get_clubplayers(self, obj):
        #clubplayers_data = getattr(self.context['view'], 'clubplayers', None)
        #if clubplayers_data is None:
            #clubplayers = obj.clubplayer_set.order_by('-end_date', '-pk')
        #else:
            #clubplayers = clubplayers_data.get(obj.pk)
        #return ClubPlayerSerializer(
            #clubplayers, context=self.context, many=True).data

    def get_rating(self, obj):
        rated_by = self.context['request'].GET.get('rated_by', '')
        if rated_by:
            rating = getattr(obj, rated_by, None)
            if type(rating) == float:
                rating = '%.3f' % rating
            return rating

    def get_rating_index(self, obj):
        rated_by = self.context['request'].GET.get('rated_by', '')
        if rated_by:
            return getattr(obj, '%s_index' % rated_by)
        else:
            rating = getattr(self.context['view'], 'rating', {})
            return rating.get(obj.pk)

    class Meta(object):
        fields = (
            'pk', 'url', 'photo', 'lastname', 'name', 'line_display',
            'citizenship', 'club', 'age', 'birth_date_short',
            'rating', 'rating_index', 'fio', 'contract_to', 'contract_type',
            'weight', 'height', 'grip', 'matches_total')
        model = Player


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
    class AggregateField(serializers.ReadOnlyField):
        def get_attribute(self, instance):
            if getattr(instance, '_aggregate', None) is None:
                instance._aggregate = instance.aggregate(*itertools.chain(
                    map(Sum, (
                        'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals',
                        'es_goals', 'overtime_goals', 'win_goals', 'bullet_goals',
                        'shots', 'faceoff', 'winfaceoff', 'winfaceoff_p',
                        'goals', 'assists', 'points', 'loose_goals', 'saves')),
                    map(Avg, (
                        'shots', 'pis', 'winfaceoff_p', 'saves_p', 'sf')),
                ))
            return instance._aggregate

    class AggregateSumField(AggregateField):
        def to_representation(self, value):
            return value.get('%s__sum' % self.field_name) or 0

    class AggregateAvgField(AggregateField):
        def to_representation(self, value):
            result = value.get(self.field_name)
            return ('%0.2f' % result) if result else '0'

    count = serializers.SerializerMethodField()
    start_date = serializers.SerializerMethodField()
    end_date = serializers.SerializerMethodField()
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
    gamingtime__avg = serializers.SerializerMethodField()
    change_count__avg = serializers.SerializerMethodField()
    loose_goals = AggregateSumField()
    saves = AggregateSumField()
    saves_p__avg = AggregateAvgField()
    sf__avg = AggregateAvgField()
    shots_received = serializers.SerializerMethodField()
    matches_win = serializers.SerializerMethodField()
    matches_lose = serializers.SerializerMethodField()
    zero_goals_matches = serializers.SerializerMethodField()
    bullet_matches = serializers.SerializerMethodField()

    def get_count(self, obj):
        return obj.count()

    def get_start_date(self, obj):
        if hasattr(obj, 'start_date'):
            return obj.start_date

    def get_end_date(self, obj):
        if hasattr(obj, 'end_date'):
            return obj.end_date

    def get_gamingtime__avg(self, obj):
        gamingtime_all = (
            obj.aggregate(Avg('adv_stats__gamingtime_all'))
            .get('adv_stats__gamingtime_all__avg') or 0)
        gamingtime = (
            obj.aggregate(Avg('gamingtime'))
            .get('gamingtime__avg') or 0)
        # seconds to minutes
        result = (gamingtime_all or gamingtime) / 60
        return ('%0.2f' % result) if result else '0'

    def get_change_count__avg(self, obj):
        change_count_all = (
            obj.aggregate(Avg('adv_stats__change_count_all'))
            .get('adv_stats__change_count_all__avg') or 0)
        change_count = (
            obj.aggregate(Avg('change_count'))
            .get('change_count__avg') or 0)
        result = change_count_all or change_count
        return ('%0.2f' % result) if result else '0'

    def get_shots_received(self, obj):
        loose_goals = (
            obj.aggregate(Sum('loose_goals'))
            .get('loose_goals__sum') or 0)
        saves = (
            obj.aggregate(Sum('saves'))
            .get('saves__sum') or 0)
        return loose_goals + saves

    def get_matches_win(self, obj):
        return obj.home_matches_win().count() + obj.guest_matches_win().count()

    def get_matches_lose(self, obj):
        return (
            obj.home_matches_lose().count() + obj.guest_matches_lose().count())

    def get_zero_goals_matches(self, obj):
        # at least 58 minutes
        return obj.filter(loose_goals=0, gamingtime__gte=58*60).count()

    def get_bullet_matches(self, obj):
        return obj.filter(bullet_goals__gt=0).count()

    class Meta(object):
        fields = (
            'count', 'date', 'season', 'goals', 'assists', 'points',
            'plus_minus', 'penalty_time', 'ev_goals', 'pp_goals', 'es_goals',
            'overtime_goals', 'win_goals', 'bullet_goals', 'shots', 'pis__avg',
            'faceoff', 'winfaceoff', 'winfaceoff_p__avg',
            'shots__avg', 'gamingtime__avg', 'change_count__avg',
            'start_date', 'end_date', 'loose_goals', 'saves', 'saves_p__avg',
            'sf__avg', 'shots_received', 'matches_win', 'matches_lose',
            'zero_goals_matches', 'bullet_matches',
        )
        model = ClubPlayerMatch


class ClubPlayerMatchPaginationSerilizer(pagination.PaginationSerializer):
    is_limited = serializers.SerializerMethodField()

    def get_is_limited(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated():
            return False
        return True


class PlayerCardClubsSerializer(BaseClubSerializer):
    class Meta(object):
        fields = 'pk', 'title', 'logo', 'url', 'main_color'
        model = Club


class PlayerCardCoachesSerializer(CoachSerializer):
    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname'
        model = Coach


class PlayerNamesSerializer(AbstractManSerializer):
    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname'
        model = Player


class ClubTitlesSerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = Club


class PlayerNumbersClubSerializer(ClubListSerializer):
    seasons = SeasonSerializer(many=True)

    class Meta(ClubListSerializer.Meta):
        fields = ClubListSerializer.Meta.fields + ('seasons',)
        model = Club


class PlayerNumbersSerializer(serializers.ModelSerializer):
    clubs = PlayerNumbersClubSerializer(many=True)
    number = serializers.ReadOnlyField()

    class Meta(object):
        fields = 'clubs', 'number'
        model = Player
