# coding: utf-8
from __future__ import unicode_literals

from uuid import uuid4
from StringIO import StringIO
import PIL

from django.contrib.auth import get_user_model

from rest_framework import serializers

from filer.models import Folder, Image

from .utils import make_avatar


class RegistrationSer(serializers.ModelSerializer):
    def save(self):
        obj = super(RegistrationSer, self).save()
        obj.set_password(self.data['password'])
        obj.save()

    class Meta(object):
        model = get_user_model()
        fields = 'username', 'fio', 'id', 'password', 'email_notification'
        # write_only_fields = 'password',
        read_only_fields = 'id',


class ProfileVersionSerializer(serializers.ModelSerializer):
    class Meta(object):
        fields = 'pk', 'version'
        model = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class AvatarField(serializers.Field):
        def get_attribute(self, obj):
            return obj

        def to_representation(self, obj):
            return obj.avatar and obj.avatar.url

        def to_internal_value(self, data):
            name = str(uuid4()) + '.jpeg'
            folder, fcreated = Folder.objects.get_or_create(name='User avatar')
            image, icreated = Image.objects.get_or_create(
                folder=folder, name=name, is_public=True)
            image.file.save(name, make_avatar(data, name, (70, 85)))
            return image

    date_joined = serializers.SerializerMethodField()
    avatar = AvatarField(required=False)

    def get_date_joined(self, obj):
        return obj.date_joined and obj.date_joined.strftime('%d %B %Y')

    def validate_avatar(self, value):
        # TODO: validate image format and size
        return value

    class Meta(object):
        fields = (
            'pk', 'username', 'email', 'fio', 'date_joined', 'avatar',
            'name_visible', 'website', 'countries', 'clubs')
        read_only_fields = 'username', 'date_joined'
        model = get_user_model()
