#!/usr/bin/env python3
"""
Парсер календаря матчей КХЛ.
Читает список URL из файла (по умолчанию games.txt) и сохраняет матчи в SQLite.

Использование:
    python3 parse_khl_calendar.py
    python3 parse_khl_calendar.py --games games.txt --db khl_calendar.sqlite3
    python3 parse_khl_calendar.py --games games.txt --json matches.json
"""

import argparse
import json
import logging
import re
import sqlite3
import sys

import requests
from lxml import html


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(message)s',
    datefmt='%H:%M:%S',
)
log = logging.getLogger(__name__)

KHL_BASE_URL = 'https://www.khl.ru'
_EN_DASH = '–'
_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru,en;q=0.5',
}

DEFAULT_GAMES_FILE = 'games.txt'
DEFAULT_DB = 'khl_calendar.sqlite3'

# ---------------------------------------------------------------------------
# Чтение файла со ссылками
# ---------------------------------------------------------------------------

def parse_games_file(path):
    """Читает файл вида:
        REG25/26 https://www.khl.ru/calendar/1369/00/
        PO 24/25 https://www.khl.ru/calendar/1289/00/
    URL всегда последний токен в строке (начинается с http).
    Всё перед URL — метка (label).
    Возвращает список словарей с ключами: label, url, is_playoff, season.
    """
    entries = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens = line.split()
            # URL — последний токен
            url = tokens[-1]
            if not url.startswith('http'):
                continue
            label = ' '.join(tokens[:-1]).strip()
            if not label:
                continue
            is_playoff = label.upper().startswith('PO')
            season_match = re.search(r'\d{2}/\d{2}', label)
            season = season_match.group() if season_match else ''
            # season_khl_id из URL: https://www.khl.ru/calendar/1369/00/ → 1369
            season_khl_id_match = re.search(r'/calendar/(\d+)/', url)
            season_khl_id = int(season_khl_id_match.group(1)) if season_khl_id_match else None
            entries.append({
                'label': label,
                'url': url,
                'is_playoff': is_playoff,
                'season': season,
                'season_khl_id': season_khl_id,
            })
    return entries


# ---------------------------------------------------------------------------
# Парсер
# ---------------------------------------------------------------------------

class KHLCalendarParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(_HEADERS)

    def parse_url(self, url, is_playoff=False, season='', label='', season_khl_id=None):
        tree = self._fetch(url)
        if tree is None:
            return []
        return self._parse_matches(
            tree, is_playoff=is_playoff, season=season,
            label=label, season_khl_id=season_khl_id,
        )

    def _fetch(self, url):
        try:
            resp = self.session.get(url, allow_redirects=True, timeout=30)
        except requests.RequestException as e:
            log.error('Ошибка запроса %s: %s', url, e)
            return None
        if resp.status_code != 200:
            log.error('HTTP %d для %s', resp.status_code, url)
            return None
        return html.fromstring(resp.content)

    def _parse_matches(self, tree, is_playoff=False, season='', label='', season_khl_id=None):
        matches = []
        day_blocks = tree.xpath('//div[contains(@class, "calendary-body__item")]')
        for block in day_blocks:
            date = self._get_date(block)
            is_past = 'games_past' in block.get('class', '')
            for game_div in block.xpath('.//div[@class="card-game "]'):
                match = self._parse_game(
                    game_div, date, is_past,
                    is_playoff=is_playoff, season=season,
                    label=label, season_khl_id=season_khl_id,
                )
                if match:
                    matches.append(match)
        return matches

    def _get_date(self, block):
        els = block.xpath('.//time[contains(@class, "calendary-body__wrap-time")]/text()')
        return els[0].strip() if els else ''

    def _parse_game(self, game_div, date, is_past, is_playoff=False, season='', label='', season_khl_id=None):
        home_el = game_div.xpath('.//a[contains(@class, "card-game__club_left")]')
        guest_el = game_div.xpath('.//a[contains(@class, "card-game__club_right")]')
        if not home_el or not guest_el:
            return None

        protocol_href = game_div.xpath('.//a[contains(@href, "/protocol/")]/@href')
        resume_href = game_div.xpath('.//a[contains(@href, "/resume/")]/@href')
        khl_id = self._extract_game_id(protocol_href[0]) if protocol_href else None

        game_number_els = game_div.xpath(
            './/p[contains(@class, "card-game__center-number")]/text()'
        )
        game_number = game_number_els[0].strip() if game_number_els else ''

        result = {
            'date': date,
            'khl_id': khl_id,
            'season_khl_id': season_khl_id,
            'game_number': game_number,
            'home_team': self._get_team_name(home_el[0]),
            'home_team_slug': self._get_team_slug(home_el[0]),
            'guest_team': self._get_team_name(guest_el[0]),
            'guest_team_slug': self._get_team_slug(guest_el[0]),
            'is_finished': is_past,
            'is_playoff': is_playoff,
            'season': season,
            'season_label': label,
            'match_url': KHL_BASE_URL + resume_href[0] if resume_href else None,
            'protocol_url': KHL_BASE_URL + protocol_href[0] if protocol_href else None,
        }

        if is_past:
            result.update(self._parse_score(game_div))

        return result

    def _parse_score(self, game_div):
        sl_els = game_div.xpath('.//span[contains(@class, "score-left")]/text()')
        sr_els = game_div.xpath('.//span[contains(@class, "score-right")]')
        if not sl_els or not sr_els:
            return {}

        home_raw = sl_els[0].strip()
        guest_raw = sr_els[0].text_content().strip()

        overtime = 'ОТ' in guest_raw or 'OT' in guest_raw
        shootout = 'Б' in guest_raw
        guest_digits = re.sub(r'[^\d]', '', guest_raw)

        period_texts = game_div.xpath(
            './/p[contains(@class, "card-game__center-value")]/text()'
        )
        period_scores = [
            p.strip() for p in period_texts
            if p.strip() and p.strip() != _EN_DASH
        ]

        return {
            'home_score': int(home_raw) if home_raw.isdigit() else None,
            'guest_score': int(guest_digits) if guest_digits.isdigit() else None,
            'overtime': overtime,
            'shootout': shootout,
            'period_scores': period_scores,
        }

    @staticmethod
    def _extract_game_id(href):
        parts = href.strip('/').split('/')
        try:
            return int(parts[-2])
        except (IndexError, ValueError):
            return None

    @staticmethod
    def _get_team_name(club_el):
        els = club_el.xpath('.//p[contains(@class, "card-game__club-name")]/text()')
        return els[0].strip() if els else ''

    @staticmethod
    def _get_team_slug(club_el):
        href = club_el.get('href', '')
        return href.strip('/').split('/')[-1]


