#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp.parsers.club import GetAllClubURLs


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py get_all_club_datas'

    def handle(self, *args, **options):
        links = GetAllClubURLs().get_page()
        print(links)
        return 'done'
        