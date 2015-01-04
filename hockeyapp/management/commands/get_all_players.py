#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp.parsers.player import GetAllPlayerIDs
from hockeyapp.tasks import async_hockey_player_update

class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py get_all_players'

    def handle(self, *args, **options):
        ids = list()
        for char in b'АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЭЮЯ':
            lst_link = GetAllPlayerIDs().get_page(id=char)
            ids.extend([elem.split('/')[2] for elem in lst_link])
        for khl_id in set(ids):
            print(khl_id, end='')
            async_hockey_player_update.delay(khl_id)
            print('\tok')
        return 'done'
