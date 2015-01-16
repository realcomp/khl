#coding: utf-8
from __future__ import print_function

from django.core.management import BaseCommand

from hockeyapp.models import Judge


class Command(BaseCommand):
    help = 'Correcing jduges name and relations. Use: ./manage.py correct_judges'

    def handle(self, *args, **options):
        judges = Judge.objects.filter(ru_fio__icontains='          ')
        for j in judges:
            print(j)
            print(j.matchjudges.all())
            mjs = j.matchjudges.exists()
            mljs = j.matchlinejudges.exists()
            first = j.ru_fio.split('          ')[0].strip()
            second = j.ru_fio.split('          ')[2].strip()
            for _j in (first, second):
                exist_judge = Judge.objects.filter(ru_fio=_j).last()
                if not exist_judge:
                    exist_judge, _crt = Judge.objects.get_or_create(ru_fio=_j)
                if mjs:
                    exist_judge.matchjudges.add(*j.matchjudges.all())
                if mljs:
                    exist_judge.matchlinejudges.add(*j.matchlinejudges.all())
        judges.delete()
        return 'done'
        