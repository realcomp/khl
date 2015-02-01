#coding: utf-8
from __future__ import unicode_literals, print_function
from django.core.management import BaseCommand

from hockeyapp import parsers
from hockeyapp.tasks import async_hockey_player_update

class Command(BaseCommand):
    help = '''Hockey match parser. Use: ./manage.py get_all_players <parser_id>
            parsers:
                    1 - MHL parser,
                    2 - KHL parser,
                    3 - VHL parser,
                    4 - MHL-2 parser.
    '''


    def handle(self, *args, **options):
        parser_id = int(args[0])
        parser = {  1: parsers.player.GetAllMHLPlayerIDs,
                    2: parsers.player.GetAllKHLPlayerIDs,
                    3: parsers.player.GetAllVHLPlayerIDs,
                    4: parsers.player.GetAllMHL2PlayerIDs,
        }.get(parser_id)
        ids = parser().get_ids()
        for khl_id in set(ids):
            print(khl_id, end='')
            async_hockey_player_update.delay(khl_id, parser_id)
            print('\tok')
        return 'done'
