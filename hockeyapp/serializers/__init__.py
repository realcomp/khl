# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dateutil import relativedelta

from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from rest_framework import serializers

from addresses.models import Address, Country
from base.models import Season

from ..models import Coach, Arena, Club, Player, League


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

    def get_label(self, obj):
        return '%s %s-%s' % (
            _('SEASON'), obj.start_date.year, obj.end_date.year)

    class Meta(object):
        fields = 'pk', 'title', 'label'
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
    club = ClubLightListSerializer()
    photo = serializers.ReadOnlyField(source='photo.url')
    age = serializers.SerializerMethodField()
    photo = serializers.ReadOnlyField(source='photo.url')
    contract_type = serializers.ReadOnlyField(
        source='get_contract_type_display')
    birth_date = serializers.SerializerMethodField()
    birth_date_short = serializers.SerializerMethodField()
    url = serializers.ReadOnlyField(source='get_absolute_url')
    citizenship = CountrySerializer()

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

    def get_contract_to(self, obj):
        return obj.contract_to and obj.contract_to.strftime('%d.%m.%Y')

    def get_khl_url(self, obj):
        return 'http://www.khl.ru/players/%s/' % obj.khl_id

    def get_last_clubs(self, obj):
        players_clubs = getattr(self.context['view'], 'players_clubs', {})
        return ClubLightListSerializer(
            players_clubs.get(obj.pk), many=True, context=self.context).data

    class Meta(object):
        fields = (
            'pk', 'fio', 'line', 'birth_date', 'age', 'weight', 'height',
            'photo', 'khl_url', 'birth_date_short', 'club', 'last_clubs',
            'url', 'citizenship', 'grip', 'wiki_page', 'contract_type',
            'contract_to', 'number', 'line_display', 'name', 'lastname')
        model = Player


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
