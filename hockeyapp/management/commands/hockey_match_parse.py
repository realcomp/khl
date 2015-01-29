#coding: utf-8
from __future__ import print_function
from django.core.management import BaseCommand
from hockeyapp.tasks import async_hockey_matches_parser


class Command(BaseCommand):
    help = '''Hockey match parser.
            Use: ./manage.py hockey_match_parse <parser_id> <from_id> <count>
            parsers:
                    1 - MHL parser,
                    2 - KHL parser,
                    3 - VHL parser,
                    4 - MHL-2 parser.
    '''

    def handle(self, *args, **options):
        parserid = int(args[0])
        firstid = int(args[1])
        matches = int(args[2])
        async_hockey_matches_parser.delay(parserid, firstid, matches)
        return 'done'
        