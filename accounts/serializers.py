#coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth import get_user_model

from rest_framework import serializer


class RegistrationSer(serializer.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = 'username', 'fio', 'id', 'password'
        write_only_fields = 'password',
        read_only_fields = 'id',