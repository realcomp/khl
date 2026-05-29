# coding: utf-8
"""
Django management command для импорта матчей из khl_calendar.sqlite3 в PostgreSQL.

Использование (на сервере):
    python manage.py import_khl_calendar
    python manage.py import_khl_calendar --db /path/to/khl_calendar.sqlite3
    python manage.py import_khl_calendar --dry-run        # только показать что будет
    python manage.py import_khl_calendar --update-scores  # обновить счёт у уже существующих
"""
from __future__ import unicode_literals

import logging
import sqlite3

from django.core.management.base import BaseCommand
from django.utils import timezone

log = logging.getLogger(__name__)

DEFAULT_DB = 'khl_calendar.sqlite3'

# challenge_type: 1 = Регулярный чемпионат, 2 = Плей-офф
CHALLENGE_TYPE_REG = 1
CHALLENGE_TYPE_PLAYOFF = 2

# Месяцы для парсинга даты из строки вида "20 марта 2026, Пт"
_MONTHS = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
}


def parse_date(date_str):
    """Парсит строку вида '20 марта 2026, Пт' в timezone-aware datetime."""
    if not date_str:
        return None
    try:
        # "20 марта 2026, Пт" → ["20 марта 2026", " Пт"]
        part = date_str.split(',')[0].strip()
        day, month_name, year = part.split()
        month = _MONTHS.get(month_name.lower())
        if not month:
            return None
        import datetime
        dt = datetime.datetime(int(year), month, int(day))
        return timezone.make_aware(dt, timezone.get_current_timezone())
    except Exception:
        return None


