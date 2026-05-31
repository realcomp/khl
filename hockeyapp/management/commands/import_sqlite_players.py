# -*- coding: utf-8 -*-
"""
Импортирует игроков, статистику и фотографии из players_parsed.sqlite3 в Postgres.

Использование:
    python manage.py import_sqlite_players
    python manage.py import_sqlite_players --db /app/media/players_parsed.sqlite3
    python manage.py import_sqlite_players --dry-run
    python manage.py import_sqlite_players --skip-photos
    python manage.py import_sqlite_players --skip-stats
"""
from __future__ import unicode_literals

import datetime
import os
import sqlite3

from django.conf import settings
from django.core.files import File as DjangoFile
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option


MONTHS_RU = {
    'января': 1, 'февраля': 2, 'марта': 3, 'апреля': 4,
    'мая': 5, 'июня': 6, 'июля': 7, 'августа': 8,
    'сентября': 9, 'октября': 10, 'ноября': 11, 'декабря': 12,
}


def parse_birth_date(s):
    """'25 июня 1984' -> datetime.date(1984, 6, 25), or None."""
    if not s:
        return None
    parts = s.strip().split()
    if len(parts) != 3:
        return None
    try:
        day = int(parts[0])
        month = MONTHS_RU.get(parts[1].lower())
        year = int(parts[2])
        if month and 1900 < year < 2100:
            return datetime.date(year, month, day)
    except (ValueError, TypeError):
        pass
    return None


