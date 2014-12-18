#coding: utf-8
from __future__ import print_function
from django.core.management import BaseCommand

from hockeyapp.parsers import HockeyMatchParser#, GetPlayerInfo
#from hockeyapp.tasks import async_hockey_match_parser
#from hockeyapp.models import Player


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py hockey_match_parse <from_id> <count>'

    def handle(self, *args, **options):
        firstid = int(args[0])
        matches = int(args[1])
        for matchid in (firstid+i for i in range(matches)):
            #async_hockey_match_parser.delay(matchid)
            HockeyMatchParser().put_data_in_db_from_page(matchid)
            #HockeyMatchParser().get_page(matchid)
            #print(HockeyMatchParser().get_page(matchid))
            print(matchid,'\tok')
        #print(GetPlayerInfo().get_page(4202))
        #Player.objects.get_or_create_player(khl_id=4202)
        return 'done'
        