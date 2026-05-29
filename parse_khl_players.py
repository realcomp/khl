#!/usr/bin/env python3
"""
Автономный парсер карточек игроков khl.ru.
Результат пишется в SQLite-файл (по умолчанию players_parsed.sqlite3).

Использование:
    python3 parse_khl_players.py
    python3 parse_khl_players.py --start 490 --end 500
    python3 parse_khl_players.py --start 1000 --db my.sqlite3
"""

import argparse
import datetime
import logging
import os
import random
import re
import sqlite3
import sys
import time

import requests
from lxml import html as lxml_html


# ---------------------------------------------------------------------------
# Константы
# ---------------------------------------------------------------------------

BASE_URL = "https://www.khl.ru/players/{}/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

SKATER_COLS = {
    "№": "number",
    "И": "matches",
    "Ш": "goals",
    "А": "assists",
    "О": "points",
    "+/-": "plus_minus",
    "+": "plus",
    "-": "minus",
    "Штр": "penalty_time",
    "ШР": "es_goals",
    "ШБ": "pp_goals",
    "ШМ": "sh_goals",
    "ШО": "overtime_goals",
    "ШП": "win_goals",
    "РБ": "bullet_goals",
    "БВ": "shots",
    "%БВ": "pis",
    "БВ/И": "shots_per_game",
    "Вбр": "faceoff",
    "ВВбр": "winfaceoff",
    "%Вбр": "winfaceoff_p",
    "ВП/И": "icetime_per_game",
    "СПр": "hits",
    "БлБ": "blocks",
    "ФоП": "fouls",
    "ОТБ": "takeaways",
    "ПХТ": "interceptions",
}

GOALIE_COLS = {
    "И": "matches",
    "В": "wins",
    "П": "losses",
    "ИБ": "bullet_matches",
    "Бр": "shots_received",
    "ПШ": "loose_goals",
    "ОБ": "saves",
    "%ОБ": "saves_p",
    "КН": "sf",
    "Ш": "goals",
    "А": "assists",
    'И"0"': "zero_goals_matches",
    "Штр": "penalty_time",
    "ВП": "gamingtime",
}

TOURNAMENT_MAP = {
    "рег": "regular",
    "regular": "regular",
    "плей": "playoff",
    "playoff": "playoff",
}

POSITION_MAP = {
    "вратарь": "goalie",
    "goalkeeper": "goalie",
    "защитник": "defender",
    "defender": "defender",
    "нападающий": "forward",
    "forward": "forward",
    "offender": "forward",
}

# Все числовые поля статистики
STAT_FIELDS = [
    "number", "matches", "goals", "assists", "points",
    "plus_minus", "plus", "minus", "penalty_time",
    "es_goals", "pp_goals", "sh_goals", "overtime_goals",
    "win_goals", "bullet_goals", "shots", "pis", "shots_per_game",
    "faceoff", "winfaceoff", "winfaceoff_p", "icetime_per_game",
    "hits", "blocks", "fouls", "takeaways", "interceptions",
    "wins", "losses", "bullet_matches", "shots_received", "loose_goals",
    "saves", "saves_p", "sf", "zero_goals_matches", "gamingtime",
]


# ---------------------------------------------------------------------------
# БД
# ---------------------------------------------------------------------------

