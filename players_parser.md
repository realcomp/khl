# Парсер сезонной статистики игроков khl.ru

## Команда для бекапа БД (SQLite)

```bash
# Выполни перед запуском парсера:
sqlite3 /Users/Shared/Projects/khl/db.sqlite3 ".backup '/Users/Shared/Projects/khl/db.sqlite3.backup_$(date +%Y%m%d_%H%M%S)'"
```

---

## Что выяснено по реальному HTML khl.ru

**URL карточки:** `https://www.khl.ru/players/{id}/`
Сайт отдаёт 403 на curl/дефолтный requests, но нормально работает с реалистичным User-Agent + Cookie-сессией через `urllib` или `requests.Session`.

**Структура карточки игрока** (блок `frameCard-header__detail-body`):
- Имя (ru): `frameCard-header__detail-titleItem`
- Имя (en): следующий div после русского имени
- Клуб, амплуа — в одной строке
- Поля-детали: дата рождения, возраст, гражданство, сборная, рост, вес, хват, контракт до
- Фото: `//img.khl.ru/players/{id}/160.jpg` (фиксированный паттерн)

**Таблица статистики** — блок `div.statTable-tabContent.fade` (первый — сезонная, второй — поматчевая):

Структура строк:
```
<tr>  →  "25/26 | плей-офф"          ← строка-заголовок сезона
<tr>  →  "Локомотив | 47 | 22 | ..."  ← строка данных клуба
```

---

## Колонки статистики

### Полевые игроки (нападающие, защитники)

| Аббр. | Расшифровка | Поле в модели |
|---|---|---|
| №  | Номер игрока | `number` |
| И  | Игры | `matches` |
| Ш  | Голы | `goals` |
| А  | Передачи | `assists` |
| О  | Очки | `points` |
| +/- | Плюс/Минус | `plus_minus` |
| +  | Плюс | `plus` |
| -  | Минус | `minus` |
| Штр | Штрафное время | `penalty_time` |
| ШР | Шайбы в равенстве | `es_goals` |
| ШБ | Шайбы в большинстве | `pp_goals` |
| ШМ | Шайбы в меньшинстве | `sh_goals` |
| ШО | Шайбы в овертайме | `overtime_goals` |
| ШП | Победные шайбы | `win_goals` |
| РБ | Решающие буллиты | `bullet_goals` |
| БВ | Броски по воротам | `shots` |
| %БВ | % реализованных бросков | `pis` |
| БВ/И | Бросков за игру | `shots_per_game` |
| Вбр | Вбрасывания | `faceoff` |
| ВВбр | Выигранные вбрасывания | `winfaceoff` |
| %Вбр | % выигранных вбрасываний | `winfaceoff_p` |
| ВП/И | Время на площадке за игру | `icetime_per_game` |
| СПр | Силовые приёмы | `hits` |
| БлБ | Блокированные броски | `blocks` |
| ФоП | Фолы против | `fouls` |
| ОТБ | Отборы шайбы | `takeaways` |
| ПХТ | Перехват передачи | `interceptions` |

### Вратари

| Аббр. | Расшифровка | Поле в модели |
|---|---|---|
| И  | Игры | `matches` |
| В  | Победы | `wins` |
| П  | Поражения | `losses` |
| ИБ | Игры в буллитах | `bullet_matches` |
| Бр | Броски по воротам (по вратарю) | `shots_received` |
| ПШ | Пропущенные шайбы | `loose_goals` |
| ОБ | Отражённые броски | `saves` |
| %ОБ | % отражённых бросков | `saves_p` |
| КН | Коэффициент надёжности | `sf` |
| Ш  | Голы (вратаря) | `goals` |
| А  | Передачи (вратаря) | `assists` |
| И"0" | Матчи "на ноль" (shutouts) | `zero_goals_matches` |
| Штр | Штрафное время | `penalty_time` |
| ВП | Время на площадке | `gamingtime` |

---

## Новая модель: `PlayerSeasonStat`

