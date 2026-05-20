# Документация проекта Sportomatics / KHL

Сайт хоккейной статистики. Работает на `khl.sportomatics.com`.

## Файлы документации

| Файл | Содержание |
|---|---|
| [deploy.md](deploy.md) | **Деплой на сервер** — команды, workflow, как обновить код |
| [architecture.md](architecture.md) | Архитектура, стек, приложения, Docker-контейнеры |
| [legacy-issues.md](legacy-issues.md) | **Важно перед разработкой** — Python 2.7, сломанный Gulp, хардкод, старые зависимости |
| [serializers.md](serializers.md) | Устройство сериализаторов, правила для фото/логотипов |
| [frontend.md](frontend.md) | AngularJS, app.js, ng-src vs src, шаблоны |
| [media-files.md](media-files.md) | Медиафайлы — хранение, 404, восстановление |

## TL;DR — Самое важное

1. **Python 2.7 + Django 1.7** — писать только совместимый код
2. **Код запечён в Docker-образ** → после изменений нужен `docker compose build web`
3. **Gulp сломан** → `app.js` пересобирать вручную Python-скриптом (см. [legacy-issues.md](legacy-issues.md))
4. **Нет локального Docker** → всё тестируется на сервере `/opt/sportomatics/`
5. **Фото через FIFSerialiser** → в Angular шаблонах обязательно `.photo.file`, не `.photo`
6. **`logo.url` / `photo.url` напрямую = баг** → всегда через `_photo_path()` / `_url_path()`
7. **`local_settings.py`** на сервере переопределяет базы данных, Redis, Debug и прочее — не в git

## Сервер

```
SSH: root@<IP сервера>
Проект: /opt/sportomatics/
```

## Git

```
Remote: git@github.com:realcomp/khl.git
Основная ветка разработки: perf-audit-autofix
```
