# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializers


class RegistrationSer(serializers.ModelSerializer):
    class Meta(object):
        model = get_user_model()
        fields = 'username', 'fio', 'id', 'password'
        write_only_fields = 'password',
        read_only_fields = 'id',


class ProfileSerializer(serializers.ModelSerializer):
    date_joined = serializers.SerializerMethodField()

    def get_date_joined(self, obj):
        return obj.date_joined and obj.date_joined.strftime('%d %B %Y')

    class Meta(object):
        fields = 'pk', 'username', 'email', 'fio', 'date_joined'
        model = get_user_model()


class ProfileUpdateSerializer(serializers.ModelSerializer):
    # def update(self, instance, validated_data):
    #     password = validated_data.pop('password')
    #     instance.set_password(password)
    #     instance.save()
    #     super(ProfileUpdateSerializer, self).update(instance, validated_data)

    class Meta(object):
        fields = 'pk', 'email', 'fio'#, 'password'
        model = get_user_model()
        read_only_fields = 'pk',