Отдельная модель для агрегированных сезонных данных с сайта khl.ru.
Не заменяет `ClubPlayerMatch` (поматчевые данные), а дополняет их сводными данными за сезон.

```
Player ─── PlayerSeasonStat ─── Club (FK)
                             ─── Season (FK)
                             ─── tournament_type ('regular', 'playoff', 'other')
                             ─── [все поля статистики]
```

Уникальное ограничение: `unique_together = (player, club, season, tournament_type)`

Файл: `hockeyapp/models/players.py` (добавить рядом с `ClubPlayer`)

---

## Логика сохранения

1. `get_or_create(Player, khl_id=id)` → обновить bio-поля
2. Для каждой строки таблицы:
   - Распарсить строку-заголовок: `"25/26 | рег.чемпионат"` → сезон + тип турнира
   - Тип: `рег.чемпионат` → `regular`, `плей-офф` → `playoff`, остальное → `other`
   - Сезон "25/26" → найти `Season` по `start_date.year=2025`, иначе создать
   - Клуб: найти `Club` по `ru_title__icontains=название`, иначе `create(ru_title=название)` — атрибуты заполним отдельным парсером клубов
   - **Фильтр по году:** если `Player` уже существовал в БД до запуска → пропускать строки с `season.start_date.year < 2014`
   - `update_or_create(PlayerSeasonStat, player=p, club=c, season=s, tournament_type=t)`

---

## Стратегия перебора и rate limiting

```
start_id = 1 (или --start N)
consecutive_fails = 0
MAX_FAILS = 30

for id = start_id, start_id+1, ...:
    sleep(random.uniform(3.0, 7.0))  # до каждого запроса
    response = fetch(url, session, timeout=15, retries=3, backoff)
    if 404 or empty:
        consecutive_fails += 1
        if consecutive_fails >= MAX_FAILS: break
        continue
    consecutive_fails = 0
    parse_and_save(response)
```

HTTP-сессия: `requests.Session` с реалистичными заголовками, повторное использование TCP-соединения.

При ошибке сети / 5xx: повторить до 3 раз с экспоненциальной паузой (2s → 4s → 8s), потом пропустить и залогировать.

---

## Логирование

Каждая строка лога — одна запись:

```
[OK]   496 | Радулов Александр | нападающий | 16 сезонов | https://www.khl.ru/players/496/
[NEW]  497 | новый игрок создан, 8 сезонов сохранено
[UPD]  498 | игрок обновлён, добавлено 3 новых сезона с 2014+
[404]  499 | не найден (подряд: 1/30)
[SKIP] 500 | страница пустая
[ERR]  501 | ConnectionTimeout (попытка 3/3), пропущен
```

- Stdout: всё выше
- Файл: `logs/fetch_khl_players_YYYYMMDD_HHMMSS.log`

---

## Management-команда

Файл: `hockeyapp/management/commands/fetch_khl_players.py`

```bash
# Полный прогон с нуля
./manage.py fetch_khl_players

# Начать с конкретного ID (продолжить после паузы)
./manage.py fetch_khl_players --start 400

# Тест без записи в БД
./manage.py fetch_khl_players --start 490 --end 500 --dry-run
```

---

## Парсер

Файл: `hockeyapp/parsers/player.py` — добавить классы:
- `KHLPlayerPageV2` — парсит bio-карточку игрока
- `KHLPlayerSeasonStatsV2` — парсит таблицу сезонной статистики

Технический стек: `requests.Session` + `lxml` (как в существующих парсерах через `GrabParser`).

---

## Что НЕ входит в задачу

- Поматчевая статистика (второй таб "Матчи КХЛ") — отдельная задача
- Заполнение атрибутов новых клубов (лига, город, логотип) — парсер клубов уже есть (`get_all_club_datas`)
- Загрузка фото игроков — URL известен (`//img.khl.ru/players/{id}/160.jpg`), сохраняем как `ava_url`, загрузку делаем отдельно
