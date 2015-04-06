#coding: utf-8
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

import base.tests

from hockeyapp.models import League


class AccountsTest(base.tests.BaseTest):
    def setUp(self):
        League.objects.create(en_title='KHL')

        User = get_user_model()
        self.user = User.objects.create_user(username='lost@password.com')

    def test_registration(self):
        '''
            test registration functionality
        '''
        response = self.client.get(reverse('accounts:signup'))
        self.assertEqual(response.status_code, 200)

    def test_registration_api(self):
        response = self.client.post(
            reverse('accounts:registration-api'),
            data={
                'username': 'test1@test.com',
                'password': '123456'
            }
        )
        self.assertEqual(response.status_code, 201)

    def test_password_reset_api(self):
        response = self.client.post(
            reverse('accounts:password-reset-api'),
            data={'email': self.user.username})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('accounts:password-reset-api'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['email'][0]['code'], 'required')
