#coding: utf-8
from __future__ import print_function
from django.core.management import BaseCommand
from hockeyapp.tasks import async_hockey_matches_parser


class Command(BaseCommand):
    help = 'Hockey match parser. Use: ./manage.py hockey_match_parse <from_id> <count>'

    def handle(self, *args, **options):
        firstid = int(args[0])
        matches = int(args[1])
        async_hockey_matches_parser.delay(firstid, matches)
        return 'done'
        