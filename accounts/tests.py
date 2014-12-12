#coding: utf-8
from django.core.urlresolvers import reverse

import base.tests


class AccountsTest(base.tests.BaseTest):
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