# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import rest_framework as drf

from api.base.serializers import IIFMinimalSerializer, FIFSerialiser
from hockeyapp.models import ArenaInstaPhoto, Club, Match, Player


class ClubMinimalSerialiser(drf.serializers.ModelSerializer):
    class Meta:
        model = Club
        fields = 'id', 'ru_title', 'get_absolute_url', 'arena'
        read_only_fields = fields


class ArenaInstaPhotoSerializer(drf.serializers.ModelSerializer):
    photo = IIFMinimalSerializer()
    players = drf.serializers.PrimaryKeyRelatedField(many=True, read_only=False,
            allow_null=True, queryset=Player.objects.all()
    )
    class Meta:
        model = ArenaInstaPhoto
        read_only_fields = 'photo',


class MatchMinimalSerialiser(drf.serializers.ModelSerializer):
    home_team = ClubMinimalSerialiser()
    guest_team = ClubMinimalSerialiser()
    class Meta:
        model = Match
        fields = 'id', 'home_team', 'guest_team', 'count', 'date'
        read_only_fields = fields


class PlayerMinimalSerialiser(drf.serializers.ModelSerializer):
    photo = FIFSerialiser()
    class Meta:
        model = Player
        fields = 'id', 'number', 'line', 'ru_fio', 'photo'
        read_only_fields = fields