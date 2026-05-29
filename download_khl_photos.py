#!/usr/bin/env python3
"""
Скачивает фотографии игроков с img.khl.ru и сохраняет в media/players/khl/.
Результат (путь / статус) пишется в players_parsed.sqlite3.

Использование:
    python3 download_khl_photos.py
    python3 download_khl_photos.py --db players_parsed.sqlite3 --out media/players/khl
    python3 download_khl_photos.py --retry-errors   # перескачать ранее упавшие
    python3 download_khl_photos.py --dry-run        # только вывод, без скачивания
"""

import argparse
import logging
import os
import random
import sqlite3
import sys
import time

import requests

PHOTO_URL = "https://img.khl.ru/players/{}/160.jpg"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Referer": "https://www.khl.ru/",
    "Accept": "image/avif,image/webp,image/apng,*/*;q=0.8",
}

STATUS_OK = "ok"
STATUS_NO_PHOTO = "no_photo"
STATUS_ERROR = "error"


# ---------------------------------------------------------------------------
# БД
# ---------------------------------------------------------------------------

def open_db(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    _migrate(con)
    return con


def _migrate(con):
    cols = {row[1] for row in con.execute("PRAGMA table_info(player)")}
    if "photo_local_path" not in cols:
        con.execute("ALTER TABLE player ADD COLUMN photo_local_path TEXT")
    if "photo_status" not in cols:
        con.execute("ALTER TABLE player ADD COLUMN photo_status TEXT")
    con.commit()


def get_pending(con, retry_errors=False):
    if retry_errors:
        rows = con.execute(
            "SELECT khl_id FROM player WHERE photo_status IS NULL OR photo_status = ?",
            (STATUS_ERROR,),
        ).fetchall()
    else:
        rows = con.execute(
            "SELECT khl_id FROM player WHERE photo_status IS NULL"
        ).fetchall()
    return [r["khl_id"] for r in rows]


def save_ok(con, khl_id, rel_path):
    con.execute(
        "UPDATE player SET photo_local_path = ?, photo_status = ? WHERE khl_id = ?",
        (rel_path, STATUS_OK, khl_id),
    )
    con.commit()


def save_status(con, khl_id, status):
    con.execute(
        "UPDATE player SET photo_status = ?, photo_local_path = NULL WHERE khl_id = ?",
        (status, khl_id),
    )
    con.commit()


# ---------------------------------------------------------------------------
# HTTP
# ---------------------------------------------------------------------------

def make_session():
    s = requests.Session()
    s.headers.update(HEADERS)
    return s


def download_photo(session, khl_id, retries=3):
    url = PHOTO_URL.format(khl_id)
    last_exc = None
    for attempt in range(retries):
        try:
            resp = session.get(url, timeout=15)
            return resp
        except requests.exceptions.RequestException as exc:
            last_exc = exc
            if attempt < retries - 1:
                time.sleep(2 ** (attempt + 1))
    raise last_exc


# ---------------------------------------------------------------------------
# Логирование
# ---------------------------------------------------------------------------

def setup_logger(log_dir):
    os.makedirs(log_dir, exist_ok=True)
    ts = time.strftime("%Y%m%d_%H%M%S")
    log_path = os.path.join(log_dir, f"download_khl_photos_{ts}.log")

    logger = logging.getLogger("khl_photos")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    sh = logging.StreamHandler(sys.stdout)
    sh.setFormatter(fmt)
    logger.addHandler(sh)

    return logger


def log(logger, tag, msg):
    logger.info(f"{tag:<10} {msg}")


# ---------------------------------------------------------------------------
# Основной цикл
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Скачивает фото игроков khl.ru")
    parser.add_argument("--db", default="players_parsed.sqlite3",
                        help="SQLite с игроками (default: players_parsed.sqlite3)")
    parser.add_argument("--out", default="media/players/khl",
                        help="Папка для фото (default: media/players/khl)")
    parser.add_argument("--logs", default="logs",
                        help="Папка для логов (default: logs)")
    parser.add_argument("--retry-errors", action="store_true",
                        help="Повторить записи со статусом 'error'")
    parser.add_argument("--dry-run", action="store_true",
                        help="Только вывод, без скачивания и записи в БД")
    parser.add_argument("--delay-min", type=float, default=1.0,
                        help="Мин. задержка между запросами, сек (default: 1.0)")
    parser.add_argument("--delay-max", type=float, default=2.5,
                        help="Макс. задержка между запросами, сек (default: 2.5)")
    args = parser.parse_args()

    logger = setup_logger(args.logs)
    con = open_db(args.db)
    session = make_session()

    os.makedirs(args.out, exist_ok=True)

    pending = get_pending(con, retry_errors=args.retry_errors)
    total = len(pending)
    log(logger, "[INFO]", f"Игроков для обработки: {total}")

    ok = no_photo = errors = 0

    for i, khl_id in enumerate(pending, 1):
        prefix = f"[{i}/{total}]"

        if args.dry_run:
            log(logger, "[DRY]", f"{prefix} {khl_id} → {PHOTO_URL.format(khl_id)}")
            continue

        time.sleep(random.uniform(args.delay_min, args.delay_max))

        try:
            resp = download_photo(session, khl_id)
        except requests.exceptions.RequestException as exc:
            log(logger, "[ERR]", f"{prefix} {khl_id} | сетевая ошибка: {exc}")
            save_status(con, khl_id, STATUS_ERROR)
            errors += 1
            continue

        if resp.status_code == 404:
            log(logger, "[404]", f"{prefix} {khl_id} | нет фото")
            save_status(con, khl_id, STATUS_NO_PHOTO)
            no_photo += 1
            continue

        if resp.status_code != 200:
            log(logger, "[ERR]", f"{prefix} {khl_id} | HTTP {resp.status_code}")
            save_status(con, khl_id, STATUS_ERROR)
            errors += 1
            continue

        content = resp.content
        if len(content) < 500:
            # Сервер вернул 200 с пустышкой (иногда бывает заглушка)
            log(logger, "[404]", f"{prefix} {khl_id} | пустой ответ ({len(content)} б)")
            save_status(con, khl_id, STATUS_NO_PHOTO)
            no_photo += 1
            continue

        filename = f"{khl_id}.jpg"
        abs_path = os.path.join(args.out, filename)
        rel_path = os.path.join("players", "khl", filename).replace("\\", "/")

        with open(abs_path, "wb") as f:
            f.write(content)

        save_ok(con, khl_id, rel_path)
        log(logger, "[OK]", f"{prefix} {khl_id} | {len(content):,} б → {rel_path}")
        ok += 1

    con.close()
    log(logger, "[INFO]",
        f"Готово. OK: {ok}, нет фото: {no_photo}, ошибки: {errors}, всего: {total}")


if __name__ == "__main__":
    main()
