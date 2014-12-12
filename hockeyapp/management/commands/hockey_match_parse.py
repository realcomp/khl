#coding: utf-8
from __future__ import print_function
from django.core.management import BaseCommand

from hockeyapp.utils import HockeyMatchParser#, GetPlayerInfo


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py hockey_match_parse <from_id> <count>'

    def handle(self, *args, **options):
        firstid = int(args[0])
        matches = int(args[1])
        for matchid in (firstid+i for i in range(matches)):
            HockeyMatchParser().put_data_in_db_from_page(matchid)
            #print(HockeyMatchParser().get_page(matchid))
            print(matchid,'\tok')
        #print(GetPlayerInfo().get_page(1))
        return 'done'
        