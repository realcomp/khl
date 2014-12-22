#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp.parsers.club import GetAllClubURLs, ClubInfo


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py get_all_club_datas'

    def handle(self, *args, **options):
        links = GetAllClubURLs().get_page()
        for link in links:
            print(link,'...')
            ClubInfo().put_data_in_db_from_page(link[:-1]) #remove last slash
            print('\tok')
        return 'done'
        