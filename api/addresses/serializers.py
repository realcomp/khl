# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from api.base.serializers import TitleBaseSerializer

from addresses.models import Address, City, Country


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