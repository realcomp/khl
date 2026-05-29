# download_khl_photos.py — скачивание фотографий игроков khl.ru

Автономный скрипт на Python 3, не зависящий от Django.
Скачивает фотографии игроков с `img.khl.ru` и сохраняет в `media/players/khl/`.
Статус и локальный путь к файлу записываются в `players_parsed.sqlite3`.

URL фото фиксированного формата: `https://img.khl.ru/players/{khl_id}/160.jpg`

---

## Запуск

```bash
# Обычный прогон — скачать все фото (у кого photo_status IS NULL)
python3 download_khl_photos.py

# Сухой прогон — только вывод списка URL, без скачивания
python3 download_khl_photos.py --dry-run

# Повторить записи с ошибкой сети (статус 'error')
python3 download_khl_photos.py --retry-errors

# Явно указать пути
python3 download_khl_photos.py --db players_parsed.sqlite3 --out media/players/khl
```

Запуск в фоне (не прерывается при закрытии терминала):

```bash
nohup python3 download_khl_photos.py > /dev/null 2>&1 &
echo $!   # запомни PID чтобы остановить через kill
```

---

## Аргументы

| Аргумент | По умолчанию | Описание |
|---|---|---|
| `--db FILE` | `players_parsed.sqlite3` | SQLite с игроками |
| `--out DIR` | `media/players/khl` | Папка для сохранения фото |
| `--logs DIR` | `logs/` | Папка для лог-файлов |
| `--retry-errors` | выкл. | Повторить записи со статусом `error` |
| `--dry-run` | выкл. | Только вывод, без скачивания и записи в БД |
| `--delay-min N` | `1.0` | Мин. задержка между запросами (сек) |
| `--delay-max N` | `2.5` | Макс. задержка между запросами (сек) |

---

## Как работает

- При первом запуске добавляет два новых столбца в таблицу `player` (если не существуют)
- Обрабатывает только записи, где `photo_status IS NULL` — повторный запуск безопасен
- Перед каждым запросом ждёт `delay_min`–`delay_max` секунд
- При ошибке сети — повторяет до 3 раз с паузой 2 → 4 → 8 секунд
- Если сервер вернул 200, но тело < 500 байт — считает заглушкой и пишет `no_photo`

---

## Скорость

| Задержка | Примерное время на ~10 500 игроков |
|---|---|
| 1.0–2.5 сек (по умолчанию) | ~5 часов |
| 0.5–1.0 сек | ~2.5 часа |

Скрипт идемпотентен: прерви в любой момент и продолжи — уже обработанные записи пропускаются.

---

## Изменения в players_parsed.sqlite3

Скрипт добавляет два столбца в таблицу `player`:

| Колонка | Тип | Значения |
|---|---|---|
| `photo_local_path` | TEXT | Относительный путь, напр. `players/khl/22135.jpg`, либо NULL |
| `photo_status` | TEXT | `null` — не проверяли, `ok`, `no_photo`, `error` |

---

## Структура файлов на диске

```
media/
└── players/
    └── khl/
        ├── 22135.jpg
        ├── 496.jpg
        └── ...
```

Путь `media/` — корень медиафайлов Django-проекта (`MEDIA_ROOT`).

---

## Лог-файлы

Создаются в `logs/` с именем `download_khl_photos_YYYYMMDD_HHMMSS.log`.

Форматы записей:

```
[OK]       [1/10528] 22135 | 12,430 б → players/khl/22135.jpg
[404]      [2/10528] 99999 | нет фото
[ERR]      [3/10528] 12345 | сетевая ошибка: ConnectionTimeout
[DRY]      [4/10528] 496 → https://img.khl.ru/players/496/160.jpg
[INFO]     Готово. OK: 8200, нет фото: 2100, ошибки: 228, всего: 10528
```

---

## Следующий шаг: перенос фото в django-filer

После скачивания и импорта игроков в `db.sqlite3` фото нужно зарегистрировать
в `django-filer` и привязать к `Player.photo` (FilerImageField).

Это делается отдельной management-командой, которая:
1. Читает `photo_local_path` из `players_parsed.sqlite3` для каждого `khl_id`
2. Открывает файл и создаёт объект `filer.models.Image`
3. Устанавливает `Player.photo = filer_image`

Игроки с `photo_status = 'no_photo'` пропускаются.

---

## Зависимости

```bash
pip3 install requests
```

Python 3.8+, стандартная библиотека (`sqlite3`, `argparse`, `logging`).