SCHEMA = """
CREATE TABLE IF NOT EXISTS player (
    khl_id      INTEGER PRIMARY KEY,
    ru_fio      TEXT,
    en_fio      TEXT,
    birth_date  TEXT,
    citizenship TEXT,
    height      INTEGER,
    weight      INTEGER,
    grip        TEXT,
    contract_to TEXT,
    position    TEXT,
    is_goalie   INTEGER DEFAULT 0,
    url         TEXT,
    parsed_at   TEXT
);

CREATE TABLE IF NOT EXISTS player_stat (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    player_khl_id   INTEGER NOT NULL REFERENCES player(khl_id),
    club_name       TEXT,
    season_str      TEXT,
    tournament_type TEXT,
    is_goalie       INTEGER DEFAULT 0,
    number          TEXT,
    matches         INTEGER,
    goals           INTEGER,
    assists         INTEGER,
    points          INTEGER,
    plus_minus      INTEGER,
    plus            INTEGER,
    minus           INTEGER,
    penalty_time    INTEGER,
    es_goals        INTEGER,
    pp_goals        INTEGER,
    sh_goals        INTEGER,
    overtime_goals  INTEGER,
    win_goals       INTEGER,
    bullet_goals    INTEGER,
    shots           INTEGER,
    pis             REAL,
    shots_per_game  REAL,
    faceoff         INTEGER,
    winfaceoff      INTEGER,
    winfaceoff_p    REAL,
    icetime_per_game TEXT,
    hits            INTEGER,
    blocks          INTEGER,
    fouls           INTEGER,
    takeaways       INTEGER,
    interceptions   INTEGER,
    wins            INTEGER,
    losses          INTEGER,
    bullet_matches  INTEGER,
    shots_received  INTEGER,
    loose_goals     INTEGER,
    saves           INTEGER,
    saves_p         REAL,
    sf              REAL,
    zero_goals_matches INTEGER,
    gamingtime      TEXT,
    UNIQUE(player_khl_id, club_name, season_str, tournament_type)
);
"""


def open_db(path):
    con = sqlite3.connect(path)
    con.executescript(SCHEMA)
    con.commit()
    return con


def already_parsed(con, player_id):
    row = con.execute(
        "SELECT khl_id FROM player WHERE khl_id = ?", (player_id,)
    ).fetchone()
    return row is not None


def save_player(con, player_id, bio, is_goalie, stat_rows, url):
    now = datetime.datetime.now().isoformat(timespec="seconds")
    con.execute(
        """
        INSERT INTO player
            (khl_id, ru_fio, en_fio, birth_date, citizenship,
             height, weight, grip, contract_to, position, is_goalie, url, parsed_at)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(khl_id) DO UPDATE SET
            ru_fio=excluded.ru_fio, en_fio=excluded.en_fio,
            birth_date=excluded.birth_date, citizenship=excluded.citizenship,
            height=excluded.height, weight=excluded.weight,
            grip=excluded.grip, contract_to=excluded.contract_to,
            position=excluded.position, is_goalie=excluded.is_goalie,
            url=excluded.url, parsed_at=excluded.parsed_at
        """,
        (
            player_id,
            bio.get("ru_fio", ""),
            bio.get("en_fio", ""),
            bio.get("birth_date", ""),
            bio.get("citizenship_name", ""),
            _to_int(bio.get("height")),
            _to_int(bio.get("weight")),
            bio.get("grip", ""),
            bio.get("contract_to", ""),
            bio.get("position_text", ""),
            1 if is_goalie else 0,
            url,
            now,
        ),
    )
    for row in stat_rows:
        values = [
            player_id,
            row.get("club_name", ""),
            row.get("season_str", ""),
            _map_tournament(row.get("tournament_str", "")),
            1 if is_goalie else 0,
        ]
        for field in STAT_FIELDS:
            values.append(row.get(field))
        con.execute(
            f"""
            INSERT INTO player_stat
                (player_khl_id, club_name, season_str, tournament_type, is_goalie,
                 {', '.join(STAT_FIELDS)})
            VALUES ({', '.join(['?'] * (5 + len(STAT_FIELDS)))})
            ON CONFLICT(player_khl_id, club_name, season_str, tournament_type)
            DO UPDATE SET {', '.join(f'{f}=excluded.{f}' for f in STAT_FIELDS)},
                          is_goalie=excluded.is_goalie
            """,
            values,
        )
    con.commit()


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def make_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def fetch(session, player_id, retries=3):
    url = BASE_URL.format(player_id)
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


