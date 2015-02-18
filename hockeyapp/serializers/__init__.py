# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.db.models import Avg, Sum
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from addresses.models import Address, Country
from base.models import Season

from ..models import (
    Coach, Arena, Club, Player, League, ClubPlayerMatch, ClubPlayer)


class LangDepSerializer(serializers.ModelSerializer):
    '''
    Language-Dependent Serializer
    '''
    def _get_field(self, obj, field_name):
        # request = self.context.get('request')
        # get_field_name = lambda lang: '%s_%s' % (lang or 'en', field_name)
        # lang = request and request.LANGUAGE_CODE
        # if hasattr(obj, get_field_name(lang)):
        #     return getattr(obj, get_field_name(lang))
        # return getattr(obj, get_field_name(None))
        return obj.get_locale_attr(
            field_name, request=self.context.get('request'))


class AbstractManSerializer(LangDepSerializer):
    fio = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()
    lastname = serializers.SerializerMethodField()
    get_fio = lambda self, obj: self._get_field(obj, 'fio')
    get_name = lambda self, obj: self._get_field(obj, 'name')
    get_lastname = lambda self, obj: self._get_field(obj, 'lastname')


class TitleBaseSerializer(LangDepSerializer):
    title = serializers.SerializerMethodField()
    get_title = lambda self, obj: self._get_field(obj, 'title')


class AddressSerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = Address


class CountrySerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = Country


class LeagueSerializer(TitleBaseSerializer):
    class Meta(object):
        fields = 'pk', 'title'
        model = League


class CountryLeaguesSerializer(CountrySerializer):
    league_set = LeagueSerializer(many=True)

    class Meta(CountrySerializer.Meta):
        fields = 'pk', 'title', 'league_set'


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


class ArenaSerializer(TitleBaseSerializer):
    photo = serializers.ReadOnlyField(source='photo.url')
    url = serializers.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = (
            'pk', 'title', 'photo', 'capacity', 'site', 'contacts', 'url',
            'coords')
        model = Arena


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
            'pk', 'title', 'logo', 'url', 'title_verbose')
        model = Club


class ClubListSerializer(ClubLightListSerializer):
    address = AddressSerializer()
    arena = ArenaSerializer()
    coach = CoachSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'url', 'title_verbose', 'address', 'arena',
            'coach')
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


class PlayerCardDetailSerializer(PlayerCardSerializer):
    seasons_count = serializers.SerializerMethodField()
    matches_count = serializers.SerializerMethodField()
    goals_count = serializers.SerializerMethodField()
    scored_count = serializers.SerializerMethodField()
    assisted_count = serializers.SerializerMethodField()
    goals_avg = serializers.SerializerMethodField()
    scored_avg = serializers.SerializerMethodField()
    assisted_avg = serializers.SerializerMethodField()
    plus_minus_avg = serializers.SerializerMethodField()

    _clubplayermatches = None

    def _get_clubplayermatches(self, obj):
        if self._clubplayermatches is None:
            clubplayers = obj.clubplayer_set.values_list('pk', flat=True)
            self._clubplayermatches = (
                ClubPlayerMatch.objects
                .filter(clubplayer__in=clubplayers)
                .distinct())
        return self._clubplayermatches

    def get_seasons_count(self, obj):
        pks = obj.clubplayer_set.values_list('season_id', flat=True)
        return Season.objects.filter(pk__in=pks).distinct().count()

    def get_matches_count(self, obj):
        return self._get_clubplayermatches(obj).count()

    def get_goals_count(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Sum('goals')).get('goals__sum')) or 0

    def get_scored_count(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Sum('shots')).get('shots__sum')) or 0

    def get_assisted_count(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Sum('assists')).get('assists__sum')) or 0

    def get_goals_avg(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Avg('goals')).get('goals__avg')) or 0

    def get_scored_avg(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Avg('shots')).get('shots__avg')) or 0

    def get_assisted_avg(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Avg('assists')).get('assists__avg')) or 0

    def get_plus_minus_avg(self, obj):
        return (
            self._get_clubplayermatches(obj)
            .aggregate(Avg('plus_minus')).get('plus_minus__avg')) or 0

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short', 'club',
            'url', 'citizenship', 'grip', 'wiki_page', 'contract_type',
            'contract_to', 'number', 'line_display', 'name', 'lastname',
            'seasons_count', 'matches_count',
            'goals_count', 'scored_count', 'assisted_count',
            'goals_avg', 'scored_avg', 'assisted_avg',
            'plus_minus_avg')
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
