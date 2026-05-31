# Импорт игроков из SQLite в Postgres

Перенос данных из `players_parsed.sqlite3` (результат парсинга KHL) в основную БД Postgres на сервере.

## Что переносится

| Источник (SQLite) | Назначение (Postgres) | Правило |
|---|---|---|
| `player` | `hockeyapp_player` | создать новых, обновить только пустые поля |
| `player.photo_local_path` | filer + `player.photo` | только если у игрока ещё нет фото |
| `player_stat` | `hockeyapp_playerseasonstat` | upsert (создать или обновить статистику) |

## Требования перед запуском

На сервере должны быть:
- `players_parsed.sqlite3` — в `/opt/sportomatics/media/` (или указать путь через `--db`)
- Фотографии — в `/opt/sportomatics/media/players/khl/<khl_id>.jpg`
- Management command — `hockeyapp/management/commands/import_sqlite_players.py` в образе

## Шаг 1 — скопировать файлы на сервер (с Mac)

```bash
# SQLite с данными игроков
scp players_parsed.sqlite3 root@server:/opt/sportomatics/media/

# Фотографии (~9 800 файлов)
rsync -avz --progress media/players/khl/ root@server:/opt/sportomatics/media/players/khl/

# Management command (если код не задеплоен через git + docker build)
scp hockeyapp/management/commands/import_sqlite_players.py \
  root@server:/tmp/import_sqlite_players.py
```

## Шаг 2 — скопировать management command в контейнер

```bash
# Если файл передан через /tmp:
docker cp /tmp/import_sqlite_players.py \
  sportomatics-web-1:/app/hockeyapp/management/commands/

# Если код уже в образе после git pull + docker compose build web — этот шаг не нужен
```

## Шаг 3 — сухой прогон

```bash
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3 --dry-run
```

Вывод покажет:
- сколько игроков будет создано/обновлено
- **Unmatched clubs** — названия клубов из SQLite, не найденные в Postgres
- **Unmatched seasons** — строки сезонов (например `"22/23"`), не совпавшие с Season
- **Unmatched countries** — страны, не найденные в `addresses_country`

## Шаг 4 — полный импорт

```bash
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3
```

### Опции команды

| Флаг | Описание |
|---|---|
| `--db PATH` | Путь к SQLite (по умолчанию `BASE_DIR/players_parsed.sqlite3`) |
| `--dry-run` | Только вывод, ничего не записывает |
| `--skip-photos` | Пропустить импорт фотографий |
| `--skip-stats` | Пропустить импорт PlayerSeasonStat |

## Примечания

- **Существующие игроки**: поля обновляются только если они пустые/null в Postgres — данные, внесённые вручную, не затираются.
- **Статистика**: всегда перезаписывается (upsert) — это основная цель импорта.
- **Фотографии**: загружаются через django-filer только если `player.photo` ещё не задан.
- `photo_local_path` в SQLite хранится относительно `media/`, например `players/khl/1.jpg`. Абсолютный путь внутри контейнера: `/app/media/players/khl/1.jpg`.
- Незаматченные клубы и сезоны выводятся в конце — их нужно добавить как алиасы или завести в БД вручную.
