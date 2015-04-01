# -*- coding: utf-8 -*-
import json

from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.template import loader

from rest_framework import generics, permissions, response
from rest_framework.views import APIView

from ..forms import PasswordResetForm
from ..serializers import (
    ProfileSerializer, ProfileVersionSerializer, RegistrationSer,
    PasswordResetConfirmSerializer)


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

    def perform_create(self, serializer):
        super(RegistrationView, self).perform_create(serializer)
        user = authenticate(
            username=self.request.DATA['username'],
            password=self.request.DATA['password'])
        login(self.request, user)


class PasswordResetView(APIView):
    """
    POST:
    email - user's email
    """
    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.DATA)
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
            return response.Response(
                json.loads(form.errors.as_json()), status=400)


class PasswordResetConfirmView(generics.CreateAPIView):
    serializer_class = PasswordResetConfirmSerializer


class EmailConfirmationView(APIView):
    permission_classes = permissions.IsAuthenticated,

    def post(self, request, *args, **kwargs):
        template_name = 'accounts/email/email_confirmation.html'
        context = {
            'url': request.build_absolute_uri(
                reverse('accounts:email-confirmation')),
            'uidb64': urlsafe_base64_encode(force_bytes(request.user.pk)),
            'token': default_token_generator.make_token(request.user),
        }
        kwargs = {
            'subject': _('Sportomatics.ru E-Mail confirmation'),
            'message': 'HTML',
            'from_email': 'no-reply@sportomatics.ru',
            'recipient_list': [request.user.username],
            'html_message': loader.render_to_string(template_name, context),
        }
        from django.core.mail import send_mail
        send_mail(**kwargs)
        return response.Response({}, status=200)