# ---------------------------------------------------------------------------
# SQLite
# ---------------------------------------------------------------------------

CREATE_TABLE = """
CREATE TABLE IF NOT EXISTS matches (
    khl_id          INTEGER PRIMARY KEY,
    season_khl_id   INTEGER,
    season_label    TEXT,
    season          TEXT,
    is_playoff      INTEGER,
    date            TEXT,
    game_number     TEXT,
    home_team       TEXT,
    home_team_slug  TEXT,
    guest_team      TEXT,
    guest_team_slug TEXT,
    home_score      INTEGER,
    guest_score     INTEGER,
    overtime        INTEGER,
    shootout        INTEGER,
    period_scores   TEXT,
    is_finished     INTEGER,
    match_url       TEXT,
    protocol_url    TEXT
)
"""

UPSERT = """
INSERT OR REPLACE INTO matches
    (khl_id, season_khl_id, season_label, season, is_playoff, date, game_number,
     home_team, home_team_slug, guest_team, guest_team_slug,
     home_score, guest_score, overtime, shootout, period_scores,
     is_finished, match_url, protocol_url)
VALUES
    (:khl_id, :season_khl_id, :season_label, :season, :is_playoff, :date, :game_number,
     :home_team, :home_team_slug, :guest_team, :guest_team_slug,
     :home_score, :guest_score, :overtime, :shootout, :period_scores,
     :is_finished, :match_url, :protocol_url)
"""


def save_to_sqlite(matches, db_path):
    con = sqlite3.connect(db_path)
    con.execute(CREATE_TABLE)
    rows = []
    for m in matches:
        rows.append({
            'khl_id': m.get('khl_id'),
            'season_khl_id': m.get('season_khl_id'),
            'season_label': m.get('season_label', ''),
            'season': m.get('season', ''),
            'is_playoff': int(m.get('is_playoff', False)),
            'date': m.get('date', ''),
            'game_number': m.get('game_number', ''),
            'home_team': m.get('home_team', ''),
            'home_team_slug': m.get('home_team_slug', ''),
            'guest_team': m.get('guest_team', ''),
            'guest_team_slug': m.get('guest_team_slug', ''),
            'home_score': m.get('home_score'),
            'guest_score': m.get('guest_score'),
            'overtime': int(m.get('overtime', False)),
            'shootout': int(m.get('shootout', False)),
            'period_scores': ','.join(m.get('period_scores', [])),
            'is_finished': int(m.get('is_finished', False)),
            'match_url': m.get('match_url'),
            'protocol_url': m.get('protocol_url'),
        })
    con.executemany(UPSERT, rows)
    con.commit()
    con.close()
    return len(rows)


# ---------------------------------------------------------------------------
# Точка входа
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description='Парсер календаря КХЛ')
    ap.add_argument('--games', default=DEFAULT_GAMES_FILE,
                    help=f'Файл со ссылками (по умолчанию: {DEFAULT_GAMES_FILE})')
    ap.add_argument('--db', default=DEFAULT_DB,
                    help=f'SQLite-файл результата (по умолчанию: {DEFAULT_DB})')
    ap.add_argument('--json', default=None, metavar='FILE',
                    help='Дополнительно сохранить в JSON')
    args = ap.parse_args()

    try:
        entries = parse_games_file(args.games)
    except FileNotFoundError:
        log.error('Файл не найден: %s', args.games)
        sys.exit(1)

    if not entries:
        log.error('В файле %s нет записей', args.games)
        sys.exit(1)

    log.info('Загружено %d URL из %s', len(entries), args.games)
    for e in entries:
        kind = 'Плей-офф' if e['is_playoff'] else 'Регулярный чемпионат'
        log.info('  %-12s  %-25s  %s', e['label'], kind, e['url'])

    parser = KHLCalendarParser()
    all_matches = []

    for entry in entries:
        log.info('Парсим %s ...', entry['label'])
        matches = parser.parse_url(
            entry['url'],
            is_playoff=entry['is_playoff'],
            season=entry['season'],
            label=entry['label'],
            season_khl_id=entry.get('season_khl_id'),
        )
        log.info('  → %d матчей', len(matches))
        all_matches.extend(matches)

    if not all_matches:
        log.warning('Матчей не найдено')
        sys.exit(0)

    finished = sum(1 for m in all_matches if m.get('is_finished'))
    playoff  = sum(1 for m in all_matches if m.get('is_playoff'))
    log.info('Итого: %d матчей  (сыграно: %d, плей-офф: %d)', len(all_matches), finished, playoff)

    saved = save_to_sqlite(all_matches, args.db)
    log.info('Сохранено в %s: %d записей', args.db, saved)

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as f:
            json.dump(all_matches, f, ensure_ascii=False, indent=2)
        log.info('JSON сохранён: %s', args.json)


if __name__ == '__main__':
    main()
