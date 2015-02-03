#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp import parsers


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py get_all_club_datas'

    def handle(self, *args, **options):
        for links, club_parser in ( 
            (parsers.club.KHLClubURLs().get_page(), parsers.club.KHLClubInfo), 
            (parsers.club.VHLClubURLs().get_page(), parsers.club.VHLClubInfo),
            (parsers.club.MHLClubURLs().get_page(), parsers.club.MHLClubInfo),
            (parsers.club.MHL2ClubURLs().get_page(), parsers.club.MHL2ClubInfo),
        ):
            if club_parser:
                self.update_clubs(links, club_parser)
        return 'done'


    def update_clubs(self, links, club_parser):
        for link in links:
            print(link, end='')
            club_parser().put_data_in_db_from_page(link[:-1]) #remove last slash
            print('\tok')