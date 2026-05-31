# Импорт игроков из SQLite в Postgres

Перенос данных из `players_parsed.sqlite3` (результат парсинга KHL) в основную БД Postgres на сервере.

## Текущий статус (май 2026)

Импорт **выполнен**:
- Игроков создано: 4051, обновлено: 2709, без изменений: 3768
- Фотографий импортировано: 3741 (через django-filer)
- Строк статистики (`PlayerSeasonStat`): ~21 881
- Миграция `0088_playerseasonstat` применена

## Архитектура: два уровня статистики

В БД сосуществуют **два разных** способа хранения статистики:

| Таблица | Что хранит | Записей |
|---|---|---|
| `hockeyapp_clubplayermatch` | 1 строка = 1 матч = 1 игрок | ~1.4 млн |
| `hockeyapp_playerseasonstat` | 1 строка = итого за сезон в клубе | ~21 881 |

`PlayerSeasonStat` заполняется из `player_stat` в SQLite (данные с KHL.ru за 2014–2026), покрывает сезоны которых нет в матчах (16/17–25/26 и частично старее).

## Что переносится

| Источник (SQLite) | Назначение (Postgres) | Правило |
|---|---|---|
| `player` | `hockeyapp_player` | создать новых, обновить только пустые поля |
| `player.photo_local_path` | filer + `player.photo` | только если у игрока ещё нет фото |
| `player_stat` | `hockeyapp_playerseasonstat` | upsert (создать или обновить статистику) |

## Требования перед запуском

На сервере должны быть:
- `players_parsed.sqlite3` — в `/opt/sportomatics/media/`
- Фотографии — в `/opt/sportomatics/media/players/khl/<khl_id>.jpg`
- Код задеплоен через `git pull` + `docker compose build web`
- Миграция `0088_playerseasonstat` применена

## Шаг 1 — скопировать файлы на сервер (с Mac)

```bash
# SQLite с данными игроков
scp players_parsed.sqlite3 root@91.99.210.59:/opt/sportomatics/media/

# Фотографии (~9 800 файлов)
rsync -avz --progress media/players/khl/ root@91.99.210.59:/opt/sportomatics/media/players/khl/
```

## Шаг 2 — деплой и миграция (если первый раз на новом сервере)

```bash
cd /opt/sportomatics
git pull origin perf-audit-autofix
docker compose build web
docker compose up -d web
docker exec sportomatics-web-1 python manage.py migrate hockeyapp 0088_playerseasonstat
```

## Шаг 3 — очистка SQLite перед импортом

В `player_stat` могут быть строки-заголовки с неправильными `club_name`:

```bash
sqlite3 /opt/sportomatics/media/players_parsed.sqlite3 "
DELETE FROM player_stat
WHERE club_name IN (
  'Всего в КХЛ:', 'Всего:', 'Кубок Надежды:', 'Плей-офф:', 'Регулярный чемпионат:'
);
"
```

## Шаг 4 — сухой прогон

```bash
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3 --dry-run
```

Вывод покажет:
- сколько игроков будет создано/обновлено
- **Unmatched clubs** — клубы из SQLite, не найденные в Postgres
- **Unmatched seasons** — сезоны не совпавшие с `base_season`
- **Unmatched countries** — страны не найденные в `addresses_country`

## Шаг 5 — полный импорт

```bash
# Только игроки и фото (без статистики)
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3 --skip-stats

# Только статистика (фото уже есть)
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3 --skip-photos
```

### Опции команды

| Флаг | Описание |
|---|---|
| `--db PATH` | Путь к SQLite (по умолчанию `BASE_DIR/players_parsed.sqlite3`) |
| `--dry-run` | Только вывод, ничего не записывает |
| `--skip-photos` | Пропустить импорт фотографий |
| `--skip-stats` | Пропустить импорт PlayerSeasonStat |

## Устранение типовых проблем

### Unmatched seasons — все сезоны не нашлись
`base_season` содержит только старые сезоны. Добавить недостающие:
```bash
docker exec sportomatics-db-1 psql -U sportomatics -d sportomatics -c "
INSERT INTO base_season (ru_title, en_title, title, start_date, end_date) VALUES
  ('Сезон 16/17', 'Season 16/17', 'Сезон 16/17', '2016-07-01', '2017-06-30'),
  ...;
"
```
Формат ключа сезона: `str(start_date.year)[2:] + '/' + str(end_date.year)[2:]` → `"22/23"`.

### Unmatched clubs
Проверить как клуб называется в БД:
```bash
docker exec sportomatics-db-1 psql -U sportomatics -d sportomatics -c "
SELECT id, ru_title FROM hockeyapp_club WHERE ru_title ILIKE '%название%';
"
```
Если клуб есть под другим именем — исправить `club_name` в SQLite:
```bash
sqlite3 /opt/sportomatics/media/players_parsed.sqlite3 \
  "UPDATE player_stat SET club_name = 'Правильное название' WHERE club_name = 'Неправильное';"
```
Если клуба нет совсем — добавить (все поля NOT NULL обязательны):
```bash
docker exec sportomatics-db-1 psql -U sportomatics -d sportomatics -c "
INSERT INTO hockeyapp_club (ru_title, en_title, title, site, contacts, html_body, proccesed_time, url, fb, gl, im, ok, pp, tw, ut, vk, main_color, secondary_color, third_color)
VALUES ('Название', 'Name', 'Название', '', '', '', NOW(), '', '', '', '', '', '', '', '', '', '', '', '');
"
```

### Unmatched countries
Страны с нестандартными названиями добавить в `addresses_country`:
```bash
docker exec sportomatics-db-1 psql -U sportomatics -d sportomatics -c "
INSERT INTO addresses_country (ru_title, en_title, title) VALUES ('Название', 'Name', 'Название');
"
```

### Записи с club=NULL после импорта — переимпортировать
```bash
# Удалить кривые записи
docker exec sportomatics-db-1 psql -U sportomatics -d sportomatics -c "
DELETE FROM hockeyapp_playerseasonstat WHERE club_id IS NULL;
"
# Переимпортировать
docker exec sportomatics-web-1 python manage.py import_sqlite_players \
  --db /app/media/players_parsed.sqlite3 --skip-photos
```

### SyntaxError / ImportError при запуске
- Код в контейнере старый — нужен `git pull` + `docker compose build web` + `docker compose up -d web`
- Затем `docker cp` не нужен, команда уже в образе

## Известные несоответствия названий клубов

| В SQLite | В БД (id) |
|---|---|
| Лев Пп | Лев Попрад (165) |
| Лев Пр | Лев Прага (226) |
| Куньлунь РС | Куньлунь РС (добавлен вручную) |
| Драконы | Драконы (добавлен вручную) |
