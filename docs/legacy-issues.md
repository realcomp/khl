# Legacy-проблемы и ограничения

## Python 2.7 + Django 1.7 — главное ограничение

Весь проект написан на **Python 2.7** (EOL с 2020 года).

Последствия:
- `urlparse` — из стандартной библиотеки Python 2, в Python 3 это `urllib.parse`
- `from __future__ import unicode_literals` — везде в начале файлов
- `ugettext_lazy` вместо `gettext_lazy`
- `django.conf.urls.patterns()` — устаревший API
- `TEMPLATE_DIRS`, `TEMPLATE_CONTEXT_PROCESSORS` — старый стиль (не `TEMPLATES = [...]`)
- Нет f-строк, нет `async/await`, нет type hints
- `django.core.urlresolvers` (старый путь, в Django 2+ это `django.urls`)

**При любом изменении Python-кода** использовать только синтаксис Python 2.7.

## Gulp 3 — нерабочий

`gulpfile.js` использует Gulp 3, который **несовместим с Node 20+**:
```
ReferenceError: primordials is not defined
```

**Не пытаться запускать `gulp`** для пересборки `app.js`.

### Как пересобрать app.js вручную

`app.js` — конкатенация всех файлов из `base/static/js/` в определённом порядке.

```bash
# На локальной машине (Python 3)
python3 -c "
import os, glob
order_file = 'base/static/js/router.js'
controllers = sorted(glob.glob('base/static/js/controllers/*.js'))
services = sorted(glob.glob('base/static/js/services/*.js'))
others = [
    'base/static/js/script.min.js',
    'base/static/js/players-scripts.js',
    'base/static/js/players-checkbox.js',
    'base/static/js/players-dropdown.js',
    'base/static/js/dropdown.js',
    'base/static/js/club-team.js',
    'base/static/js/angucomplete.js',
]
files = [order_file] + controllers + services + others
with open('base/static/build/app.js', 'w') as out:
    for f in files:
        if os.path.exists(f):
            out.write(open(f).read())
            out.write(';\n')
"
# Проверить синтаксис
node --check base/static/build/app.js
```

После изменения `app.js` — коммитить файл и деплоить через `docker compose build web`.

## Два разных формата фото

В проекте **два разных формата** для поля `photo` в зависимости от сериализатора:

### 1. Простая строка URL (большинство сериализаторов в `hockeyapp/`)

```python
# hockeyapp/serializers/__init__.py, clubs.py, players.py
photo = serializers.SerializerMethodField()
def get_photo(self, obj):
    return _photo_path(obj.photo)
# → "/media/filer_public/63/16/.../4804.jpeg"
```

В шаблоне: `<img src="{{ photo }}">` или `ng-src="{{player.photo}}"`

### 2. Объект FIFSerialiser (партнёры, API-игроки)

```python
# api/base/serializers.py — FIFSerialiser
# Возвращает: {"id": 1686, "file": "/media/...", "name": "...", "_height": 250, "_width": 200}
```

В шаблоне: **обязательно** `ng-src="{{player.photo.file}}"` — нужно обращаться к `.file`!

**Ошибка**: если использовать `{{player.photo}}` — Angular вставит весь JSON-объект как URL,
и получится 404 на URL вида `%7B%22id%22:1686,%22file%22:...%7D`.

## Медиафайлы и URL

`MEDIA_URL = '/media/'` — относительный путь.

`obj.photo.url` (Django-Filer) может возвращать **полный URL** вида
`http://dev.sportomatics.ru/media/...` если в `local_settings.py` на сервере
настроен `FILER_STORAGES` с абсолютным базовым URL.

**Решение**: функция `_photo_path()` в `hockeyapp/serializers/__init__.py`
и `_url_path()` в `api/base/serializers.py` — обе обрезают схему+хост,
возвращая только путь `/media/...`.

```python
from urlparse import urlparse

def _url_path(url):
    if not url:
        return url
    parsed = urlparse(url)
    return parsed.path if parsed.scheme else url
```

**Все сериализаторы** должны использовать эти функции — никакого
`ReadOnlyField(source='logo.url')` или `ReadOnlyField(source='photo.url')` напрямую.

## Хардкод `http://dev.sportomatics.ru` — устранён

`dev.sportomatics.ru` — мёртвый домен, которого не существует.
Все вхождения удалены в коммите `b4be3b8f` (май 2026).

Если вдруг найдётся новое вхождение — искать и удалять:
```bash
grep -rn "dev\.sportomatics\.ru" . --include="*.py" --include="*.html" --include="*.js"
```

## `DEBUG = True` в settings.py

В `settings.py` прописан `DEBUG = True` — это нормально, так как `local_settings.py`
на сервере переопределяет его. Но `local_settings.py` не в git — не редактировать
настройки напрямую в `settings.py` ожидая что это изменит поведение на сервере.

## Устаревшие зависимости

| Пакет | Версия | Проблема |
|---|---|---|
| Django | 1.7.4 | EOL, нет security patches |
| djangorestframework | 3.1.1 | Очень старый |
| django-filer | 0.9.9 | Старый, патчится через sed в Dockerfile |
| celery | 3.1.17 | EOL |
| django-polymorphic | 0.8.1 | Старый |
| kombu | 3.0.24 | Патчится через sed в Dockerfile |

Dockerfile содержит `sed`-патчи для совместимости:
```dockerfile
RUN sed -i 's/from uuid import UUID...' /usr/local/lib/python2.7/.../kombu/...
RUN sed -i 's/from filer.models import mixins...' /usr/local/lib/python2.7/.../filer/...
RUN sed -i 's/from polymorphic import ...' /usr/local/lib/python2.7/.../filer/...
```

## Google Maps без API-ключа

В шаблонах подключены Google Maps v3.2 без API-ключа:
- Предупреждение `NoApiKeys` в консоли
- Предупреждение `RetiredVersion` (v3.2 снята с поддержки)
- Карты работают, но с ограничениями

## Социальная аутентификация

`django-social-auth` 0.7.28 — очень старая версия.
Ключи API для Twitter, Facebook, VK и других прописаны пустыми в `settings.py`.
Реальные ключи — только в `local_settings.py` на сервере.

## Google OAuth2 credentials в settings.py

`GOOGLE_OAUTH2_CLIENT_ID` и `GOOGLE_OAUTH2_CLIENT_SECRET` прописаны
прямо в `settings.py` (публичный git-репозиторий). Это потенциальная
утечка — но поскольку ключи уже там, менять пока не нужно, если они рабочие.

## SECRET_KEY в settings.py

`SECRET_KEY` прописан прямо в `settings.py`. Аналогично — уже публично,
но переопределяется через `local_settings.py` на проде.
