# -*- coding: utf-8 -*-
import json

from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, permissions, response
from rest_framework.views import APIView

from ..forms import PasswordResetForm
from ..serializers import (
    ProfileSerializer, ProfileVersionSerializer, RegistrationSer)


class ProfileVersionView(generics.RetrieveUpdateAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = ProfileVersionSerializer

    def get_object(self):
        return self.request.user


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes = permissions.IsAuthenticated,
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user


class RegistrationView(generics.CreateAPIView):
    serializer_class = RegistrationSer


class PasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': 'no-reply@sportomatics.ru',
                'request': request,
            }
            form.save(**opts)
            return response.Response({}, status=200)
        else:
            return response.Response({
                'errors': json.loads(form.errors.as_json()),
            }, status=400)
