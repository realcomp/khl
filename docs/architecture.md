# Архитектура проекта

## Стек

| Слой | Технология | Версия |
|---|---|---|
| Язык | Python | **2.7** (EOL) |
| Фреймворк | Django | **1.7.4** (очень старый) |
| API | Django REST Framework | 3.1.1 |
| БД | PostgreSQL | 9.6 |
| Кэш/очередь | Redis | 4.0 |
| Задачи | Celery | 3.1.17 |
| Медиафайлы | django-filer | 0.9.9 |
| Фронтенд | AngularJS | ~1.x |
| Сборка JS | Gulp 3 (нерабочий) | — |
| Веб-сервер | Gunicorn + Nginx | — |
| Контейнеризация | Docker Compose | v3.7 |

## Django-приложения

```
accounts/       — пользователи, аутентификация
addresses/      — адреса, города, страны
api/            — REST API endpoints
  addresses/    — API для адресов
  base/         — базовые сериализаторы (FIFSerialiser, _url_path)
  hockey/       — API для хоккейных данных (клубы, матчи, партнёры)
base/           — базовые модели, шаблоны, статика
bower/          — Bower-пакеты через Django (устарело)
hockeyapp/      — основное приложение (клубы, игроки, матчи)
  models/       — модели данных
  serializers/  — сериализаторы DRF
  views/        — Django views
  templates/    — HTML-шаблоны
  tasks/        — Celery-задачи (парсинг, счётчики)
sportomatics/   — конфигурация Django (settings, urls, wsgi)
```

## Docker-контейнеры

| Контейнер | Роль |
|---|---|
| `web` | Django + Gunicorn, порт 8000 |
| `nginx` | Проксирование, статика, медиа; порт 3011→80 |
| `db` | PostgreSQL (том `pgdata`) |
| `redis` | Кэш + брокер Celery (том `redisdata`) |
| `celery_worker` | Фоновые задачи |
| `celery_beat` | Планировщик задач |

## Тома и файлы

```
./media/        → /app/media (bind-mount в web и nginx)
./nginx/        → конфиг nginx
static_volume   → /app/static (named volume, общий для web и nginx)
pgdata          → данные PostgreSQL
redisdata       → данные Redis
```

## Nginx

Конфиг: `nginx/default.conf`
- `/media/` → `/app/media/` (bind-mount из `./media/`)
- `/static/` → `/app/static/` (named volume)
- `/` → `proxy_pass http://web:8000`

## URL-структура

```
/admin/                 — Django Admin (suit)
/api/...                — REST API
/ru/hockey/             — основные страницы (i18n_patterns)
/ru/hockey/players/<id>/        — карточка игрока
/ru/hockey/clubs/<slug>/        — страница клуба
/ru/hockey/players/<id>/partners/   — партнёры игрока
```

## Настройки

`sportomatics/settings.py` — базовые настройки (коммитятся в git)

`local_settings.py` — серверные настройки (НЕ в git, только на сервере).
Переопределяет: `DATABASES` (PostgreSQL), `MEDIA_URL`, `FILER_STORAGES`,
`SECRET_KEY`, `DEBUG`, `BROKER_URL`, `CACHES`.

По умолчанию в `settings.py`:
- `DEBUG = True` — на сервере переопределяется через `local_settings.py`
- `DATABASES` → SQLite (на сервере → PostgreSQL)
- `BROKER_URL` → `redis://localhost:6379/0` (на сервере → `redis://redis:6379/0`)
- `CACHES` → localhost Redis (на сервере → `redis://redis:6379/0`)

## Фронтенд

- **AngularJS** — все динамические компоненты
- Контроллеры: `base/static/js/controllers/*.js`
- Сервисы: `base/static/js/services/*.js`
- Собранный бандл: `base/static/build/app.js`
- Сторонние библиотеки: `base/static/build/libs.min.js`

В Django-шаблонах AngularJS-блоки оборачиваются в `{% verbatim %}...{% endverbatim %}`,
чтобы Django не интерпретировал `{{ }}` как свои переменные.

## Интернационализация

Сайт двуязычный: русский (`/ru/`) и английский (`/en/`).
Переводы: `locale/ru/`, `locale/en/`.
Управление через Rosetta: `/rosetta/`.
Большинство контента только на русском языке.
