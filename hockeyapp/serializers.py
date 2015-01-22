# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import fields, serializers

from addresses.models import Address, Country
from base.models import Season

from .models import Coach, Arena, Club, Player, League


class LangDepSerializer(serializers.ModelSerializer):
    '''
    Language-Dependent Serializer
    '''
    def _get_field(self, obj, field_name):
        request = self.context.get('request')
        get_field_name = lambda lang: '%s_%s' % (lang or 'en', field_name)
        lang = request and request.LANGUAGE_CODE
        if hasattr(obj, get_field_name(lang)):
            return getattr(obj, get_field_name(lang))
        return getattr(obj, get_field_name(None))


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


class PlayerClubSerializer(TitleBaseSerializer):
    address = AddressSerializer()
    url = fields.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = 'pk', 'title', 'address', 'url'
        model = Club


class BasePlayerCardSerializer(AbstractManSerializer):
    club = PlayerClubSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    age = serializers.SerializerMethodField()
    photo = serializers.ReadOnlyField(source='photo.url')
    contract_type = serializers.ReadOnlyField(
        source='get_contract_type_display')
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    url = serializers.ReadOnlyField(source='get_absolute_url')

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


class PlayerCardSerializer(BasePlayerCardSerializer):
    line_display = serializers.ReadOnlyField(source='get_line_display')
    contract_to = serializers.SerializerMethodField()
    khl_url = serializers.SerializerMethodField()
    # last_clubs = PlayerClubSerializer(many=True)
    last_clubs = serializers.SerializerMethodField()
    citizenship = CountrySerializer()

    def get_contract_to(self, obj):
        return obj.contract_to and obj.contract_to.strftime('%d.%m.%Y')

    def get_khl_url(self, obj):
        return 'http://www.khl.ru/players/%s/' % obj.khl_id

    def get_last_clubs(self, obj):
        players_clubs = getattr(self.context['view'], 'players_clubs', {})
        return PlayerClubSerializer(
            players_clubs.get(obj.pk), many=True, context=self.context).data

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short', 'club', 'last_clubs',
            'url', 'citizenship', 'grip', 'wiki_page', 'contract_type',
            'contract_to', 'number', 'line_display', 'name', 'lastname')
        model = Player


class CoachSerializer(AbstractManSerializer):
    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname'
        model = Coach


class ArenaSerializer(TitleBaseSerializer):
    photo = fields.ReadOnlyField(source='photo.url')
    url = fields.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = (
            'pk', 'title', 'photo', 'capacity', 'site', 'contacts', 'url',
            'coords')
        model = Arena


class ClubListSerializer(TitleBaseSerializer):
    logo = fields.ReadOnlyField(source='logo.url')
    coach = CoachSerializer()
    arena = ArenaSerializer()
    # players
    # farm_club
    # junior_club
    address = AddressSerializer()
    url = fields.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'address', 'url')
        model = Club


class ClubPlayerSerializer(BasePlayerCardSerializer):
    line_display = fields.ReadOnlyField(source='get_line_display')
    club = ClubListSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    is_joined = serializers.ReadOnlyField()
    is_left = serializers.ReadOnlyField()

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'line_display', 'club', 'photo', 'number',
            'birth_date', 'birth_date_short', 'contract_type', 'age', 'url',
            'name', 'lastname', 'is_joined', 'is_left', 'is_legionnaire')
        model = Player


class ClubCoachSerializer(CoachSerializer):
    is_joined = serializers.ReadOnlyField()
    is_left = serializers.ReadOnlyField()

    class Meta(object):
        fields = 'pk', 'fio', 'name', 'lastname', 'is_joined', 'is_left'
        model = Player


class SeasonSerializer(TitleBaseSerializer):
    label = serializers.SerializerMethodField()

    def get_label(self, obj):
        return '%s %s-%s' % (
            _('SEASON'), obj.start_date.year, obj.end_date.year)

    class Meta(object):
        fields = 'pk', 'title', 'label'
        model = Season


class ClubSerializer(ClubListSerializer):
    seasons = SeasonSerializer(many=True)
    prev_season = serializers.SerializerMethodField()
    all_players = serializers.SerializerMethodField()
    offender_players = serializers.SerializerMethodField()
    defender_players = serializers.SerializerMethodField()
    goalkeeper_players = serializers.SerializerMethodField()
    coaches = serializers.SerializerMethodField()

    _seasons_selected = None
    _players = None
    _coaches = None

    def _get_seasons(self, obj):
        if not self._seasons_selected:
            request = self.context.get('request')
            try:
                season = obj.seasons.get(pk=request.GET.get('season'))
            except Season.DoesNotExist:
                season = obj.seasons[0]
            self._seasons_selected = (
                obj.get_prev_season(season) or season,
                season,
                obj.get_next_season(season) or season,
            )
        return self._seasons_selected

    def get_prev_season(self, obj):
        return SeasonSerializer(
            self._get_seasons(obj)[0], context=self.context).data

    def _get_players(self, obj):
        if self._players:
            return self._players
        clubplayers = map(
            lambda x: obj.clubplayer_set.filter(season=x),
            self._get_seasons(obj))
        players = map(
            lambda x: set(Player.objects.filter(clubplayer__in=x)),
            clubplayers)
        joined = players[1] - players[0]  # joined club in current season
        left = players[1] - players[2]  # left club in next season
        self._players = players[1]  # middle one is the current season
        for player in self._players:
            player.is_joined = player in joined
            player.is_left = player in left
        return self._players

    def _get_coaches(self, obj):
        if self._coaches:
            return self._coaches
        clubcoaches = map(
            lambda x: obj.coachclub_set.filter(season=x),
            self._get_seasons(obj))
        coaches = map(
            lambda x: set(Coach.objects.filter(coachclub__in=x)),
            clubcoaches)
        joined = coaches[1] - coaches[0]  # joined club in current season
        left = coaches[1] - coaches[2]  # left club in next season
        self._coaches = coaches[1]  # middle one is the current season
        for coach in self._coaches:
            coach.is_joined = coach in joined
            coach.is_left = coach in left
        return self._coaches

    def get_all_players(self, obj):
        players = self._get_players(obj)
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_offender_players(self, obj):
        players = filter(lambda x: x.line == 3, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_defender_players(self, obj):
        players = filter(lambda x: x.line == 2, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_goalkeeper_players(self, obj):
        players = filter(lambda x: x.line == 1, self._get_players(obj))
        return ClubPlayerSerializer(
            players, context=self.context, many=True).data

    def get_coaches(self, obj):
        coaches = self._get_coaches(obj)
        return ClubCoachSerializer(
            coaches, context=self.context, many=True).data

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'address', 'all_players', 'offender_players',
            'defender_players', 'goalkeeper_players', 'coaches',
            'url', 'seasons', 'prev_season')
        model = Club


class MetricsPlayerSerializer(BasePlayerCardSerializer):
    url = serializers.SerializerMethodField()
    line = serializers.SerializerMethodField()
    grip = serializers.SerializerMethodField()

    def get_url(self, obj):
        return reverse('hockeyapp:metrics-player-card', kwargs={'pk': obj.pk})

    def get_line(self, obj):
        return obj.get_line_display().lower()[:3]

    def get_grip(self, obj):
        return obj.grip.lower()[:3]

    class Meta(object):
        fields = (
            'pk', 'url', 'fio', 'club', 'line', 'photo', 'grip',
            'contract_type', 'height', 'weight', 'age', 'name', 'lastname',
            'birth_date', 'birth_date_short')
        model = Player
