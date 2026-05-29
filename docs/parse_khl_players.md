# parse_khl_players.py — парсер игроков khl.ru

Автономный скрипт на Python 3, не зависящий от Django.
Собирает биографию и сезонную статистику игроков с сайта khl.ru
и сохраняет результат в локальный SQLite-файл.

---

## Запуск

```bash
# Полный прогон (ID 1–25000)
python3 parse_khl_players.py

# Начать с конкретного ID
python3 parse_khl_players.py --start 12345

# Задать диапазон
python3 parse_khl_players.py --start 490 --end 500

# Указать свой файл БД
python3 parse_khl_players.py --db my_output.sqlite3

# Перепарсить всё заново (игнорировать уже сохранённые ID)
python3 parse_khl_players.py --no-resume
```

Запуск в фоне (не прерывается при закрытии терминала):

```bash
nohup python3 parse_khl_players.py > /dev/null 2>&1 &
echo $!   # запомни PID чтобы остановить через kill
```

---

## Аргументы

| Аргумент | По умолчанию | Описание |
|---|---|---|
| `--start N` | 1 | Первый ID игрока |
| `--end N` | 25000 | Последний ID игрока |
| `--db FILE` | `players_parsed.sqlite3` | Путь к SQLite-файлу результата |
| `--logs DIR` | `logs/` | Папка для лог-файлов |
| `--resume` | включён | Пропускать уже разобранные ID |
| `--no-resume` | — | Перепарсить все ID заново |

---

## Как работает

- Перебирает ID от `--start` до `--end` последовательно
- Перед каждым запросом ждёт `2–4` секунды (случайная задержка)
- При ошибке сети — повторяет до 3 раз с паузой 2 → 4 → 8 секунд
- При HTTP 404 — фиксирует в лог и продолжает (цикл **не прерывается**)
- Уже разобранные ID пропускаются (`--resume`, включён по умолчанию) — это позволяет безопасно возобновить прерванный прогон
- Использует `requests.Session` с реалистичными заголовками браузера

---

## Скорость

| Задержка | Среднее время на 25 000 ID |
|---|---|
| 2–4 сек (текущая) | ~21 час |
| 1–3 сек | ~14 часов |
| 3–7 сек | ~35–70 часов |

---

## Структура SQLite

### Таблица `player` — биография

| Колонка | Тип | Описание |
|---|---|---|
| `khl_id` | INTEGER PK | ID игрока на khl.ru |
| `ru_fio` | TEXT | Имя на русском |
| `en_fio` | TEXT | Имя на английском |
| `birth_date` | TEXT | Дата рождения |
| `citizenship` | TEXT | Гражданство |
| `height` | INTEGER | Рост (см) |
| `weight` | INTEGER | Вес (кг) |
| `grip` | TEXT | Хват |
| `contract_to` | TEXT | Контракт до |
| `position` | TEXT | Амплуа (текст с сайта) |
| `is_goalie` | INTEGER | 1 если вратарь |
| `url` | TEXT | URL страницы |
| `parsed_at` | TEXT | Время парсинга |

### Таблица `player_stat` — сезонная статистика

Уникальный ключ: `(player_khl_id, club_name, season_str, tournament_type)`

**Общие поля:**

| Колонка | Описание |
|---|---|
| `player_khl_id` | FK → player.khl_id |
| `club_name` | Название клуба (текст с сайта) |
| `season_str` | Сезон, например `25/26` |
| `tournament_type` | `regular` / `playoff` / `other` |
| `is_goalie` | 1 если вратарь |

**Полевые игроки:**

`number`, `matches`, `goals`, `assists`, `points`, `plus_minus`, `plus`, `minus`, `penalty_time`, `es_goals`, `pp_goals`, `sh_goals`, `overtime_goals`, `win_goals`, `bullet_goals`, `shots`, `pis`, `shots_per_game`, `faceoff`, `winfaceoff`, `winfaceoff_p`, `icetime_per_game`, `hits`, `blocks`, `fouls`, `takeaways`, `interceptions`

**Вратари:**

`matches`, `wins`, `losses`, `bullet_matches`, `shots_received`, `loose_goals`, `saves`, `saves_p`, `sf`, `goals`, `assists`, `zero_goals_matches`, `penalty_time`, `gamingtime`

---

## Лог-файлы

Создаются в папке `logs/` с именем `fetch_khl_players_YYYYMMDD_HHMMSS.log`.
Дублируются в stdout.

Форматы записей:

```
[OK]    496 | Александр Радулов | нападающий | 26 сезонов | https://...
[SKIP]  497 | уже в БД
[404]   499 | не найден (подряд: 3)
[ERR]   501 | ConnectionTimeout (попытка 3/3), пропущен
```

---

## Перенос данных на сервер

После завершения прогона файл `players_parsed.sqlite3` переносится на сервер,
где Django-команда `import_khl_stats` читает его и загружает данные
в PostgreSQL с правильным разрешением FK (Player по khl_id, Club по названию,
Season по году).

```bash
# На сервере (в Docker):
docker-compose exec web ./manage.py import_khl_stats --db players_parsed.sqlite3
```

---

## Зависимости

```bash
pip3 install requests lxml
```

Python 3.8+, стандартная библиотека (`sqlite3`, `argparse`, `logging`).