class Command(BaseCommand):
    help = 'Import players, stats and photos from players_parsed.sqlite3'

    option_list = BaseCommand.option_list + (
        make_option(
            '--db',
            dest='db',
            default=os.path.join(settings.BASE_DIR, 'players_parsed.sqlite3'),
            help='Path to players_parsed.sqlite3',
        ),
        make_option(
            '--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help='Show what would be done without writing to DB',
        ),
        make_option(
            '--skip-photos',
            action='store_true',
            dest='skip_photos',
            default=False,
            help='Do not import photos into filer',
        ),
        make_option(
            '--skip-stats',
            action='store_true',
            dest='skip_stats',
            default=False,
            help='Do not import PlayerSeasonStat records',
        ),
    )

    def handle(self, *args, **options):
        db_path = options['db']
        dry_run = options['dry_run']
        skip_photos = options['skip_photos']
        skip_stats = options['skip_stats']

        if not os.path.exists(db_path):
            raise CommandError('SQLite file not found: %s' % db_path)

        if dry_run:
            self.stdout.write('DRY RUN — nothing will be saved\n')

        from addresses.models import Country
        from filer.models import Image as FilerImage
        from hockeyapp.models.players import Player
        from hockeyapp.models.clubs import Club

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row

        # ── lookup caches ─────────────────────────────────────────────────────
        countries = {c.ru_title.strip(): c for c in Country.objects.all() if c.ru_title}
        clubs = {}
        for c in Club.objects.all():
            if c.ru_title:
                clubs[c.ru_title.strip()] = c
            if c.en_title:
                clubs[c.en_title.strip()] = c

        seasons = {}
        if not skip_stats:
            from base.models import Season
            for s in Season.objects.filter(start_date__isnull=False, end_date__isnull=False):
                key = '%s/%s' % (str(s.start_date.year)[2:], str(s.end_date.year)[2:])
                seasons[key] = s

        self.stdout.write('Countries: %d, Clubs: %d, Seasons: %d\n' % (
            len(countries), len(set(clubs.values())), len(seasons)))

        stats = {
            'players_created': 0,
            'players_updated': 0,
            'players_skipped': 0,
            'photos_imported': 0,
            'photos_skipped': 0,
            'stats_written': 0,
            'unmatched_clubs': set(),
            'unmatched_seasons': set(),
            'unmatched_countries': set(),
        }

        # ── import players ────────────────────────────────────────────────────
        cur = conn.execute('SELECT * FROM player ORDER BY khl_id')
        rows = cur.fetchall()
        self.stdout.write('Processing %d players...\n' % len(rows))

        for row in rows:
            khl_id = row['khl_id']
            if not khl_id:
                continue

            try:
                player = Player.objects.get(khl_id=khl_id)
                created = False
            except Player.DoesNotExist:
                player = Player(khl_id=khl_id)
                created = True

            changed_fields = []

            def _set_if_empty(field, value):
                if value and not getattr(player, field):
                    setattr(player, field, value)
                    changed_fields.append(field)

            _set_if_empty('ru_fio', row['ru_fio'])
            _set_if_empty('en_fio', row['en_fio'])
            _set_if_empty('url', row['url'])
            _set_if_empty('grip', row['grip'])

            if row['height'] and not player.height:
                player.height = row['height']
                changed_fields.append('height')
            if row['weight'] and not player.weight:
                player.weight = row['weight']
                changed_fields.append('weight')

            bd = parse_birth_date(row['birth_date'])
            if bd and not player.birth_date:
                player.birth_date = bd
                changed_fields.append('birth_date')

            citizenship_str = (row['citizenship'] or '').strip()
            if citizenship_str and not player.citizenship_id:
                country = countries.get(citizenship_str)
                if country:
                    player.citizenship = country
                    changed_fields.append('citizenship')
                else:
                    stats['unmatched_countries'].add(citizenship_str)

            if not dry_run and (created or changed_fields):
                player.save()

            if created:
                stats['players_created'] += 1
            elif changed_fields:
                stats['players_updated'] += 1
            else:
                stats['players_skipped'] += 1

            # ── photo ─────────────────────────────────────────────────────────
            if not skip_photos and row['photo_status'] == 'ok' and not player.photo_id:
                photo_rel = row['photo_local_path']
                photo_abs = os.path.join(settings.MEDIA_ROOT, photo_rel)
                if os.path.exists(photo_abs):
                    if not dry_run:
                        fname = os.path.basename(photo_abs)
                        with open(photo_abs, 'rb') as f:
                            filer_img = FilerImage.objects.create(
                                original_filename=fname,
                                file=DjangoFile(f, name=fname),
                            )
                        player.photo = filer_img
                        player.save(update_fields=['photo'])
                    stats['photos_imported'] += 1
                else:
                    stats['photos_skipped'] += 1

        # ── import season stats ───────────────────────────────────────────────
        if not skip_stats:
            try:
                from hockeyapp.models.players import PlayerSeasonStat
            except ImportError:
                self.stdout.write('WARNING: PlayerSeasonStat not found — skipping stats. Deploy new code + migrate first.\n')
                conn.close()
                return
            cur = conn.execute('SELECT * FROM player_stat ORDER BY id')
            stat_rows = cur.fetchall()
            self.stdout.write('Processing %d stat rows...\n' % len(stat_rows))

            player_cache = {}

            for row in stat_rows:
                khl_id = row['player_khl_id']
                if khl_id not in player_cache:
                    try:
                        player_cache[khl_id] = Player.objects.get(khl_id=khl_id)
                    except Player.DoesNotExist:
                        player_cache[khl_id] = None
                player = player_cache[khl_id]
                if not player:
                    continue

                club_name = (row['club_name'] or '').strip()
                club = clubs.get(club_name)
                if not club and club_name:
                    stats['unmatched_clubs'].add(club_name)

                season_str = (row['season_str'] or '').strip()
                season = seasons.get(season_str)
                if not season and season_str:
                    stats['unmatched_seasons'].add(season_str)

                tournament_type = row['tournament_type'] or 'regular'

                stat_kwargs = dict(
                    player=player,
                    club=club,
                    season=season,
                    tournament_type=tournament_type,
                )
                stat_values = dict(
                    is_goalie=bool(row['is_goalie']),
                    number=row['number'] or '',
                    matches=row['matches'],
                    goals=row['goals'],
                    assists=row['assists'],
                    points=row['points'],
                    plus_minus=row['plus_minus'],
                    plus=row['plus'],
                    minus=row['minus'],
                    penalty_time=row['penalty_time'],
                    es_goals=row['es_goals'],
                    pp_goals=row['pp_goals'],
                    sh_goals=row['sh_goals'],
                    overtime_goals=row['overtime_goals'],
                    win_goals=row['win_goals'],
                    bullet_goals=row['bullet_goals'],
                    shots=row['shots'],
                    pis=row['pis'],
                    shots_per_game=row['shots_per_game'],
                    faceoff=row['faceoff'],
                    winfaceoff=row['winfaceoff'],
                    winfaceoff_p=row['winfaceoff_p'],
                    icetime_per_game=row['icetime_per_game'] or '',
                    hits=row['hits'],
                    blocks=row['blocks'],
                    fouls=row['fouls'],
                    takeaways=row['takeaways'],
                    interceptions=row['interceptions'],
                    wins=row['wins'],
                    losses=row['losses'],
                    bullet_matches=row['bullet_matches'],
                    shots_received=row['shots_received'],
                    loose_goals=row['loose_goals'],
                    saves=row['saves'],
                    saves_p=row['saves_p'],
                    sf=row['sf'],
                    zero_goals_matches=row['zero_goals_matches'],
                    gamingtime=row['gamingtime'] or '',
                )

                if not dry_run:
                    obj, created = PlayerSeasonStat.objects.get_or_create(
                        defaults=stat_values,
                        **stat_kwargs
                    )
                    if not created:
                        for k, v in stat_values.items():
                            setattr(obj, k, v)
                        obj.save()

                stats['stats_written'] += 1

        conn.close()

        # ── summary ───────────────────────────────────────────────────────────
        self.stdout.write('\n=== Done ===\n')
        self.stdout.write('Players created:   %d\n' % stats['players_created'])
        self.stdout.write('Players updated:   %d\n' % stats['players_updated'])
        self.stdout.write('Players unchanged: %d\n' % stats['players_skipped'])
        self.stdout.write('Photos imported:   %d\n' % stats['photos_imported'])
        self.stdout.write('Photos missing:    %d\n' % stats['photos_skipped'])
        self.stdout.write('Stat rows written: %d\n' % stats['stats_written'])

        if stats['unmatched_countries']:
            self.stdout.write('Unmatched countries (%d): %s\n' % (
                len(stats['unmatched_countries']),
                ', '.join(sorted(stats['unmatched_countries'])[:20]),
            ))
        if stats['unmatched_clubs']:
            self.stdout.write('Unmatched clubs (%d): %s\n' % (
                len(stats['unmatched_clubs']),
                ', '.join(sorted(stats['unmatched_clubs'])[:30]),
            ))
        if stats['unmatched_seasons']:
            self.stdout.write('Unmatched seasons: %s\n' % ', '.join(
                sorted(stats['unmatched_seasons'])))
