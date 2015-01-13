# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.utils import timezone

from rest_framework import fields, serializers

from addresses.models import Address, Country

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
    get_fio = lambda self, obj: self._get_field(obj, 'fio')


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

    def get_age(self, obj):
        if obj.birth_date:
            delta = relativedelta.relativedelta(
                timezone.now().date(), obj.birth_date)
            return delta.years, delta.months
        return None, None


class PlayerCardSerializer(BasePlayerCardSerializer):
    line = serializers.ReadOnlyField(source='get_line_display')
    contract_to = serializers.SerializerMethodField()
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    khl_url = serializers.SerializerMethodField()
    # last_clubs = PlayerClubSerializer(many=True)
    last_clubs = serializers.SerializerMethodField()
    url = serializers.ReadOnlyField(source='get_absolute_url')
    citizenship = CountrySerializer()

    def get_contract_to(self, obj):
        return obj.contract_to and obj.contract_to.strftime('%d.%m.%Y')

    def get_birth_date(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d %B %Y')

    def get_birth_date_short(self, obj):
        return obj.birth_date and obj.birth_date.strftime('%d.%m.%Y')

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
            'contract_to', 'number')
        model = Player


class CoachSerializer(AbstractManSerializer):
    class Meta(object):
        fields = 'pk', 'fio'
        model = Coach


class ArenaSerializer(TitleBaseSerializer):
    photo = fields.ReadOnlyField(source='photo.url')
    url = fields.ReadOnlyField(source='get_absolute_url')

    class Meta(object):
        fields = 'pk', 'title', 'photo', 'capacity', 'site', 'contacts', 'url'
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


class ClubPlayerSerializer(AbstractManSerializer):
    line = fields.ReadOnlyField(source='get_line_display')
    club = ClubListSerializer()
    photo = fields.ReadOnlyField(source='photo.url')

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'club', 'photo', 'number')
        model = Player


class ClubSerializer(ClubListSerializer):
    all_players = ClubPlayerSerializer(many=True)
    current_offender_players = ClubPlayerSerializer(many=True)
    current_defender_players = ClubPlayerSerializer(many=True)
    current_goalkeeper_players = ClubPlayerSerializer(many=True)
    coach = CoachSerializer()

    class Meta(object):
        fields = (
            'pk', 'title', 'logo', 'site', 'contacts', 'coach', 'arena',
            'address', 'all_players', 'current_offender_players',
            'current_defender_players', 'current_goalkeeper_players', 'coach',
            'url')
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
            'contract_type', 'height', 'weight', 'age')
        model = Player
