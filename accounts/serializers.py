# coding: utf-8
from __future__ import unicode_literals

from uuid import uuid4

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import ugettext as _

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
            'name_visible', 'website', 'countries', 'clubs', 'email_validated')
        read_only_fields = 'username', 'date_joined'
        model = get_user_model()


class TokenSerializer(serializers.Serializer):
    uidb64 = serializers.CharField(max_length=255)
    token = serializers.CharField(max_length=255)

    def validate_uidb64(self, value):
        try:
            urlsafe_base64_decode(value)
        except (TypeError, ValueError, OverflowError):
            raise serializers.ValidationError(_('Password reset unsuccessful'))
        else:
            return value

    def _get_user(self):
        User = get_user_model()
        try:
            uid = urlsafe_base64_decode(self.initial_data['uidb64'])
            user = User._default_manager.get(pk=uid)
        except User.DoesNotExist:
            user = None
        return user

    def validate_token(self, value):
        user = self._get_user()
        if user is not None and default_token_generator.check_token(
                user, value):
            return value
        raise serializers.ValidationError(_('Password reset unsuccessful'))


class PasswordResetConfirmSerializer(TokenSerializer):
    password = serializers.CharField(max_length=255)

    def save(self):
        user = self._get_user()
        user.set_password(self.data['password'])
        user.save()


class EmailConfirmationSerializer(TokenSerializer):
    def save(self):
        user = self._get_user()
        user.email_validated = True
        user.save()
