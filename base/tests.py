# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.db import transaction
from django.test.client import Client

from django_nose.testcases import FastFixtureTestCase


class BaseTest(FastFixtureTestCase):
    fixtures = ('',)
    def setUp(self):
        self.test_client = Client()

    @classmethod
    def _fixture_teardown(cls):
        if settings.DATABASES.get('default', {}
                            ).get('ENGINE') != 'django.db.backends.sqlite3':
            fixtures = getattr(cls, 'fixtures', None)
            _fb_should_teardown_fixtures = getattr(cls, '_fb_should_teardown_fixtures', True)
            # _fixture_teardown needs help with constraints.
            if fixtures and _fb_should_teardown_fixtures:
                call_command('flush', interactive=False, verbosity=1)
        return super(BaseTest, cls)._fixture_teardown()

    def get_simple_page(self, url, kw=None):
        kw = kw or {}
        response = self.test_client.get(reverse(url, kwargs=kw))
        self.assertEqual(response.status_code, 200)
        return response

    def get_simple_pages(self, url_lst):
        for url in url_lst:
            self.get_simple_page(url)

    def get_list_and_detail_pages(self, url_dict):
        for obj_list_url, obj_detail_url in url_dict.items():
            # get obj_list page
            response = self.get_simple_page(obj_list_url)
            ad_pk = response.context[0].get('object_list')[0].pk
            # get obj detail page
            self.get_simple_page(obj_detail_url, kw=dict(pk=ad_pk))     

    def create_page(self, url, params=None, kw=None):
        kw = kw or {}
        params = params or {}
        response = self.test_client.post(reverse(url, kwargs=kw), params)
        self.assertEqual(response.status_code, 201)
        return response

    def logining(self):
        transaction.set_autocommit(True)
        _pswd = '12345'
        _email = 'test@test.com'
        usr = User.objects.filter(email=_email, uin=_pswd).last()
        usr.set_password(_pswd)
        usr.save()
        params = { 
                    'password': _pswd,
                    'username': _email,
                }
        response=self.test_client.post(reverse('auth_login'), params)
        self.assertEqual(response.status_code, 200)


class BaseAPITest(BaseTest):
    def test_successfull_registration(self):
        _postdata = {
                        'username': 'test1@test.com',
                        'password1': '12345d',
                        'password2': '12345d',
                        'fio': 'test test'
        }
        response = self.client.post(reverse('accounts:signup'), data=_postdata)
        self.assertEqual(response.status_code, 302)

    def base_simple_tests(self):
        '''
            test base functionality
        '''
        #self.logining()
        url_lst = (
                    #'api:base_v1:media_files_list',
                )
        self.get_simple_pages(url_lst)

        url_dict = {
            #'base:ads_list': 'base:ads',
        }
        self.get_list_and_detail_pages(url_dict)

        #create
        creates = {
                    #'api:base_v1:email_file_order_create':   {
                                                    #'client': 1,
                                                    #'name': '123sda',
                                                    #'number': '',
                                                    #'org': ''
                                                #},
        }
        for url, params in creates.items():
            self.create_page(url, params)