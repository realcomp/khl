# Парсер и импорт матчей КХЛ

Система состоит из двух шагов: локальный парсер собирает данные с khl.ru в промежуточный SQLite-файл, затем Django-команда переносит их в PostgreSQL на сервере.

```
khl.ru  →  parse_khl_calendar.py  →  khl_calendar.sqlite3  →  import_khl_calendar  →  PostgreSQL
```

---

## Файлы

| Файл | Назначение |
|---|---|
| `parse_khl_calendar.py` | Парсер. Запускается локально, не требует Django |
| `games.txt` | Список URL для парсинга — редактируется вручную |
| `khl_calendar.sqlite3` | Промежуточная база — результат парсера |
| `hockeyapp/management/commands/import_khl_calendar.py` | Django-команда для вливания в PostgreSQL |

---

## games.txt — формат файла

Каждая строка: `МЕТКА URL`

- Метка начинается с `REG` (регулярный чемпионат) или `PO` (плей-офф)
- Сезон в формате `ДД/ДД` (например `25/26`) — можно писать слитно или через пробел
- URL — всегда последний токен в строке, начинается с `https://`
- Строки, начинающиеся с `#`, и пустые строки игнорируются

```
# Сезон 2025-2026
REG25/26  https://www.khl.ru/calendar/1369/00/
PO25/26   https://www.khl.ru/calendar/1370/00/

# Сезон 2024-2025
REG 24/25  https://www.khl.ru/calendar/1288/00/
PO 24/25   https://www.khl.ru/calendar/1289/00/
```

Откуда брать URL: на сайте khl.ru открыть нужный календарь сезона, скопировать адрес страницы. ID сезона виден прямо в URL: `khl.ru/calendar/`**1369**`/00/`.

---

## Шаг 1 — запуск парсера (локально)

```bash
# Базовый запуск: читает games.txt, пишет khl_calendar.sqlite3
python3 parse_khl_calendar.py

# Явно указать файлы
python3 parse_khl_calendar.py --games games.txt --db khl_calendar.sqlite3

# Дополнительно сохранить в JSON (удобно для отладки)
python3 parse_khl_calendar.py --json matches.json
```

**Что происходит при запуске:**

1. Читает `games.txt`, распознаёт метки и URL
2. Открывает `requests.Session()` — сессия автоматически получает cookie с первого редиректа khl.ru (без этого сайт отдаёт 403)
3. Для каждого URL загружает страницу и обходит блоки `calendary-body__item`
4. Из каждой карточки матча извлекает данные и записывает в SQLite через `INSERT OR REPLACE` (повторный запуск безопасен — перезапишет)

**Зависимости** (стандартные для проекта): `requests`, `lxml`

---

## Что собирает парсер

Для каждого матча в `khl_calendar.sqlite3` сохраняются:

| Колонка | Пример | Описание |
|---|---|---|
| `khl_id` | `897597` | ID матча на khl.ru (PRIMARY KEY) |
| `season_khl_id` | `1369` | ID сезона (из URL календаря) |
| `season_label` | `REG25/26` | Метка из games.txt |
| `season` | `25/26` | Сезон |
| `is_playoff` | `0` / `1` | Плей-офф? |
| `date` | `20 марта 2026, Пт` | Дата матча (строка) |
| `game_number` | `№ 107` | Номер матча в сезоне |
| `home_team` | `СКА` | Хозяева (ru_title) |
| `home_team_slug` | `ska` | Слаг команды из URL |
| `guest_team` | `Драконы` | Гости (ru_title) |
| `guest_team_slug` | `dragons` | Слаг команды из URL |
| `home_score` | `5` | Голы хозяев |
| `guest_score` | `1` | Голы гостей |
| `overtime` | `0` / `1` | Победа в овертайме |
| `shootout` | `0` / `1` | Победа по буллитам |
| `period_scores` | `3:1,1:0,1:0` | Счёт по периодам (через запятую) |
| `is_finished` | `0` / `1` | Матч сыгран? |
| `match_url` | `https://www.khl.ru/game/1369/897597/resume/` | Карточка матча на сайте |
| `protocol_url` | `https://www.khl.ru/game/1369/897597/protocol/` | Протокол матча |

