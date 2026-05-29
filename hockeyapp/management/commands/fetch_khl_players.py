# coding: utf-8
from __future__ import unicode_literals, print_function

import datetime
import json
import logging
import os
import random
import time

import requests
from lxml import html as lxml_html

from django.core.management import BaseCommand

from addresses.models import Country
from base.models import Season
from hockeyapp.models import Club, Player, PlayerSeasonStat
from hockeyapp.parsers.player import (
    KHLPlayerPageV2, KHLPlayerSeasonStatsV2,
    _map_tournament, _map_position, _parse_int, _parse_float,
)

KHL_PLAYER_URL = 'https://www.khl.ru/players/{}/'

SESSION_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': (
        'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/avif,image/webp,*/*;q=0.8'
    ),
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
}


def _make_session():
    s = requests.Session()
    s.headers.update(SESSION_HEADERS)
    return s


def _fetch(session, player_id, retries=3):
    """Fetch player page. Returns (response, url) or raises last exception."""
    url = KHL_PLAYER_URL.format(player_id)
    last_exc = None
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=15)
            return resp, url
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
    raise last_exc


def _season_from_str(season_str):
    """
    '25/26' → Season with start_date.year == 2025.
    Finds or creates Season object.
    """
    parts = season_str.strip().split('/')
    if len(parts) != 2:
        return None
    try:
        start_year = int(parts[0].strip())
        end_year = int(parts[1].strip())
    except ValueError:
        return None

    if start_year < 100:
        start_year += 2000
    if end_year < 100:
        end_year += 2000

    season = Season.objects.filter(start_date__year=start_year).first()
    if season:
        return season

    return Season.objects.create(
        ru_title='{}/{}'.format(str(start_year)[2:], str(end_year)[2:]),
        en_title='{}/{}'.format(str(start_year)[2:], str(end_year)[2:]),
        start_date=datetime.date(start_year, 9, 1),
        end_date=datetime.date(end_year, 4, 30),
    )


def _club_from_name(club_name):
    """Find Club by ru_title (case-insensitive contains) or create stub."""
    club = Club.objects.filter(ru_title__icontains=club_name).first()
    if not club:
        club = Club.objects.create(ru_title=club_name)
    return club


def _country_from_name(name):
    if not name:
        return None
    return Country.objects.filter(ru_title__icontains=name).first()


def _parse_birth_date(s):
    if not s:
        return None
    for fmt in ('%d.%m.%Y', '%Y-%m-%d', '%d/%m/%Y'):
        try:
            return datetime.datetime.strptime(s.strip(), fmt).date()
        except ValueError:
            continue
    return None


def _coerce_stat(field, raw):
    """Convert raw string stat value to the right Python type for the field."""
    if raw in (None, '', '-', '—', '—'):
        return None

    int_fields = {
        'number', 'matches', 'goals', 'assists', 'points', 'plus', 'minus',
        'penalty_time', 'es_goals', 'pp_goals', 'sh_goals', 'overtime_goals',
        'win_goals', 'bullet_goals', 'shots', 'faceoff', 'winfaceoff',
        'hits', 'blocks', 'fouls', 'takeaways', 'interceptions',
        'wins', 'losses', 'bullet_matches', 'shots_received', 'loose_goals',
        'saves', 'zero_goals_matches',
    }
    float_fields = {
        'pis', 'shots_per_game', 'winfaceoff_p', 'saves_p', 'sf',
    }
    str_fields = {'icetime_per_game', 'gamingtime'}
    signed_int_fields = {'plus_minus'}

    if field in str_fields:
        return raw

    if field in int_fields:
        return _parse_int(raw)

    if field in signed_int_fields:
        try:
            return int(raw.replace('\xa0', '').strip())
        except (ValueError, AttributeError):
            return None

    if field in float_fields:
        return _parse_float(raw)

    return raw


