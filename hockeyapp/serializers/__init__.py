# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from addresses.models import Address, Country, City
from base.models import Season
from base.serializers import LangDepSerializer, TitleBaseSerializer

from ..models import (
    Coach, Arena, Club, Player, League, ClubPlayer, ClubPlayerMatch)


class AbstractManSerializer(LangDepSerializer):
    fio = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    get_fio = lambda self, obj: self._get_field(obj, 'fio')
    get_name = lambda self, obj: self._get_field(obj, 'name')
    get_lastname = lambda self, obj: self._get_field(obj, 'lastname')


class CountrySerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = Country

class CitySerializer(TitleBaseSerializer):
    country = CountrySerializer()

    class Meta(object):
        fields = 'pk', 'title', 'country'
        model = City

class AddressSerializer(TitleBaseSerializer):
    city = CitySerializer()

    class Meta(object):
        fields = 'pk', 'title', 'city'
        model = Address


class LeagueSerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = League


class CountryLeaguesSerializer(CountrySerializer):
    league_set = LeagueSerializer(many=True)

    class Meta(CountrySerializer.Meta):
        fields = 'pk', 'title', 'code', 'league_set'


class CoachSerializer(AbstractManSerializer):
    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname'
        model = Coach


class SeasonSerializer(TitleBaseSerializer):
    label = serializers.SerializerMethodField()
    short_title = serializers.ReadOnlyField()

    def get_label(self, obj):
        return '%s %s-%s' % (
            _('SEASON'), obj.start_date.year, obj.end_date.year)

    class Meta(object):
        fields = (
            'pk', 'title', 'label', 'short_title', 'start_date', 'end_date')
        model = Season


class BaseClubPlayerSerializer(serializers.ModelSerializer):

    class Meta(object):
        fields = 'pk'
        model = ClubPlayer


class BaseClubSerializer(TitleBaseSerializer):
    logo = serializers.ReadOnlyField(source='logo.url')
    url = serializers.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'url')
        model = Club


class ClubLightListSerializer(BaseClubSerializer):
    title_verbose = serializers.SerializerMethodField()

    def get_title_verbose(self, obj):
        return obj.get_title_verbose(request=self.context.get('request'))

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'url', 'title_verbose',
            'main_color', 'secondary_color', 'third_color')
        model = Club


class ArenaSerializer(TitleBaseSerializer):
    photo = serializers.ReadOnlyField(source='photo.url')
    url = serializers.ReadOnlyField(source='get_absolute_url')
    club_set = ClubLightListSerializer(many=True)

    class Meta(object):
        fields = (
            'pk', 'title', 'photo', 'capacity', 'site', 'contacts', 'url',
            'coords', 'club_set')
        model = Arena


class ClubListSerializer(ClubLightListSerializer):
    address = AddressSerializer()
    arena = ArenaSerializer()
    coach = CoachSerializer()
    league = LeagueSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'url', 'title_verbose', 'address', 'arena',
            'coach', 'site', 'email', 'phone', 'league', 'main_color')
        model = Club


class BasePlayerCardSerializer(AbstractManSerializer):
    def get_age(self, obj):
        if obj.birth_date:
            delta = relativedelta.relativedelta(
                timezone.now().date(), obj.birth_date)
            return delta.years, delta.months
        return None, None

    def get_birth_date(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d %B %Y')

    def get_birth_date_short(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d.%m.%Y')

    def get_contract_to(self, obj):
        return obj.contract_to and obj.contract_to.strftime('%d.%m.%Y')

    def get_khl_url(self, obj):
        return 'http://www.khl.ru/players/%s/' % obj.khl_id


class ClubPlayerSerializer(serializers.ModelSerializer):
    season = SeasonSerializer()
    club = ClubLightListSerializer()
    club_url = serializers.ReadOnlyField()

    class Meta(object):
        fields = 'pk', 'season', 'club', 'club_url'
        model = ClubPlayer


class PlayerCardSerializer(BasePlayerCardSerializer):
    club = ClubLightListSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    age = serializers.SerializerMethodField()
    contract_type = serializers.ReadOnlyField(
        source='get_contract_type_display')
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    url = serializers.ReadOnlyField(source='get_absolute_url')
    citizenship = CountrySerializer()
    line_display = serializers.ReadOnlyField(source='get_line_display')
    contract_to = serializers.SerializerMethodField()
    khl_url = serializers.SerializerMethodField()

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short', 'club',
            'url', 'citizenship', 'grip', 'wiki_page', 'contract_type',
            'contract_to', 'number', 'line_display', 'name', 'lastname')
        model = Player


class LastClubPlayerMatchSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='match.date')
    gamingtime_m = serializers.SerializerMethodField()

    def get_gamingtime_m(self, obj):
        return (obj.gamingtime or 0) / 60

    class Meta(object):
        fields = 'pk', 'date', 'gamingtime_m'
        model = ClubPlayerMatch


class PlayerCardDetailSerializer(PlayerCardSerializer):
    club = ClubListSerializer()
    last_match = LastClubPlayerMatchSerializer()

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short', 'club', 'line',
            'url', 'citizenship', 'grip', 'wiki_page', 'contract_type',
            'contract_to', 'number', 'line_display', 'name', 'lastname',
            'seasons_total', 'matches_total', 'goals_total', 'assists_total',
            'points_total', 'plus_minus_total', 'penalty_time_total',
            'goals_average', 'assists_average', 'points_average',
            'plus_minus_average', 'penalty_time_average', 'gamingtime_total',
            'seasons_total_index', 'matches_total_index', 'goals_total_index',
            'assists_total_index', 'points_total_index',
            'plus_minus_total_index', 'penalty_time_total_index',
            'goals_average_index', 'assists_average_index',
            'points_average_index', 'plus_minus_average_index',
            'penalty_time_average_index',
            'bullet_matches_total', 'zero_goals_matches_total',
            'shots_received_total', 'saves_total', 'loose_goals_total',
            'saves_p_average', 'sf_average', 'matches_win_total',
            'matches_lose_total',
            'bullet_matches_total_index', 'zero_goals_matches_total_index',
            'shots_received_total_index', 'saves_total_index',
            'saves_p_average_index', 'sf_average_index',
            'loose_goals_total_index', 'matches_win_total_index',
            'matches_lose_total_index', 'gamingtime_total_index',
            'fb', 'vk', 'last_match',
            )
        model = Player


class MetricsPlayerSerializer(BasePlayerCardSerializer):
    club = ClubLightListSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    age = serializers.SerializerMethodField()
    contract_type = serializers.ReadOnlyField(
        source='get_contract_type_display')
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    url = serializers.SerializerMethodField()
    citizenship = CountrySerializer()

    def get_url(self, obj):
        return reverse('hockeyapp:metrics-player-card', kwargs={'pk': obj.pk})

    class Meta(object):
        fields = (
            'pk', 'fio', 'name', 'lastname', 'club', 'photo',
            'url', 'line', 'grip',
            'contract_type', 'height', 'weight', 'age',
            'birth_date', 'birth_date_short', 'citizenship')
        model = Player