Матчи которые ещё не сыграны сохраняются без `home_score`, `guest_score`, `overtime`, `shootout`, `period_scores`.

---

## Шаг 2 — перенос файла на сервер

```bash
scp khl_calendar.sqlite3 user@server:/path/to/project/
```

---

## Шаг 3 — импорт в PostgreSQL (на сервере)

```bash
# Сначала обязательно: dry-run — посмотреть что произойдёт без записи
python manage.py import_khl_calendar --dry-run

# Реальный импорт
python manage.py import_khl_calendar

# Указать путь к SQLite вручную
python manage.py import_khl_calendar --db /path/to/khl_calendar.sqlite3

# Обновить счёт у матчей которые уже есть в БД
python manage.py import_khl_calendar --update-scores
```

**Что делает команда:**

Для каждой строки из SQLite:

1. Ищет `Club` (хозяева и гости) — сначала по slug в поле `Club.url`, потом по точному `ru_title`, потом по `icontains`. Если клуб не найден — **создаёт минимальную запись автоматически** (`ru_title` + `url` вида `khl.ru/clubs/ska/`). Логирует каждое создание.
2. Ищет `Challenge` по `khl_id` сезона — должен уже существовать в БД.
3. Создаёт `Schedule` (запись в календаре) с `khl_id`, датой, командами, типом чемпионата.
4. Если матч сыгран — создаёт `Match` с `home_score`, `guest_score`, `overtime_win`, `bullet_win` и привязывает к Schedule через OneToOne.
5. Если запись с таким `khl_id` уже есть — пропускает (если не передан `--update-scores`).

**Поля Match которые НЕ заполняются** (только из протокола, не из календаря): `spectators`, `judges`, `players`, `goals_history`, `penalties_history`, `html_body`.

---

## Предварительное условие: Challenge должен существовать

`Challenge` — это сезон/турнир в Django-модели. Команда ищет его по `khl_id`, но не создаёт сама.

Перед первым импортом нового сезона нужно вручную создать `Challenge` в Django-админке:

- `khl_id` — ID из URL календаря (`khl.ru/calendar/`**1369**`/00/`)
- `league` — КХЛ
- `challenge_type` — 1 (Регулярный чемпионат) или 2 (Плей-офф)
- `season` — нужный Season

Если `Challenge` не найден, команда выводит предупреждение, но продолжает — `Schedule` создаётся с `challenge=None`.

---

## Типичный полный цикл

```bash
# 1. Отредактировать games.txt — добавить новые сезоны

# 2. Запустить парсер локально
python3 parse_khl_calendar.py

# 3. Скопировать на сервер
scp khl_calendar.sqlite3 user@server:/app/

# 4. На сервере: проверить что всё выглядит правильно
python manage.py import_khl_calendar --dry-run

# 5. Создать недостающие Challenge в админке (если нужно)

# 6. Запустить импорт
python manage.py import_khl_calendar
```

---

## Частые проблемы

**Новые клубы появляются автоматически**
Если клуб не найден в БД — команда создаёт его сама с минимальными данными (`ru_title` и `url`). Вручную ничего создавать не нужно. После импорта в Django-админке можно дозаполнить остальные поля (логотип, арена, тренер и т.д.).

**«Challenge не найден для khl_id=1369»**
Не создан Challenge для этого сезона. Создать вручную в Django-админке (см. раздел выше).

**Парсер получает 403 при запуске**
khl.ru делает 307-редирект и ставит cookie. `requests.Session()` обрабатывает это автоматически. Если 403 всё равно возникает — возможно, сайт добавил дополнительную защиту. Попробовать запустить чуть позже или с другого IP.

**Повторный запуск парсера**
Безопасен: `INSERT OR REPLACE` перезаписывает существующие строки по `khl_id`. Удалять старый SQLite не нужно.

**Повторный запуск import_khl_calendar**
Без `--update-scores` уже существующие матчи пропускаются. С `--update-scores` — обновляются поля счёта.