class Command(BaseCommand):
    help = (
        'Parse player seasonal stats from khl.ru. '
        'Usage: ./manage.py fetch_khl_players [--start N] [--end N] '
        '[--dry-run] [--output FILE]'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--start', type=int, default=1,
            help='First player ID to fetch (default: 1)')
        parser.add_argument(
            '--end', type=int, default=25000,
            help='Last player ID to fetch (default: 25000)')
        parser.add_argument(
            '--dry-run', action='store_true', default=False,
            help='Parse without writing to DB')
        parser.add_argument(
            '--output', default=None, metavar='FILE',
            help='Write parsed data to JSONL file instead of DB')

    def handle(self, *args, **options):
        start_id = options['start']
        end_id = options['end']
        dry_run = options.get('dry_run', False)
        output_path = options.get('output')

        log_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(
                os.path.dirname(os.path.abspath(__file__))))),
            'logs',
        )
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        log_path = os.path.join(
            log_dir,
            'fetch_khl_players_{}.log'.format(
                datetime.datetime.now().strftime('%Y%m%d_%H%M%S')),
        )
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        logger = logging.getLogger('fetch_khl_players')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(file_handler)

        if dry_run:
            self._log(logger, '[INFO]', 'Dry-run mode — no DB writes')
        if output_path:
            self._log(logger, '[INFO]',
                      'Output mode — writing JSONL to {}'.format(output_path))

        bio_parser = KHLPlayerPageV2()
        stats_parser = KHLPlayerSeasonStatsV2()
        session = _make_session()

        consecutive_fails = 0
        out_file = open(output_path, 'a', encoding='utf-8') if output_path else None

        try:
            for player_id in range(start_id, end_id + 1):
                time.sleep(random.uniform(3.0, 7.0))

                # --- Fetch ---
                try:
                    resp, url = _fetch(session, player_id)
                except requests.exceptions.RequestException as exc:
                    msg = '{} | {} (попытка 3/3), пропущен'.format(player_id, exc)
                    self._log(logger, '[ERR]', msg)
                    continue

                if resp.status_code == 404:
                    consecutive_fails += 1
                    self._log(logger, '[404]',
                              '{} | не найден (подряд: {})'.format(
                                  player_id, consecutive_fails))
                    continue

                if resp.status_code != 200:
                    msg = '{} | HTTP {}, пропущен'.format(
                        player_id, resp.status_code)
                    self._log(logger, '[ERR]', msg)
                    continue

                consecutive_fails = 0

                # --- Parse HTML ---
                try:
                    tree = lxml_html.fromstring(resp.content)
                except Exception as exc:
                    self._log(logger, '[ERR]',
                              '{} | lxml parse error: {}'.format(player_id, exc))
                    continue

                bio = bio_parser.parse(tree)

                if not bio.get('ru_fio'):
                    self._log(logger, '[SKIP]',
                              '{} | страница пустая'.format(player_id))
                    continue

                is_goalie = KHLPlayerPageV2.is_goalie(bio)
                stat_rows = stats_parser.parse(tree, is_goalie=is_goalie)

                name = bio.get('ru_fio', '?')
                role_str = 'вратарь' if is_goalie else bio.get(
                    'position_text', 'полевой')

                if dry_run:
                    self._log(logger, '[DRY]',
                              '{} | {} | {} | {} сезонов | {}'.format(
                                  player_id, name, role_str,
                                  len(stat_rows), url))
                    continue

                if out_file:
                    # --- Write to JSONL file (no DB) ---
                    record = {
                        'player_khl_id': player_id,
                        'url': url,
                        'bio': bio,
                        'is_goalie': is_goalie,
                        'stats': stat_rows,
                    }
                    out_file.write(json.dumps(record, ensure_ascii=False) + '\n')
                    out_file.flush()
                    self._log(logger, '[OK]',
                              '{} | {} | {} | {} сезонов | {}'.format(
                                  player_id, name, role_str,
                                  len(stat_rows), url))
                else:
                    # --- Save to DB ---
                    tag, seasons_saved = self._save_player(
                        player_id, bio, is_goalie, stat_rows, url)
                    self._log(logger, tag,
                              '{} | {} | {} | {} сезонов | {}'.format(
                                  player_id, name, role_str,
                                  seasons_saved, url))

        finally:
            if out_file:
                out_file.close()

        self._log(logger, '[INFO]', 'Готово. Обработано ID {} — {}'.format(
            start_id, end_id))

    # ------------------------------------------------------------------

    def _save_player(self, player_id, bio, is_goalie, stat_rows, url):
        player, created = Player.objects.get_or_create(khl_id=player_id)
        tag = '[NEW]' if created else '[UPD]'

        # Update bio fields
        update_fields = []
        for src_key, model_field in (
            ('ru_fio', 'ru_fio'),
            ('en_fio', 'en_fio'),
            ('grip', 'grip'),
        ):
            val = bio.get(src_key, '').strip()
            if val and getattr(player, model_field, '') != val:
                setattr(player, model_field, val)
                update_fields.append(model_field)

        height = _parse_int(bio.get('height', ''))
        if height and player.height != height:
            player.height = height
            update_fields.append('height')

        weight = _parse_int(bio.get('weight', ''))
        if weight and player.weight != weight:
            player.weight = weight
            update_fields.append('weight')

        birth_date = _parse_birth_date(bio.get('birth_date', ''))
        if birth_date and player.birth_date != birth_date:
            player.birth_date = birth_date
            update_fields.append('birth_date')

        pos_line = _map_position(bio.get('position_text', ''))
        if pos_line and player.line != pos_line:
            player.line = pos_line
            update_fields.append('line')

        if url and player.url != url:
            player.url = url
            update_fields.append('url')

        country = _country_from_name(bio.get('citizenship_name', ''))
        if country and player.citizenship_id != country.pk:
            player.citizenship = country
            update_fields.append('citizenship')

        contract_to_str = bio.get('contract_to', '').strip()
        if contract_to_str:
            contract_to = _parse_birth_date(contract_to_str)
            if contract_to and player.contract_to != contract_to:
                player.contract_to = contract_to
                update_fields.append('contract_to')

        if update_fields:
            player.save(update_fields=update_fields)

        # Year cutoff for pre-existing players
        cutoff_year = 2014 if not created else None

        seasons_saved = 0
        for row in stat_rows:
            season = _season_from_str(row.get('season_str', ''))
            if not season:
                continue

            if cutoff_year and season.start_date and \
                    season.start_date.year < cutoff_year:
                continue

            club = _club_from_name(row.get('club_name', ''))
            tournament_type = _map_tournament(row.get('tournament_str', ''))

            stat_defaults = {'is_goalie': is_goalie}
            for field in (
                'number', 'matches', 'goals', 'assists', 'points',
                'plus_minus', 'plus', 'minus', 'penalty_time',
                'es_goals', 'pp_goals', 'sh_goals', 'overtime_goals',
                'win_goals', 'bullet_goals', 'shots', 'pis',
                'shots_per_game', 'faceoff', 'winfaceoff', 'winfaceoff_p',
                'icetime_per_game', 'hits', 'blocks', 'fouls',
                'takeaways', 'interceptions',
                'wins', 'losses', 'bullet_matches', 'shots_received',
                'loose_goals', 'saves', 'saves_p', 'sf',
                'zero_goals_matches', 'gamingtime',
            ):
                raw = row.get(field)
                if raw is not None:
                    stat_defaults[field] = _coerce_stat(field, raw)

            PlayerSeasonStat.objects.update_or_create(
                player=player,
                club=club,
                season=season,
                tournament_type=tournament_type,
                defaults=stat_defaults,
            )
            seasons_saved += 1

        return tag, seasons_saved

    @staticmethod
    def _log(logger, tag, message):
        line = '{:<7} {}'.format(tag, message)
        print(line)
        logger.info(line)
