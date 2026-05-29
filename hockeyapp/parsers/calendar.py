# coding: utf-8
from __future__ import unicode_literals

import re

import requests
from lxml import html


KHL_BASE_URL = 'https://www.khl.ru'

_HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'ru,en;q=0.5',
}

_EN_DASH = '–'


def parse_games_file(path):
    """Читает файл вида:
        REG25/26 https://www.khl.ru/calendar/1369/00/
        PO25/26  https://www.khl.ru/calendar/1370/00/

    Возвращает список словарей:
        [{'label': 'REG25/26', 'url': '...', 'is_playoff': False, 'season': '25/26'}, ...]
    """
    entries = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split(None, 1)
            if len(parts) != 2:
                continue
            label, url = parts[0], parts[1].strip()
            # REG25/26 → тип REG, сезон 25/26
            # PO 24/25 → тип PO, сезон 24/25  (с пробелом тоже разобрали split)
            is_playoff = label.upper().startswith('PO')
            season = re.search(r'\d{2}/\d{2}', label)
            season = season.group() if season else ''
            entries.append({
                'label': label,
                'url': url,
                'is_playoff': is_playoff,
                'season': season,
            })
    return entries


class KHLCalendarParser:
    """Парсер календаря матчей КХЛ с сайта khl.ru.

    Пример — парсинг по файлу со ссылками:
        parser = KHLCalendarParser()
        all_matches = parser.parse_from_file('games.txt')

    Пример — парсинг одного URL:
        matches = parser.parse_url('https://www.khl.ru/calendar/1369/00/')
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(_HEADERS)

    def parse_from_file(self, path):
        """Читает games.txt и возвращает все матчи со всех URL в файле."""
        entries = parse_games_file(path)
        all_matches = []
        for entry in entries:
            matches = self.parse_url(
                entry['url'],
                is_playoff=entry['is_playoff'],
                season=entry['season'],
                label=entry['label'],
            )
            all_matches.extend(matches)
        return all_matches

    def parse_url(self, url, is_playoff=False, season='', label=''):
        """Парсит один URL календаря и возвращает список матчей."""
        tree = self._fetch(url)
        if tree is None:
            return []
        return self._parse_matches(tree, is_playoff=is_playoff, season=season, label=label)

    def _fetch(self, url):
        try:
            resp = self.session.get(url, allow_redirects=True, timeout=30)
        except requests.RequestException:
            return None
        if resp.status_code != 200:
            return None
        return html.fromstring(resp.content)

    def _parse_matches(self, tree, is_playoff=False, season='', label=''):
        matches = []
        day_blocks = tree.xpath('//div[contains(@class, "calendary-body__item")]')
        for block in day_blocks:
            date = self._get_date(block)
            is_past = 'games_past' in block.get('class', '')
            for game_div in block.xpath('.//div[@class="card-game "]'):
                match = self._parse_game(
                    game_div, date, is_past,
                    is_playoff=is_playoff, season=season, label=label,
                )
                if match:
                    matches.append(match)
        return matches

    def _get_date(self, block):
        els = block.xpath('.//time[contains(@class, "calendary-body__wrap-time")]/text()')
        return els[0].strip() if els else ''

    def _parse_game(self, game_div, date, is_past, is_playoff=False, season='', label=''):
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

        home_score_raw = sl_els[0].strip()
        guest_score_raw = sr_els[0].text_content().strip()

        overtime = 'ОТ' in guest_score_raw or 'OT' in guest_score_raw
        shootout = 'Б' in guest_score_raw
        guest_score_digits = re.sub(r'[^\d]', '', guest_score_raw)

        period_texts = game_div.xpath(
            './/p[contains(@class, "card-game__center-value")]/text()'
        )
        period_scores = [
            p.strip() for p in period_texts
            if p.strip() and p.strip() != _EN_DASH
        ]

        return {
            'home_score': int(home_score_raw) if home_score_raw.isdigit() else None,
            'guest_score': int(guest_score_digits) if guest_score_digits.isdigit() else None,
            'overtime': overtime,
            'shootout': shootout,
            'period_scores': period_scores,
        }

    @staticmethod
    def _extract_game_id(href):
        # /game/1369/897597/protocol/ → 897597
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
