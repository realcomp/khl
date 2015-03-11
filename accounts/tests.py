#coding: utf-8
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse

import base.tests


class AccountsTest(base.tests.BaseTest):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='lost@password.com', email='lost@password.com')

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

    # def test_password_reset(self):
    #     data = {
    #         'username': self.user.username,
    #     }
    #     response = self.client.post(
    #         reverse('accounts:password-reset-api'), data=data)
    #     self.assertEqual(response.status_code, 200)
