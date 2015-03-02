# coding: utf-8
from __future__ import unicode_literals

from base.tests import BaseTest


class BaseAPITest(BaseTest):
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