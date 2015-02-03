#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp import parsers


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py get_all_club_datas'

    def handle(self, *args, **options):
        links = parsers.club.KHLClubURLs().get_page()
        for link in links:
            print(link, end='')
            parsers.club.KHLClubInfo().put_data_in_db_from_page(link[:-1]) #remove last slash
            print('\tok')
        return 'done'