#coding: utf-8
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

import base.tests


class AccountsTest(base.tests.BaseTest):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username='lost@password.com')

    def test_successfull_registration(self):
        '''
            test registration functionality
        '''
        _postdata = {
            'username': 'test1@test.com',
            'password1': '12345d',
            'password2': '12345d',
            'fio': 'test test'
        }
        response = self.client.post(reverse('accounts:signup'), data=_postdata)
        self.assertEqual(response.status_code, 302)

    def test_password_reset(self):
        response = self.client.post(
            reverse('accounts:password-reset-api'),
            data={'email': self.user.username})
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            reverse('accounts:password-reset-api'))
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.data['errors']['email'][0]['code'], 'required')