class Command(BaseCommand):
    help = 'Импортирует матчи из khl_calendar.sqlite3 в базу данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--db', default=DEFAULT_DB,
            help='Путь к SQLite-файлу (по умолчанию: khl_calendar.sqlite3)',
        )
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Только показать статистику, ничего не записывать',
        )
        parser.add_argument(
            '--update-scores', action='store_true',
            help='Обновить счёт у уже существующих Schedule/Match записей',
        )

    def handle(self, *args, **options):
        # Импортируем здесь, чтобы не ломать модуль при отсутствии Django
        from hockeyapp.models import Challenge, Schedule
        from hockeyapp.models.match import Match
        from hockeyapp.models.clubs import Club

        db_path = options['db']
        dry_run = options['dry_run']
        update_scores = options['update_scores']

        if dry_run:
            self.stdout.write('=== DRY RUN — изменения не сохраняются ===')

        rows = self._load_sqlite(db_path)
        if not rows:
            self.stderr.write('Нет данных в {}'.format(db_path))
            return

        self.stdout.write('Загружено {} матчей из {}'.format(len(rows), db_path))

        # Кешируем клубы и челленджи для скорости
        club_cache = {}    # slug → Club
        challenge_cache = {}  # season_khl_id → Challenge

        stats = {'created': 0, 'updated': 0, 'skipped': 0, 'no_club': 0}

        for row in rows:
            khl_id = row['khl_id']
            if not khl_id:
                stats['skipped'] += 1
                continue

            # --- Ищем клубы ---
            home_club = self._get_club(row['home_team'], row['home_team_slug'], club_cache)
            guest_club = self._get_club(row['guest_team'], row['guest_team_slug'], club_cache)

            if not home_club or not guest_club:
                missing = []
                if not home_club:
                    missing.append(row['home_team'])
                if not guest_club:
                    missing.append(row['guest_team'])
                self.stderr.write(
                    'Клуб не найден для матча {}: {}'.format(khl_id, ', '.join(missing))
                )
                stats['no_club'] += 1
                continue

            # --- Ищем Challenge (сезон) ---
            challenge = self._get_challenge(
                row['season_khl_id'], row['season_label'], row['is_playoff'],
                challenge_cache,
            )

            challenge_type = CHALLENGE_TYPE_PLAYOFF if row['is_playoff'] else CHALLENGE_TYPE_REG

            # --- Schedule ---
            existing_schedule = Schedule.objects.filter(khl_id=khl_id).first()

            if existing_schedule and not update_scores:
                stats['skipped'] += 1
                continue

            match_date = parse_date(row['date'])

            if not dry_run:
                if existing_schedule:
                    schedule = existing_schedule
                else:
                    schedule = Schedule(khl_id=khl_id)

                schedule.match_url = row['match_url'] or ''
                schedule.date = match_date
                schedule.challenge = challenge
                schedule.challenge_type = challenge_type
                schedule.home_team = home_club
                schedule.guest_team = guest_club
                schedule.processed = bool(row['is_finished'])
                if challenge and challenge.season:
                    schedule.season = challenge.season
                if challenge and challenge.league:
                    schedule.league = challenge.league
                schedule.save()

                # --- Match (только если матч сыгран и есть счёт) ---
                if row['is_finished'] and row['home_score'] is not None:
                    existing_match = schedule.match
                    if existing_match and not update_scores:
                        stats['skipped'] += 1
                        continue

                    if existing_match:
                        match = existing_match
                    else:
                        match = Match()

                    match.khl_id = khl_id
                    match.url = row['protocol_url'] or ''
                    match.date = match_date
                    match.home_team = home_club
                    match.guest_team = guest_club
                    match.home_score = row['home_score']
                    match.guest_score = row['guest_score']
                    match.overtime_win = bool(row['overtime'])
                    match.bullet_win = bool(row['shootout'])
                    match.count = '{}:{}'.format(row['home_score'], row['guest_score'])
                    match.challenge_type = challenge_type
                    match.save()

                    if not schedule.match:
                        schedule.match = match
                        schedule.save(update_fields=['match'])

                if existing_schedule:
                    stats['updated'] += 1
                else:
                    stats['created'] += 1
            else:
                # dry run
                action = 'update' if existing_schedule else 'create'
                self.stdout.write('  [{}] {} vs {} — {}'.format(
                    row['season_label'],
                    row['home_team'], row['guest_team'],
                    action,
                ))
                stats['created' if action == 'create' else 'updated'] += 1

        self.stdout.write('')
        self.stdout.write('Результат:')
        self.stdout.write('  Создано:         {}'.format(stats['created']))
        self.stdout.write('  Обновлено:       {}'.format(stats['updated']))
        self.stdout.write('  Пропущено:       {}'.format(stats['skipped']))
        self.stdout.write('  Не найден клуб:  {}'.format(stats['no_club']))

    def _load_sqlite(self, db_path):
        try:
            con = sqlite3.connect(db_path)
            con.row_factory = sqlite3.Row
            rows = con.execute('SELECT * FROM matches').fetchall()
            con.close()
            return [dict(r) for r in rows]
        except Exception as e:
            self.stderr.write('Ошибка чтения {}: {}'.format(db_path, e))
            return []

    def _get_club(self, title, slug, cache):
        """Ищет клуб по slug или названию, при отсутствии — создаёт минимальную запись."""
        if slug in cache:
            return cache[slug]

        from hockeyapp.models.clubs import Club

        # 1. По URL (надёжнее всего)
        club = Club.objects.filter(url__icontains='/clubs/' + slug).first()

        # 2. По точному ru_title
        if not club and title:
            club = Club.objects.filter(ru_title=title).first()

        # 3. По частичному совпадению названия
        if not club and title:
            club = Club.objects.filter(ru_title__icontains=title).first()

        # 4. Не нашли — создаём минимальную запись
        if not club and title:
            khl_url = 'https://www.khl.ru/clubs/{}/'.format(slug)
            club = Club.objects.create(ru_title=title, url=khl_url)
            log.info('Создан новый клуб: %s (%s)', title, khl_url)

        cache[slug] = club
        return club

    def _get_challenge(self, season_khl_id, season_label, is_playoff, cache):
        """Ищет Challenge по khl_id сезона."""
        if not season_khl_id:
            return None
        if season_khl_id in cache:
            return cache[season_khl_id]

        from hockeyapp.models import Challenge
        challenge = Challenge.objects.filter(khl_id=season_khl_id).first()
        cache[season_khl_id] = challenge

        if not challenge:
            log.warning(
                'Challenge не найден для khl_id=%s (%s). '
                'Создайте его вручную в админке.',
                season_khl_id, season_label,
            )
        return challenge