# ---------------------------------------------------------------------------
# Парсинг
# ---------------------------------------------------------------------------

def _cell(el):
    return (el.text_content() or "").strip()


def _to_int(s):
    if s is None:
        return None
    try:
        return int(str(s).replace("\xa0", "").strip())
    except ValueError:
        return None


def _to_float(s):
    if s is None:
        return None
    try:
        return float(str(s).replace(",", ".").replace("\xa0", "").strip())
    except ValueError:
        return None


def _map_tournament(text):
    t = text.lower()
    for key, val in TOURNAMENT_MAP.items():
        if key in t:
            return val
    return "other"


def _map_position(text):
    t = text.lower()
    for key, val in POSITION_MAP.items():
        if key in t:
            return val
    return ""


BIO_LABELS = {
    "дата рождения": "birth_date",
    "родился": "birth_date",
    "гражданство": "citizenship_name",
    "рост": "height",
    "вес": "weight",
    "хват": "grip",
    "контракт до": "contract_to",
    "амплуа": "position_text",
}


def parse_bio(tree):
    result = {}

    # Имена
    names = tree.xpath(
        '//*[contains(@class,"frameCard-header__detail-titleItem")]'
    )
    if names:
        result["ru_fio"] = _cell(names[0])
    if len(names) > 1:
        result["en_fio"] = _cell(names[1])

    # Детали: ищем любые элементы с текстом "Метка: Значение"
    body_els = tree.xpath(
        '//*[contains(@class,"frameCard-header__detail-body")]'
        '//*[contains(@class,"playerCard-item") or '
        'contains(@class,"frameCard-header__detail-item")]'
    )
    if not body_els:
        # Запасной вариант: весь bio-блок
        body_els = tree.xpath(
            '//*[contains(@class,"frameCard-header__detail-body")]//li |'
            '//*[contains(@class,"frameCard-header__detail-body")]//div[@class]'
        )

    for el in body_els:
        text = _cell(el)
        if not text:
            continue
        # Паттерн "Метка: Значение"
        if ":" in text:
            label, _, value = text.partition(":")
            key = label.strip().lower()
            field = BIO_LABELS.get(key)
            if field and value.strip():
                result[field] = value.strip()
        else:
            # Паттерн с отдельными дочерними элементами для метки и значения
            children = el.xpath("./*")
            if len(children) >= 2:
                key = _cell(children[0]).rstrip(":").strip().lower()
                field = BIO_LABELS.get(key)
                if field:
                    result[field] = _cell(children[-1])

    return result


def is_goalie(bio):
    pos = bio.get("position_text", "").lower()
    return "вратарь" in pos or "goalie" in pos or "goalkeeper" in pos


def parse_stats(tree, goalie=False):
    col_map = GOALIE_COLS if goalie else SKATER_COLS

    # Первый div.statTable-tabContent.fade — сезонная статистика
    divs = tree.xpath(
        '//div[contains(@class,"statTable-tabContent") and contains(@class,"fade")]'
    )
    if not divs:
        divs = tree.xpath('//div[contains(@class,"statTable-tabContent")]')
    if not divs:
        return []

    table = divs[0]

    # Маппинг индекс колонки → поле
    headers = table.xpath(".//thead//th | .//thead//td")
    field_map = {}
    for i, th in enumerate(headers):
        label = _cell(th)
        if label in col_map:
            field_map[i] = col_map[label]

    rows = table.xpath(".//tbody//tr")
    results = []
    cur_season = None
    cur_tournament = None

    for row in rows:
        cells = row.xpath("./td | ./th")
        if not cells:
            continue

        first = _cell(cells[0])

        # Заголовок сезона: colspan, или одна ячейка, или ≤2 ячеек с "/"
        is_header = (
            cells[0].get("colspan")
            or len(cells) == 1
            or (len(cells) <= 2 and "/" in first)
        )

        if is_header:
            # "25/26 | рег.чемпионат"
            parts = re.split(r"\s*\|\s*|\s{2,}", first, maxsplit=1)
            if len(parts) >= 2:
                cur_season = parts[0].strip()
                cur_tournament = parts[1].strip()
            elif "/" in first:
                cur_season = first.strip()
                cur_tournament = ""
            continue

        if not cur_season:
            continue

        club_name = first
        if not club_name:
            continue

        stat = {
            "club_name": club_name,
            "season_str": cur_season,
            "tournament_str": cur_tournament or "",
        }
        for i, cell in enumerate(cells):
            field = field_map.get(i)
            if field:
                stat[field] = _cell(cell)

        results.append(stat)

    return results


# ---------------------------------------------------------------------------
# Логирование
# ---------------------------------------------------------------------------

def setup_logger(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"fetch_khl_players_{ts}.log")

    logger = logging.getLogger("khl_parser")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


def log(logger, tag, message):
    logger.info(f"{tag:<7} {message}")


# ---------------------------------------------------------------------------
# Основной цикл
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Парсер игроков khl.ru → SQLite"
    )
    parser.add_argument("--start", type=int, default=1,
                        help="Первый ID (по умолчанию 1)")
    parser.add_argument("--end", type=int, default=50000,
                        help="Последний ID (по умолчанию 50000)")
    parser.add_argument("--db", default="players_parsed.sqlite3",
                        help="Путь к SQLite-файлу результатов")
    parser.add_argument("--logs", default="logs",
                        help="Папка для лог-файлов")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Пропускать уже разобранные ID (по умолчанию вкл.)")
    parser.add_argument("--no-resume", dest="resume", action="store_false",
                        help="Перепарсить все ID заново")
    args = parser.parse_args()

    logger = setup_logger(args.logs)
    con = open_db(args.db)
    session = make_session()

    consecutive_fails = 0
    log(logger, "[INFO]", f"Старт: ID {args.start}–{args.end}  БД: {args.db}")

    for player_id in range(args.start, args.end + 1):

        if args.resume and already_parsed(con, player_id):
            log(logger, "[SKIP]", f"{player_id} | уже в БД")
            continue

        time.sleep(random.uniform(2.0, 3.0))

        # Запрос
        try:
            resp, url = fetch(session, player_id)
        except requests.exceptions.RequestException as exc:
            log(logger, "[ERR]",
                f"{player_id} | {exc} (попытка 3/3), пропущен")
            continue

        if resp.status_code == 404:
            consecutive_fails += 1
            log(logger, "[404]",
                f"{player_id} | не найден (подряд: {consecutive_fails})")
            continue

        if resp.status_code != 200:
            log(logger, "[ERR]",
                f"{player_id} | HTTP {resp.status_code}, пропущен")
            continue

        consecutive_fails = 0

        # Парсинг
        try:
            tree = lxml_html.fromstring(resp.content)
        except Exception as exc:
            log(logger, "[ERR]", f"{player_id} | lxml: {exc}")
            continue

        bio = parse_bio(tree)

        if not bio.get("ru_fio"):
            log(logger, "[SKIP]", f"{player_id} | страница пустая")
            continue

        goalie = is_goalie(bio)
        stat_rows = parse_stats(tree, goalie=goalie)

        # Сохранение
        try:
            save_player(con, player_id, bio, goalie, stat_rows, url)
        except Exception as exc:
            log(logger, "[ERR]", f"{player_id} | DB error: {exc}")
            continue

        role = "вратарь" if goalie else bio.get("position_text", "полевой")
        log(logger, "[OK]",
            f"{player_id} | {bio.get('ru_fio','?')} | {role} "
            f"| {len(stat_rows)} сезонов | {url}")

    con.close()
    log(logger, "[INFO]", f"Готово. Обработано ID {args.start}–{args.end}")


if __name__ == "__main__":
    main()
